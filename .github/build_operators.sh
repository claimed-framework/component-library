#!/bin/bash
# This script creates operators for all operator files in the last commit and pushes the images to a registry.
# The KFP component yaml and Kubernetes job yaml files are added to git and pushed to branch main.
# TODO: claimed-c3 v0.2.5 is using the default version 0.1 and cannot auto-increase the version.

echo 'Running build_operators.sh'

git checkout main
# Get commit ids
log_file=".github/build_operators_commits.txt"
last_commit=$(sed -n '$p' $log_file)
echo "Last commit: "$last_commit
current_commit=$(git rev-parse --short main)
echo "Current commit: "$current_commit
# Get list of changed files from last build
file_list=$(git diff --name-only $last_commit $current_commit)
echo 'File list: '$file_list
# Add current commit id to log
echo "$current_commit" >> "$log_file"
git add $log_file

# Get default repository from env
default_repository=${repository:-docker.io/romeokienzler}
echo 'default repository: '$default_repository
default_log_level=${log_level:-INFO}
echo 'default log_level: '$default_log_level
image_list=''

for file in $file_list
do
  # Check if the file is in the directory operators and ends with .py or .ipynb
  if [[ $file =~ ^operators/.*\.(py|ipynb)$ ]]; then
    echo "Processing file "$file

    if ! [ -f $file ]; then
      # File not found in main
      echo "File not found."
      continue
    fi

    dir=$(dirname "$file")
    bname="$(basename ${file})"

    # Reset variables
    gridwrapper=false
    cos=false
    process=false
    repository=False
    version=false
    additional_files=false
    log_level=false
    dockerfile_template_path=false
    image=''

    # Reading settings from optional cfg file
    config_file=${file%.*}.cfg
    if [ -f $config_file ]; then
      while read LINE; do declare "$LINE"; done < $config_file
    else
      # Missing cfg file
      echo "Config file not found, skipping file. Please add <operator>.cfg for to create the operator."
      continue
    fi

    # Get c3 command
    if [[ -n $gridwrapper && $gridwrapper != 'false' ]]; then
      # Create grid wrapper
      command='c3_create_gridwrapper '$file

      # Add process name for grid wrapper
      if [[ -n $process && $process != 'false' ]]; then
        command=' -p '$process
      else
        command=' -p grid_process'
      fi

      if [[ -n $cos && $cos != 'false' ]]; then
        # Use cos grid wrapper
        command+=' --cos'
        # Add cos grid wrapper files to git
        git_files=${dir}/cgw_${bname%.*}.py
        git_files+=' '${dir}/cgw_${bname%.*}.yaml
        git_files+=' '${dir}/cgw_${bname%.*}.job.yaml
      else
        # Add grid wrapper files to git
        git_files=${dir}/gw_${bname%.*}.py
        git_files+=' '${dir}/gw_${bname%.*}.yaml
        git_files+=' '${dir}/gw_${bname%.*}.job.yaml
      fi
    else
      # Create normal operator
      command='c3_create_operator '$file
      # Add KFP component yaml and Kubernetes job yaml to git
      git_files=${file%.*}.yaml
      git_files+=' '${file%.*}.job.yaml
    fi

    # Get repository
    if [[ -n $repository && $repository != 'false' ]]; then
      command+=' -r '$repository
    else
      # Use default repository
      command+=' -r '$default_repository
    fi

    # Optionally add version
    if [[ -n $version && $version != 'false' ]]; then
      command+=' -v '$version
    fi

    # Optionally add additional files
    if [[ -n $additional_files && $additional_files != 'false' ]]; then
      command+=' '$additional_files
    fi

    # Add log_level
    if [[ -n $log_level && $log_level != 'false' ]]; then
      command+=' -l '$log_level
    else
      command+=' -l '$default_log_level
    fi

    # Optionally add dockerfile_template_path
    if [[ -n $dockerfile_template_path && $dockerfile_template_path != 'false' ]]; then
      command+=' --dockerfile_template_path '$dockerfile_template_path
    fi

    # Execute command
    echo 'Run c3 with: '$command
    $command

    # Check error code from command
    if [ $? -eq 0 ]; then
      echo "Operator created."
      # Add new files to git
      for git_file in $git_files
      do
        git add $git_file
      done

      # Get image name from yaml file
      while read line;
      do
        # strip line
        line=${line// /}
        # check of image substring and replace first : with =
        if [[ $line = image:* ]]; then declare "${line/:/=}"; fi
      done < ${git_files##* }
      # add image to image_list
      image_list+=' '$image

    else
      echo "Command failed with exit status $?"
    fi
  fi
done

# Push files to main if an operator was created
git pull
git commit -m "operators build [skip ci]"
git push origin HEAD:main

# Adding tags for each generated image
for image in $image_list
do
  echo "Add tag ${image/:/=}"
  git tag -f ${image/:/=} -m $image;
done
git push --tags
