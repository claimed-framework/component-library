#!/bin/bash
# This script creates operators for all operator files in the last commit and pushes the images to a registry.
# The KFP component yaml and Kubernetes job yaml files are added to git and pushed to branch main.

# default values
default_repository='docker.io/claimed'

# get list of changed files from last commit
file_list=$(git diff-tree --no-commit-id --name-only -r HEAD)
file_list=dummy/dummy.py
commit=false

for file in $file_list
do
  # reading settings from optional cfg file
  config_file=${file%.*}.cfg
  if [ -f $config_file ]; then
    while read LINE; do declare "$LINE"; done < $config_file
  fi

  # get c3 command
  if [[ $gridwrapper ]]; then
    command='c3_create_gridwrapper '$file
    if [[ $cos ]]; then
      # use cos grid wrapper
      command+=' --cos'
    fi
  else
    command='c3_create_operator '$file
  fi

  # get repository
  if [[ $repository ]]; then
    command+=' -r '$repository
  else
    command+=' -r '$default_repository
  fi

  # get version
  if [[ $version ]]; then
    command=$command' -v '$version
  fi

  # get additional files
  if [[ ${additional_files} ]]; then
    command=$command' '${additional_files}
  fi

  echo $command
  commit=true
done
