#!/usr/bin/env python
# coding: utf-8

# # Graded Programming Assignment
# 
# In this assignment, you will implement re-use the unsupervised anomaly detection algorithm but turn it into a simpler feed forward neural network for supervised classification.
# 
# You are training the neural network from healthy and broken samples and at later stage hook it up to a message queue for real-time anomaly detection.
# 
# We've provided a skeleton for you containing all the necessary code but left out some important parts indicated with ### your code here ###
# 
# After you’ve completed the implementation please submit it to the autograder
# 

# In[2]:


get_ipython().system('pip install tensorflow==2.12.0')


# In[3]:


import tensorflow as tf
if not tf.__version__ == '2.12.0':
    print(tf.__version__)
    raise ValueError('please upgrade to TensorFlow 2.12.0, or restart your Kernel (Kernel->Restart & Clear Output)')


# Now we import all the dependencies 

# In[4]:


import numpy as np
from numpy import concatenate
from matplotlib import pyplot
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
import sklearn
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Activation
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from queue import Queue
import pandas as pd
import json
get_ipython().run_line_magic('matplotlib', 'inline')


# We grab the files necessary for taining. Those are sampled from the lorenz attractor model implemented in NodeRED. Those are two serialized pickle numpy arrays. In case you are interested in how these data has been generated please have a look at the following tutorial. https://developer.ibm.com/tutorials/iot-deep-learning-anomaly-detection-2/

# In[5]:


get_ipython().system('rm watsoniotp.*')
get_ipython().system('wget https://raw.githubusercontent.com/romeokienzler/developerWorks/master/lorenzattractor/watsoniotp.healthy.phase_aligned.pickle')
get_ipython().system('wget https://raw.githubusercontent.com/romeokienzler/developerWorks/master/lorenzattractor/watsoniotp.broken.phase_aligned.pickle')
get_ipython().system('mv watsoniotp.healthy.phase_aligned.pickle watsoniotp.healthy.pickle')
get_ipython().system('mv watsoniotp.broken.phase_aligned.pickle watsoniotp.broken.pickle')


# De-serialize the numpy array containing the training data

# In[6]:


data_healthy = pickle.load(open('watsoniotp.healthy.pickle', 'rb'), encoding='latin1')
data_broken = pickle.load(open('watsoniotp.broken.pickle', 'rb'), encoding='latin1')


# Reshape to three columns and 3000 rows. In other words three vibration sensor axes and 3000 samples

# Since this data is sampled from the Lorenz Attractor Model, let's plot it with a phase lot to get the typical 2-eyed plot. First for the healthy data

# In[8]:


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Necessary for 3D plotting

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(data_healthy[:,0], data_healthy[:,1], data_healthy[:,2], lw=0.5)
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Lorenz Attractor")

plt.show()


# Then for the broken one

# In[10]:


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Necessary for 3D plotting

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(data_broken[:,0], data_broken[:,1], data_broken[:,2], lw=0.5)
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Lorenz Attractor")

plt.show()


# In the previous examples, we fed the raw data into an LSTM. Now we want to use an ordinary feed-forward network. So we need to do some pre-processing of this time series data
# 
# A widely-used method in traditional data science and signal processing is called Discrete Fourier Transformation. This algorithm transforms from the time to the frequency domain, or in other words, it returns the frequency spectrum of the signals.
# 
# The most widely used implementation of the transformation is called FFT, which stands for Fast Fourier Transformation, let’s run it and see what it returns
# 

# In[11]:


data_healthy_fft = np.fft.fft(data_healthy).real
data_broken_fft = np.fft.fft(data_broken).real


# Let’s first have a look at the shape and contents of the arrays.

# In[12]:


print (data_healthy_fft.shape)
print (data_healthy_fft)


# First, we notice that the shape is the same as the input data. So if we have 3000 samples, we get back 3000 spectrum values, or in other words 3000 frequency bands with the intensities.
# 
# The second thing we notice is that the data type of the array entries is not float anymore, it is complex. So those are not complex numbers, it is just a means for the algorithm the return two different frequency compositions in one go. The real part returns a sine decomposition and the imaginary part a cosine. We will ignore the cosine part in this example since it turns out that the sine part already gives us enough information to implement a good classifier.
# 
# But first let’s plot the two arrays to get an idea how a healthy and broken frequency spectrum differ
# 

# In[13]:


fig, ax = plt.subplots(num=None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')
size = len(data_healthy_fft)
ax.plot(range(0,size), data_healthy_fft[:,0].real, '-', color='blue', animated = True, linewidth=1)
ax.plot(range(0,size), data_healthy_fft[:,1].real, '-', color='red', animated = True, linewidth=1)
ax.plot(range(0,size), data_healthy_fft[:,2].real, '-', color='green', animated = True, linewidth=1)


# In[14]:


fig, ax = plt.subplots(num=None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')
size = len(data_healthy_fft)
ax.plot(range(0,size), data_broken_fft[:,0].real, '-', color='blue', animated = True, linewidth=1)
ax.plot(range(0,size), data_broken_fft[:,1].real, '-', color='red', animated = True, linewidth=1)
ax.plot(range(0,size), data_broken_fft[:,2].real, '-', color='green', animated = True, linewidth=1)


# So, what we've been doing is so called feature transformation step. We’ve transformed the data set in a way that our machine learning algorithm – a deep feed forward neural network implemented as binary classifier – works better. So now let's scale the data to a 0..1

# In[15]:


def scaleData(data):
    # normalize features
    scaler = MinMaxScaler(feature_range=(0, 1))
    return scaler.fit_transform(data)


# And please don’t worry about the warnings. As explained before we don’t need the imaginary part of the FFT

# In[16]:


data_healthy_scaled = scaleData(data_healthy_fft)
data_broken_scaled = scaleData(data_broken_fft)


# In[17]:


data_healthy_scaled = data_healthy_scaled.T
data_broken_scaled = data_broken_scaled.T


# Now we reshape again to have three examples (rows) and 3000 features (columns). It's important that you understand this. We have turned our initial data set which containd 3 columns (dimensions) of 3000 samples. Since we applied FFT on each column we've obtained 3000 spectrum values for each of the 3 three columns. We are now using each column with the 3000 spectrum values as one row (training example) and each of the 3000 spectrum values becomes a column (or feature) in the training data set

# In[18]:


data_healthy_scaled.reshape(3, 3000)
data_broken_scaled.reshape(3, 3000)


# # Start of Assignment
# 
# The first thing we need to do is to install a little helper library for submitting the solutions to the coursera grader:

# In[19]:


get_ipython().system('rm -f rklib.py')
get_ipython().system('wget https://raw.githubusercontent.com/IBM/coursera/master/rklib.py')


# Please specify you email address you are using with cousera here:

# In[20]:


from rklib import submit, submitAll
key = "4vkB9vnrEee8zg4u9l99rA"
all_parts = ["O5cR9","0dXlH","ZzEP8"]

email = "newpetsite01@gmail.com"


# 
# ## Task
# 
# Given, the explanation above, please fill in the following two constants in order to make the neural network work properly

# In[21]:


#### your code here ###
dim = 3000
samples = 3


# ### Submission
# 
# Now it’s time to submit your first solution. Please make sure that the secret variable contains a valid submission token. You can obtain it from the courser web page of the course using the grader section of this assignment.
# 

# In[23]:


part = "O5cR9"
token = "JB8xJ03yzyrp2MFK"  # Have a look here if you need more information on how to obtain the token: https://youtu.be/GcDo0Rwe06U?t=276

parts_data = {}
parts_data["0dXlH"] = json.dumps({"number_of_neurons_layer1": 0, "number_of_neurons_layer2": 0, "number_of_neurons_layer3": 0, "number_of_epochs": 0})
parts_data["O5cR9"] = json.dumps({"dim": dim, "samples": samples})
parts_data["ZzEP8"] = None 

submitAll(email, token, key, parts_data)


# To observe how training works we just print the loss during training

# In[24]:


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        sys.stdout.write(str(logs.get('loss'))+str(', '))
        sys.stdout.flush()
        self.losses.append(logs.get('loss'))
        
lr = LossHistory()


# ## Task
# 
# Please fill in the following constants to properly configure the neural network. For some of them you have to find out the precise value, for others you can try and see how the neural network is performing at a later stage. The grader only looks at the values which need to be precise
# 

# In[25]:


number_of_neurons_layer1 = 128
number_of_neurons_layer2 = 64
number_of_neurons_layer3 = 1
number_of_epochs = 50


# ### Submission
# 
# Please submit your constants to the grader

# In[26]:


parts_data = {}
parts_data["0dXlH"] = json.dumps({"number_of_neurons_layer1": number_of_neurons_layer1, "number_of_neurons_layer2": number_of_neurons_layer2, "number_of_neurons_layer3": number_of_neurons_layer3, "number_of_epochs": number_of_epochs})
parts_data["O5cR9"] = json.dumps({"dim": dim, "samples": samples})
parts_data["ZzEP8"] = None 
                                 
                                 
token = "JB8xJ03yzyrp2MFK"


submitAll(email, token, key, parts_data)


# ## Task
# 
# Now it’s time to create the model. Please fill in the placeholders. Please note since this is only a toy example, we don't use a separate corpus for training and testing. Just use the same data for fitting and scoring
# 

# In[29]:


from tensorflow.keras import optimizers

# Create the optimizer with the learning_rate parameter
sgd = optimizers.SGD(learning_rate=0.01, clipnorm=1.)

model = Sequential()
model.add(Dense(number_of_neurons_layer1, input_shape=(dim,), activation='relu'))
model.add(Dense(number_of_neurons_layer2, activation='relu'))
model.add(Dense(number_of_neurons_layer3, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer=sgd)

def train(data, label):
    model.fit(features, labels, epochs=number_of_epochs, batch_size=72, validation_data=(data, label), verbose=0, shuffle=True, callbacks=[lr])

def score(data):
    return model.predict(data)


# We prepare the training data by concatenating a label “0” for the broken and a label “1” for the healthy data. Finally we union the two data sets together

# In[30]:


label_healthy = np.repeat(1,3)
label_healthy.shape = (3,1)
label_broken = np.repeat(0,3)
label_broken.shape = (3,1)

train_healthy = np.hstack((data_healthy_scaled,label_healthy))
train_broken = np.hstack((data_broken_scaled,label_broken))
train_both = np.vstack((train_healthy,train_broken))


# Let’s have a look at the two training sets for broken and healthy and at the union of them. Note that the last column is the label

# In[31]:


pd.DataFrame(train_healthy)


# In[32]:


pd.DataFrame(train_broken)


# In[33]:


pd.DataFrame(train_both)


# So those are frequency bands. Notice that although many frequency bands are having nearly the same energy, the neural network algorithm still can work those out which are significantly different. 
# 
# ## Task
# 
# Now it’s time to do the training. Please provide the first 3000 columns of the array as the 1st parameter and column number 3000 containing the label as 2nd parameter. Please use the python array slicing syntax to obtain those. 
# 
# The following link tells you more about the numpy array slicing syntax
# https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.indexing.html
# 

# In[34]:


features = train_both[:,:3000]  
labels = train_both[:,3000] 


# Now it’s time to do the training. You should see the loss trajectory go down, we will also plot it later. Note: We also could use TensorBoard for this but for this simple scenario we skip it. In some rare cases training doesn’t converge simply because random initialization of the weights caused gradient descent to start at a sub-optimal spot on the cost hyperplane. Just recreate the model (the cell which contains *model = Sequential()*) and re-run all subsequent steps and train again
# 
# 

# In[35]:


train(features,labels)


# Let's plot the losses

# In[36]:


fig, ax = plt.subplots(num=None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')
size = len(lr.losses)
ax.plot(range(0,size), lr.losses, '-', color='blue', animated = True, linewidth=1)


# Now let’s examine whether we are getting good results. Note: best practice is to use a training and a test data set for this which we’ve omitted here for simplicity

# In[37]:


score(data_healthy_scaled)


# In[38]:


score(data_broken_scaled)


# ### Submission
# 
# In case you feel confident that everything works as it should (getting values close to one for the healthy and close to zero for the broken case) you can make sure that the secret variable contains a valid submission token and submit your work to the grader
# 

# In[39]:


parts_data = {}
parts_data["0dXlH"] = json.dumps({"number_of_neurons_layer1": number_of_neurons_layer1, "number_of_neurons_layer2": number_of_neurons_layer2, "number_of_neurons_layer3": number_of_neurons_layer3, "number_of_epochs": number_of_epochs})
parts_data["O5cR9"] = json.dumps({"dim": dim, "samples": samples})

                                 
                                 
token = "JB8xJ03yzyrp2MFK"


# In[40]:


prediction = str(np.sum(score(data_healthy_scaled))/3)
myData={'healthy' : prediction}
myData
parts_data["ZzEP8"] = json.dumps(myData)
submitAll(email, token, key, parts_data)


# In[ ]:




