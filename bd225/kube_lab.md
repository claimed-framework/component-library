<center>
<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/cc201/labs/5_FinalProject_Coursera/images/labs_module_1_images_IDSNlogo.png" width="300">
</center>

# Apache Spark on Kubernetes Lab
> by @romeokienzler July 2021

## Objectives

In this lab, you will:

* Install *kind* - Kubernetes in Docker - an easy way to install and run a Kubernetes cluster inside a single docker container
* Create a so called *Kubernetes Pod* - a set of containers running inside Kubernetes - here, containing Apache Spark which we use to submit jobs against Kubernetes
* Submit Apache Spark jobs to Kubernetes 

## Prerequisites
Note: If you are running this lab within the Skillsnetwort Lab environment, all prerequisites are already installed for you

The only pre-requisites to this lab are:
* A working *docker* installation
* The *git* command line tool

# Project Overview
Welcome to the lab on how to submit Apache Spark applications to a Kubernetes cluster. This is straightforward thanks to the new native Kubernetes scheduler that has been added to Spark recently.

Kubernetes is a container orchestrator which allows to schedule millions of "docker" containers on huge compute clusters containing thousands of compute nodes. Originally invented and open sourced by Google, Kubernetes became the de-facto standard for cloud native application development and deployment inside and outside IBM. With RedHat OpenShift, IBM is the leader in hybrid cloud Kubernetes and within the top three companies contributing to Kubernetes open source code base.


# Install KIND - Kubernetes in Docker
On the right hand side to this instructions you'll see the Theia IDE. Please open a terminal by clicking on "Terminal->New Terminal".
Please enter the following commands in the terminal:

> git clone https://github.com/romeokienzler/new_horizons.git
> 
> cd new_horizons
> 
> cd kind
>
> ./install_kind.sh
> 
> ./create_kind_cluster.sh
> 
> alias k='kubectl'


## Deploy the Apache Spark Kubernetes Pod
Please continue entering the following commands in the terminal:

> k apply -f ../spark/pod_spark.yaml
> 
> k apply -f rbac.yaml

Now it is time to check the status of the Pod. Just enter the following command:

> k get po

If you see the following output it means that the Pod is not
yet available and you need to wait a bit.

```
NAME   READY   STATUS              RESTARTS   AGE  
spark  0/2     ContainerCreating   0          29s
```

Just issue the command again after some time:
> k get po

You should see an output like this:

```
NAME  READY   STATUS    RESTARTS   AGE
spark 2/2     Running   0          10m
```

Note that this Pod is called *spark* and contains two
containers *(2/2)* of which are both in status *Running*. Please also note that Kubernetes automatically *RESTARTS* failed pods - this hasn't happened here so far. Most probably because the *AGE* of this pod is only 10 minutes.

## Submit Apache Spark jobs to Kubernetes

Now it is time to enter the *spark* container of this Pod.
The command *exec* is told to provide interactive access (*-it*) to the container called *spark* (-c). With *--* we execute a shell (/bin/bash).

> k exec -it spark -c spark -- /bin/bash

You've now entered container *spark* in Pod *spark* inside Kubernetes. This container we will use to submit Spark applications to the Kubernetes cluster. This container is based on an image with the Apache Spark distribution and the *kubectl* command pre-installed.

If you are interested you can have a look at the [Dockerfile](https://github.com/romeokienzler/new_horizons/blob/main/spark/Dockerfile) to understand what's really inside.

You can also check out the [pod.yaml](https://github.com/romeokienzler/new_horizons/blob/main/spark/pod_spark.yaml). You'll notice that it contains two containers. One is Apache Spark, another one is providing a Kubernetes Proxy - a so called side car container - allowing to interact with the Kubernetes cluster from inside a Pod.


Inside the container you can use the *spark-submit* command which makes use of the new native Kubernetes scheduler that has been added to Spark recently.

The following command submits the *SparkPi* sample application to the cluster. SparkPi computes Pi and the more iterations you run, the more precise it gets:

```
./bin/spark-submit \
--master k8s://http://127.0.0.1:8001 \
--deploy-mode cluster \
--name spark-pi \
--class org.apache.spark.examples.SparkPi \
--conf spark.executor.instances=3 \
--conf spark.kubernetes.container.image=romeokienzler/spark-py:3.1.2 \
--conf spark.kubernetes.executor.limit.cores=1 \
local:///opt/spark/examples/jars/spark-examples_2.12-3.1.2.jar \
10
```




So let's have a look what's going on here:
- *./bin/spark-submit* is the command to submit applications to a Apache Spark cluster
- *--master k8s://http://127.0.0.1:8001* is the address of the Kubernetes API server - the way *kubectl* but also the Apache Spark native Kubernetes scheduler interacts with the Kubernetes cluster
- *--name spark-pi* provides a name for the job and the subsequent Pods created by the Apache Spark native Kubernetes scheduler are prefixed with that name
- *--class org.apache.spark.examples.SparkPi* provides the canonical name for the Spark application to run (Java package and class name)
- *--conf spark.executor.instances=1* tells the Apache Spark native Kubernetes scheduler how many Pods it has to create to parallelize the application. Note that on this single node development Kubernetes cluster increasing this number doesn't make any sense (besides adding overhead for parallelization)
- *--conf spark.kubernetes.container.image=romeokienzler/spark-py:3.1.2* tells the Apache Spark native Kubernetes scheduler which container image it should use for creating the driver and executor Pods. This image can be custom build using the provided Dockerfiles in *kubernetes/dockerfiles/spark/* and *bin/docker-image-tool.sh* in the Apache Spark distribution
- *--conf spark.kubernetes.executor.limit.cores=1* tells the Apache Spark native Kubernetes scheduler to set the CPU core limit to only use one core per executor Pod
- *local:///opt/spark/examples/jars/spark-examples_2.12-3.1.2.jar* indicates the *jar* file the application is contained in. Note that the *local://* prefix addresses a path within the container images provided by the *spark.kubernetes.container.image* option. Since we're using a *jar* provided by the Apache Spark distribution this is not a problem, otherwise the *spark.kubernetes.file.upload.path* option has to be set and an appropriate storage subsystem has to be configured, as described in the [documentation](https://spark.apache.org/docs/latest/running-on-kubernetes.html#running-spark-on-kubernetes)
- *10* tells the application to run for *10* iterations, then output the computed value of *Pi*

Please see the [documentation](https://spark.apache.org/docs/latest/running-on-kubernetes.html#configuration) for a full list of available parameters.

Once this command runs you can open a second terminal window within Theia and issue the following command:

> kubectl get po

This will show you the additional Pods being created by the Apache Spark native Kubernetes scheduler - one driver and at least one executor (with an exception if there is only one executor, it runs within the driver Pod). Here an example when using three executors (exact IDs replaced by X and Y for readability):

```
NAME              READY STATUS    RESTARTS AGE
spark             2/2   Running   0        28m
spark-pi-X-exec-1 1/1   Running   0        33s
spark-pi-X-exec-2 1/1   Running   0        33s
spark-pi-X-exec-3 1/1   Running   0        33s
spark-pi-X-driver 1/1   Running   0        44s
spark-pi-Y-driver 0/1   Completed 0        12m
```

You can see that Pod *spark-pi-Y-driver* is in status *Completed*, from a single executor run twelve minutes ago and that there are one driver and three executors actually running for job *spark-pi-X- ..*.

To check the job's elapsed time just execute (you need to replace the Pod name of course with the one on your system):
> kubectl logs spark-pi-6f62d17a800beb3e-driver |grep "Job 0 finished:"

You should get something like:
```
Job 0 finished: reduce at SparkPi.scala:38, took 8.446024 s
```
If you are interested in knowing what value for *Pi* the application came up with just issue:

> kubectl logs spark-pi-86d1f27a80018666-driver |grep "Pi is roughly "

And you'll see something like:
```
Pi is roughly 3.1416551416551415
```

Now you can play around with values for *spark.executor.instances*, *spark.kubernetes.executor.limit.cores=1* (0.1 is also a valid number) and number of iterations and see how it affects runtime and precision of the outcome.

This concludes this lab.