[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/6718/badge)](https://bestpractices.coreinfrastructure.org/projects/6718)
[![GitHub](https://img.shields.io/badge/issue_tracking-github-blue.svg)](https://github.com/claimed-framework/component-library/issues)



# CLAIMED - The Component Library for AI, Machine Learning, ETL, and Data Science

**TL;DR**
- set of re-usable coarse-grained components (just a bunch of code)
- think of tasks, not functions (e.g., read from a database, transform data, train model, deploy model, store result to cloud object storage)
- write once, runs everywhere: Kubeflow, Apache Airflow, CLI, KNative, Docker, Kubernetes
- orchestrate with anything: shell script, Kubeflow, Airflow, Argo, Tekton
- persistence layer / queue agnostic: Cloud Object Storage, file systems, PVC, Kafka, MQTT
- just use Python - no other skills required (no Kubeflow component YAML, maven, Java)
- 1st class citizen in JupyterLab and the Elyra Pipeline Editor (creating a low code / no code IDE for data science)
- upstream repository to IBM Watson Studio Pipelines contributed components in IBM Cloud Pak for Data

You also might wanna have a look at our [FAQ](FAQ.md)


CLAIMED is a component library for artificial intelligence, machine learning, "extract, transform, load" processes, and data science. The goal is to enable low-code/no-code rapid prototyping style programming to seamlessly CI/CD into production. The library provides ready-made components for various business domains, supports multiple computer languages, works on different data flow editors and command line tools, and runs on various execution engines including Kubernetes, KNative, Kubeflow, Airflow or plain docker. To demonstrate its utility, we constructed a workflow composed exclusively of this library's components. To display the capabilities of this library, we made use of a publicly available Computed Tomography (CT) scan dataset [covidata]. We created a deep learning model, which is supposed to classify exams as either COVID-19 positive or negative. We built the pipeline with Elyra's Pipeline Visual Editor, with support for local, Airflow, and Kubeflow execution [https://arxiv.org/abs/2103.03281](https://arxiv.org/abs/2103.03281).


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
