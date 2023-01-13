# What is the CLAIMED Library?

CLAIMED is a library of re-usable coarse-grained data processing
components to create Data & AI pipelines without programming skills

# How does the CLAIMED Library help developers and data scientists?

Lead Data Scientists and Domain Experts contribute to the library to
create opinionated, tested and re-usable components which are consumed
by citizen data scientists and developers which enables them to create
state of the art Data & AI workflows

# Why did IBM decide to contribute this open source project to LFAI?

An open source project is only as strong as its community. IBM wants to
grow the community around CLAIMED and Elyra since both projects are
very strategic open source projects for IBM and RedHat

# When did IBM open source it? 

The initial repository was created in 2015 and was originally used to
support the online courses IBM provides on Coursera.org and EDX.org.
From the very positive feedback IBM received from the learners, we
decided to create a general purpose library for AI, Machine Learning,
ETL and Data Science.

# Is there any competing project at IBM, or outside of IBM?

No. Open Source and open standards are the key principles of CLAIMED.
Therefore CLAIMED can be used in various contexts and therefore doesn't
compete but integrate.

# What action do we want the open source community to take?

We are actively looking for developers and data scientists to use the
library for the daily work including production ready software. We also
want them to report issues, fix issues via pull request, participate in
our discussions and contribute new components to the library

 
# How do we want you to use CLAIMED? 

CLAIMED can be consumed in many ways and we encourage and support all
scenarios. As each CLAIMED component is backed by a jupyter notebook or
(R|python|bash) script and defines a clear interface they can be
invoked directly from source code or from a command line. This way a
Data & AI pipeline can be build by arbitrary code or shell scripts. The
next level is using docker. As each CLAIMED component is automatically
compiled into a container image, a set of "docker run" commands will do
the job. Finally, CLAIMED also creates Kubeflow Pipeline Component
specifications automatically, therefore, CLAIMED can be used in any
Kubeflow Pipeline setting, where the Gold standard is using ML Exchange
as component repository and Elyra as graphical pipeline editor.

