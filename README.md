[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/6718/badge)](https://bestpractices.coreinfrastructure.org/projects/6718)
[![GitHub](https://img.shields.io/badge/issue_tracking-github-blue.svg)](https://github.com/claimed-framework/component-library/issues)



# CLAIMED - It's time to concentrate on your code only

For more information, please visit the project's [website](https://claimed-framework.github.io/)

[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/6718/badge)](https://bestpractices.coreinfrastructure.org/projects/6718)
[![GitHub](https://img.shields.io/badge/issue_tracking-github-blue.svg)](https://github.com/claimed-framework/component-library/issues)



# CLAIMED - The Component Library for AI, Machine Learning, ETL, and Data Science
---
**TL;DR** [Video on YouTube](https://www.youtube.com/watch?v=IhrIzLgY-Cg)
- set of re-usable coarse-grained components (just a bunch of code)
- think of tasks, not functions (e.g., read from a database, transform data, train model, deploy model, store result to cloud object storage)
- write once, runs everywhere: Kubeflow, Docker/Podman, CLI, KNative, Kubernetes, CodeEngine
- orchestrate with anything: shell script, Kubeflow, CWL, ...
- persistence layer / queue agnostic: Cloud Object Storage, file systems, PVC, Kafka, MQTT
- just use Python, bash or R - no other skills required (no Kubeflow component YAML, maven, Java, Dockerfile)
- 1st class citizen in JupyterLab and the Elyra Pipeline Editor (creating a low code / no code IDE for data science)
- upstream repository to IBM Watson Studio Pipelines contributed components in IBM Cloud Pak for Data

[FAQ](FAQ.md)

---

CLAIMED is a operator component framework for artificial intelligence, machine learning, "extract, transform, load" processes, and data science. The goal is to enable low-code/no-code rapid prototyping style programming to seamlessly CI/CD into production. The open source CLAIMED component library provides ready-made components for various business domains, supports multiple computer languages, works on different data flow editors and command line tools, and runs on various execution engines including Kubernetes (Job), Knative (Pod), Kubeflow (KFP component) and on the CLI using docker or podman. In addition to the open source library, clients create their private operator libraries using in conjunction with the open source one.
Core of CLAIMED is C3, the Claimed Component Compiler which takes source code in the form of jupyter notebooks or source files and compiles it to various target runtime environments, allowing to add additional targets as plugins. Currently, C3 supports python notebooks and python scripts as input and Kubernetes/OpenShift, Kubeflow Pipeline Components/RedHat OpenShift DataScience Pipelines, and plain docker/podmain (via CLAIMED CLI)
C3 does the following steps:
- extract meta information (name, description, interface, dependencies (requirements)) from source
- create (docker) container with dependencies and source added
- push container to registry
- create kubernetes-job.yaml
- create kubeflow-pipeline-component.yaml

To demonstrate its utility, we constructed a workflow composed exclusively of this library's components. To display the capabilities of this library, we made use of a publicly available Computed Tomography (CT) scan dataset [covidata]. We created a deep learning model, which is supposed to classify exams as either COVID-19 positive or negative. We built the pipeline with Elyra's Pipeline Visual Editor, with support for local, Airflow, and Kubeflow execution [https://arxiv.org/abs/2103.03281](https://arxiv.org/abs/2103.03281).


![Low Code / No Code pipeline creation tool for data science](https://github.com/IBM/claimed/raw/master/images/elyra_pipeline.png)
*Low Code / No Code pipeline creation tool for data science*

 **Bring the latest and greatest libraries to the hands of everybody.**

![AIX360/LIME highlights a poor deep learning covid classification model looking at bones only](https://github.com/IBM/claimed/raw/master/images/elyra_lime.png)
*AIX360/LIME highlights a poor deep learning covid classification model looking at bones only*

Components of this library can be exported as:
1. Kubeflow pipeline components
2. Apache Airflow components
3. Standalone graphical components for the Elyra pipeline editor
4. Standalone components to be run from the command line
5. Standalone components to be run as docker containers
6. Standalone components to be run as Kubernetes Service
7. Standalone components to be run as KNative Application or Job
8. Components to consume from or publish to Queue Managers like Kafka or MQTT
9. Components deployed to Kubernets wrapped into DAPR (as service or message consumer/producer)

![Visually create pipelines from notebooks and run everywhere](https://github.com/IBM/claimed/raw/master/images/elyra_graphical_export.png)
*Visually create pipelines from notebooks and run them everywhere*

Each notebook is following a similar format.

1. The first cell contains a description of the component itself.
2. The second cell installs all dependencies using pip3.
3. The third cell imports all dependencies.
4. The fourth cell contains a list of dependencies, input parameters, and return values as Python comments
5. The fifth cell reads the input parameters from environment variables.


![Export notebooks and files as runtime components for different engines](https://github.com/IBM/claimed/raw/master/images/elyra_cli_export.png)
*Export notebooks and files as runtime components for different engines*


To learn more on how this library works in practice, please have a look at the following [video](https://www.youtube.com/watch?v=FuV2oG55C5s)


## Achievements

🏆 [IEEE OSS AWARD 2023](https://arxiv.org/abs/2307.06824)

Kienzler, R., Khan, R., Nilmeier, J., Nesic, I., &amp; Haddad, I. (IEEE OSS 2023). Claimed -- the open source framework for building coarse-grained operators for accelerated discovery in science. [arXiv:2307.06824](https://arxiv.org/abs/2307.06824)

## Related work
[Ploomber](https://github.com/ploomber/ploomber)

[Orchest](https://www.orchest.io/)

[covidata] Joseph Paul Cohen et al. *COVID-19 Image Data Collection: Prospective Predictions Are the Future*, arXiv:2006.11988, 2020

## Getting Help

We welcome your questions, ideas, and feedback. Please create an [issue](https://github.com/claimed-framework/component-library/issues) or a [discussion thread](https://github.com/claimed-framework/component-library/discussions).
Please see [VULNERABILITIES.md](VULNERABILITIES.md) for reporting vulnerabilities.

## Contributing to CLAIMED
Interested in helping make CLAIMED better? We encourage you to take a look at our 
[Contributing](CONTRIBUTING.md) page.

## License
This software is released under Apache License v2.0


## Credits

CLAIMED is supported by the EU’s Horizon Europe program under Grant Agreement number 101131841 and also received funding from the Swiss State Secretariat for Education, Research and Innovation (SERI) and the UK Research and Innovation (UKRI).



# Install

```bash
pip install claimed
```

This package installs the [CLAIMED Component Library (CCL)](https://pypi.org/project/claimed/), [CLAIMED Component Compiler (C3)](https://pypi.org/project/claimed-c3/) and the [CLAIMED CLI tool](https://pypi.org/project/claimed-cli/) which can be used to run operators locally. 


# Build & Publish
```bash
python -m build # might require a 'pip install build'
python -m twine upload --repository pypi dist/* # might require a 'pip install twine'
rm -r dist
```



