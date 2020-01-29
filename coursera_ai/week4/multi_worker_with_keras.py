# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + [markdown] colab_type="text" id="Tce3stUlHN0L"
# ##### Copyright 2019 The TensorFlow Authors.
#
#

# + colab={} colab_type="code" id="tuOe1ymfHZPu"
#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# + [markdown] colab_type="text" id="MfBg1C5NB3X0"
# # Multi-worker training with Keras
#
# <table class="tfo-notebook-buttons" align="left">
#   <td>
#     <a target="_blank" href="https://www.tensorflow.org/tutorials/distribute/multi_worker_with_keras"><img src="https://www.tensorflow.org/images/tf_logo_32px.png" />View on TensorFlow.org</a>
#   </td>
#   <td>
#     <a target="_blank" href="https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/distribute/multi_worker_with_keras.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Run in Google Colab</a>
#   </td>
#   <td>
#     <a target="_blank" href="https://github.com/tensorflow/docs/blob/master/site/en/tutorials/distribute/multi_worker_with_keras.ipynb"><img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />View source on GitHub</a>
#   </td>
#   <td>
#     <a href="https://storage.googleapis.com/tensorflow_docs/docs/site/en/tutorials/distribute/multi_worker_with_keras.ipynb"><img src="https://www.tensorflow.org/images/download_logo_32px.png" />Download notebook</a>
#   </td>
# </table>

# + [markdown] colab_type="text" id="xHxb-dlhMIzW"
# ## Overview
#
# This tutorial demonstrates multi-worker distributed training with Keras model using `tf.distribute.Strategy` API. With the help of the strategies specifically designed for multi-worker training, a Keras model that was designed to run on single-worker can seamlessly work on multiple workers with minimal code change.
#
# [Distributed Training in TensorFlow](../../guide/distributed_training.ipynb) guide is available for an overview of the distribution strategies TensorFlow supports for those interested in a deeper understanding of `tf.distribute.Strategy` APIs.
#
#

# + [markdown] colab_type="text" id="MUXex9ctTuDB"
# ## Setup
#
# First, setup TensorFlow and the necessary imports.

# + colab={} colab_type="code" id="IqR2PQG4ZaZ0"
from __future__ import absolute_import, division, print_function, unicode_literals

# + colab={} colab_type="code" id="bnYxvfLD-LW-"

import tensorflow_datasets as tfds
import tensorflow as tf
tfds.disable_progress_bar()

# + [markdown] colab_type="text" id="hPBuZUNSZmrQ"
# ## Preparing dataset
#
# Now, let's prepare the MNIST dataset from [TensorFlow Datasets](https://www.tensorflow.org/datasets). The [MNIST dataset](http://yann.lecun.com/exdb/mnist/) comprises 60,000
# training examples and 10,000 test examples of the handwritten digits 0–9,
# formatted as 28x28-pixel monochrome images.

# + colab={} colab_type="code" id="dma_wUAxZqo2"
BUFFER_SIZE = 10000
BATCH_SIZE = 64

def make_datasets_unbatched():
  # Scaling MNIST data from (0, 255] to (0., 1.]
  def scale(image, label):
    image = tf.cast(image, tf.float32)
    image /= 255
    return image, label

  datasets, info = tfds.load(name='mnist',
                            with_info=True,
                            as_supervised=True)

  return datasets['train'].map(scale).repeat(1000).cache().shuffle(BUFFER_SIZE)

train_datasets = make_datasets_unbatched().batch(BATCH_SIZE)


# + [markdown] colab_type="text" id="o87kcvu8GR4-"
# ## Build the Keras model
# Here we use `tf.keras.Sequential` API to build and compile a simple convolutional neural networks Keras model to train with our MNIST dataset.
#
# Note: For a more comprehensive walkthrough of building Keras model, please see [TensorFlow Keras Guide](https://www.tensorflow.org/guide/keras#sequential_model).
#

# + colab={} colab_type="code" id="aVPHl0SfG2v1"
def build_and_compile_cnn_model():
  model = tf.keras.Sequential([
      tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
      tf.keras.layers.MaxPooling2D(),
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(64, activation='relu'),
      tf.keras.layers.Dense(10, activation='softmax')
  ])
  model.compile(
      loss=tf.keras.losses.sparse_categorical_crossentropy,
      optimizer=tf.keras.optimizers.SGD(learning_rate=0.001),
      metrics=['accuracy'])
  return model


# + [markdown] colab_type="text" id="2UL3kisMO90X"
# Let's first try training the model for a small number of epochs and observe the results in single worker to make sure everything works correctly. You should expect to see the loss dropping and accuracy approaching 1.0 as epoch advances.

# + colab={} colab_type="code" id="6Qe6iAf5O8iJ"
single_worker_model = build_and_compile_cnn_model()
single_worker_model.fit(x=train_datasets, epochs=3, steps_per_epoch=5)

# + [markdown] colab_type="text" id="8YFpxrcsZ2xG"
# ## Multi-worker Configuration
#
# Now let's enter the world of multi-worker training. In TensorFlow, `TF_CONFIG` environment variable is required for training on multiple machines, each of which possibly has a different role. `TF_CONFIG` is used to specify the cluster configuration on each worker that is part of the cluster.
#
# There are two components of `TF_CONFIG`: `cluster` and `task`. `cluster` provides information about the training cluster, which is a dict consisting of different types of jobs such as `worker`. In multi-worker training, there is usually one `worker` that takes on a little more responsibility like saving checkpoint and writing summary file for TensorBoard in addition to what a regular `worker` does. Such worker is referred to as the 'chief' worker, and it is customary that the `worker` with `index` 0 is appointed as the chief `worker` (in fact this is how `tf.distribute.Strategy` is implemented). `task` on the other hand provides information of the current task.  
#
# In this example, we set the task `type` to `"worker"` and the task `index` to `0`. This means the machine that has such setting is the first worker, which will be appointed as the chief worker and do more work than other workers. Note that other machines will need to have `TF_CONFIG` environment variable set as well, and it should have the same `cluster` dict, but different task `type` or task `index` depending on what the roles of those machines are.
#
# For illustration purposes, this tutorial shows how one may set a `TF_CONFIG` with 2 workers on `localhost`.  In practice, users would create multiple workers on external IP addresses/ports, and set `TF_CONFIG` on each worker appropriately.
#
# Warning: Do not execute the following code in Colab.  TensorFlow's runtime will attempt to create a gRPC server at the specified IP address and port, which will likely fail.
#
# ```
# os.environ['TF_CONFIG'] = json.dumps({
#     'cluster': {
#         'worker': ["localhost:12345", "localhost:23456"]
#     },
#     'task': {'type': 'worker', 'index': 0}
# })
# ```
#
#

# + [markdown] colab_type="text" id="P94PrIW_kSCE"
# Note that while the learning rate is fixed in this example, in general it may be necessary to adjust the learning rate based on the global batch size.

# + [markdown] colab_type="text" id="UhNtHfuxCGVy"
# ## Choose the right strategy
#
# In TensorFlow, distributed training consists of synchronous training, where the steps of training are synced across the workers and replicas, and asynchronous training, where the training steps are not strictly synced.
#
# `MultiWorkerMirroredStrategy`, which is the recommended strategy for synchronous multi-worker training, will be demonstrated in this guide.
# To train the model, use an instance of `tf.distribute.experimental.MultiWorkerMirroredStrategy`.  `MultiWorkerMirroredStrategy` creates copies of all variables in the model's layers on each device across all workers.  It uses `CollectiveOps`, a TensorFlow op for collective communication, to aggregate gradients and keep the variables in sync.  The [`tf.distribute.Strategy` guide](../../guide/distributed_training.ipynb) has more details about this strategy.
# -


# + colab={} colab_type="code" id="1uFSHCJXMrQ-"
strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()

# + [markdown] colab_type="text" id="N0iv7SyyAohc"
# Note: `TF_CONFIG` is parsed and TensorFlow's GRPC servers are started at the time `MultiWorkerMirroredStrategy.__init__()` is called, so `TF_CONFIG` environment variable must be set before a `tf.distribute.Strategy` instance is created.

# + [markdown] colab_type="text" id="FMy2VM4Akzpr"
# `MultiWorkerMirroredStrategy` provides multiple implementations via the [`CollectiveCommunication`](https://github.com/tensorflow/tensorflow/blob/a385a286a930601211d78530734368ccb415bee4/tensorflow/python/distribute/cross_device_ops.py#L928) parameter.  `RING` implements ring-based collectives using gRPC as the cross-host communication layer.  `NCCL` uses [Nvidia's NCCL](https://developer.nvidia.com/nccl) to implement collectives.  `AUTO` defers the choice to the runtime.  The best choice of collective implementation depends upon the number and kind of GPUs, and the network interconnect in the cluster.

# + [markdown] colab_type="text" id="H47DDcOgfzm7"
# ## Train the model with MultiWorkerMirroredStrategy
#
# With the integration of `tf.distribute.Strategy` API into `tf.keras`, the only change you will make to distribute the training to multi-worker is enclosing the model building and `model.compile()` call inside `strategy.scope()`. The distribution strategy's scope dictates how and where the variables are created, and in the case of `MultiWorkerMirroredStrategy`, the variables created are `MirroredVariable`s, and they are replicated on each of the workers.
#
# Note: Currently there is a limitation in `MultiWorkerMirroredStrategy` where TensorFlow ops need to be created after the instance of strategy is created. If you see `RuntimeError: Collective ops must be configured at program startup`, try creating the instance of `MultiWorkerMirroredStrategy` at the beginning of the program and put the code that may create ops after the strategy is instantiated.
#
# Note: In this Colab, the following code can run with expected result, but however this is effectively single-worker training since `TF_CONFIG` is not set. Once you set `TF_CONFIG` in your own example, you should expect speed-up with training on multiple machines.
#
# Note: Since `MultiWorkerMirroredStrategy` does not support last partial batch handling, pass the `steps_per_epoch` argument to `model.fit()` when dataset is imbalanced on multiple workers.

# + colab={} colab_type="code" id="BcsuBYrpgnlS"
NUM_WORKERS = 2
# Here the batch size scales up by number of workers since 
# `tf.data.Dataset.batch` expects the global batch size. Previously we used 64, 
# and now this becomes 128.
GLOBAL_BATCH_SIZE = 64 * NUM_WORKERS
with strategy.scope():
  # Creation of dataset, and model building/compiling need to be within 
  # `strategy.scope()`.
  train_datasets = make_datasets_unbatched().batch(GLOBAL_BATCH_SIZE)
  multi_worker_model = build_and_compile_cnn_model()

# Keras' `model.fit()` trains the model with specified number of epochs and
# number of steps per epoch. Note that the numbers here are for demonstration
# purposes only and may not sufficiently produce a model with good quality.
multi_worker_model.fit(x=train_datasets, epochs=3000, steps_per_epoch=5000)

# + [markdown] colab_type="text" id="Rr14Vl9GR4zq"
# ### Dataset sharding and batch size
# In multi-worker training, sharding data into multiple parts is needed to ensure convergence and performance. However, note that in above code snippet, the datasets are directly sent to `model.fit()` without needing to shard; this is because `tf.distribute.Strategy` API takes care of the dataset sharding automatically in multi-worker trainings.
#
# If you prefer manual sharding for your training, automatic sharding can be turned off via `tf.data.experimental.DistributeOptions` api. Concretely,

# + colab={} colab_type="code" id="JxEtdh1vH-TF"
options = tf.data.Options()
options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.OFF
train_datasets_no_auto_shard = train_datasets.with_options(options)

# + [markdown] colab_type="text" id="NBCtYvmCH-7g"
# Another thing to notice is the batch size for the `datasets`. In the code snippet above, we use `GLOBAL_BATCH_SIZE = 64 * NUM_WORKERS`, which is `NUM_WORKERS` times as large as the case it was for single worker, because the effective per worker batch size is the global batch size (the parameter passed in `tf.data.Dataset.batch()`) divided by the number of workers, and with this change we are keeping the per worker batch size same as before.

# + [markdown] colab_type="text" id="XVk4ftYx6JAO"
# ## Performance
#
# You now have a Keras model that is all set up to run in multiple workers with `MultiWorkerMirroredStrategy`.  You can try the following techniques to tweak performance of multi-worker training.
#
# *   `MultiWorkerMirroredStrategy` provides multiple [collective communication implementations](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/distribute/cross_device_ops.py).  `RING` implements ring-based collectives using gRPC as the cross-host communication layer.  `NCCL` uses [Nvidia's NCCL](https://developer.nvidia.com/nccl) to implement collectives.  `AUTO` defers the choice to the runtime.  The best choice of collective implementation depends upon the number and kind of GPUs, and the network interconnect in the cluster.  To override the automatic choice, specify a valid value to the `communication` parameter of `MultiWorkerMirroredStrategy`'s constructor, e.g. `communication=tf.distribute.experimental.CollectiveCommunication.NCCL`.
# *    Cast the variables to `tf.float` if possible.  The official ResNet model includes [an example](https://github.com/tensorflow/models/blob/8367cf6dabe11adf7628541706b660821f397dce/official/resnet/resnet_model.py#L466) of how this can be done.
#
#
#
#

# + [markdown] colab_type="text" id="97WhAu8uKw3j"
# ## Fault tolerance
#
# In synchronous training, the cluster would fail if one of the workers fails and no failure-recovery mechanism exists. Using Keras with `tf.distribute.Strategy` comes with the advantage of fault tolerance in cases where workers die or are otherwise unstable. We do this by preserving training state in the distributed file system of your choice, such that upon restart of the instance that previously failed or preempted, the training state is recovered.
#
# Since all the workers are kept in sync in terms of training epochs and steps, other workers would need to wait for the failed or preempted worker to restart to continue.
#
# ### ModelCheckpoint callback
#
# To take advantage of fault tolerance in multi-worker training, provide an instance of `tf.keras.callbacks.ModelCheckpoint` at the `tf.keras.Model.fit()` call.  The callback will store the checkpoint and training state in the directory corresponding to the `filepath` argument to `ModelCheckpoint`.

# + colab={} colab_type="code" id="xIY9vKnUU82o"
# Replace the `filepath` argument with a path in the file system
# accessible by all workers.
callbacks = [tf.keras.callbacks.ModelCheckpoint(filepath='/tmp/keras-ckpt')]
with strategy.scope():
  multi_worker_model = build_and_compile_cnn_model()
multi_worker_model.fit(x=train_datasets,
                       epochs=3,
                       steps_per_epoch=5,
                       callbacks=callbacks)

# + [markdown] colab_type="text" id="Ii6VmEdOjkZr"
# If a worker gets preempted, the whole cluster pauses until the preempted worker is restarted. Once the worker rejoins the cluster, other workers will also restart. Now, every worker reads the checkpoint file that was previously saved and picks up its former state, thereby allowing the cluster to get back in sync. Then the training continues.
#
# If you inspect the directory containing the `filepath` you specified in `ModelCheckpoint`, you may notice some temporarily generated checkpoint files. Those files are needed for recovering the previously lost instances, and they will be removed by the library at the end of `tf.keras.Model.fit()` upon successful exiting of your multi-worker training.

# + [markdown] colab_type="text" id="ega2hdOQEmy_"
# ## See also
# 1. [Distributed Training in TensorFlow](https://www.tensorflow.org/guide/distributed_training) guide provides an overview of the available distribution strategies.
# 2. [Official models](https://github.com/tensorflow/models/tree/master/official), many of which can be configured to run multiple distribution strategies.
#
