#!/usr/bin/env python
# coding: utf-8

# Transfer Learnning Example Notebook using ResNet50 with the ImageNet weights.
# 
# @author Maximilian Dargatz
# 
# @author Romeo Kienzler
# 
# Data used in this notebook:
# 
# http://www.andrewjanowczyk.com/deep-learning/
# 
# http://www.andrewjanowczyk.com/use-case-6-invasive-ductal-carcinoma-idc-segmentation/

# In[ ]:


get_ipython().system('if [ -f IDC_regular_ps50_idx5.zip ]; then echo "images already downloaded"; else wget http://andrewjanowczyk.com/wp-static/IDC_regular_ps50_idx5.zip; fi')
get_ipython().system('if [ -d images ]; then echo "images folder already created"; else echo "creating images folder and unzipping "; mkdir images;  unzip IDC_regular_ps50_idx5.zip -d images/ ; fi')


# In[ ]:


get_ipython().run_cell_magic('bash', '', 'mkdir imagesprep\nmkdir imagesprep/train\nmkdir imagesprep/train/0\nmkdir imagesprep/train/1\nmkdir imagesprep/test\nmkdir imagesprep/test/0\nmkdir imagesprep/test/1\n\ni=0\nfor file in `find images` -name ".png"; do \n    ((i++))\n    if ! ((i % 10 == 0)); then \n        if [[ $file == *"class0.png"* ]]; then \n            cp $file imagesprep/train/0/\n        elif [[ $file == *"class1.png"* ]]; then \n            cp $file imagesprep/train/1/\n        fi\n    else \n        if [[ $file == *"class0.png"* ]]; then \n            cp $file imagesprep/test/0/\n        elif [[ $file == *"class1.png"* ]]; then \n            cp $file imagesprep/test/1/\n        fi\n    fi\ndone')


# In[ ]:


from PIL import Image
import numpy as np
import zipfile
from os import walk
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.model_selection import train_test_split

import keras
from math import ceil
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input
from keras.callbacks import EarlyStopping
from keras import Model, layers
from keras.models import load_model, model_from_json


# ## 2. Prepare the Images

# In[ ]:


train_datagen = ImageDataGenerator(
    shear_range=10,
    zoom_range=0.2,
    horizontal_flip=True,
    preprocessing_function=preprocess_input)

train_generator = train_datagen.flow_from_directory(
    'imagesprep/train',
    batch_size=32,
    class_mode='binary',
    target_size=(50,50))

validation_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input)

##brauch dann ein update auf das val set!!
validation_generator = validation_datagen.flow_from_directory(
    'imagesprep/test',
    shuffle=False,
    class_mode='binary',
    target_size=(50,50))


# In[ ]:


conv_base = ResNet50(
    include_top=False,
    weights='imagenet')

for layer in conv_base.layers:
    layer.trainable = False


# ## 3. Create a CNN (based on ResNet50)

# In[ ]:


x = conv_base.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x) 
predictions = layers.Dense(2, activation='softmax')(x)
model = Model(conv_base.input, predictions)


# In[ ]:


optimizer = keras.optimizers.Adam()
model.compile(loss='sparse_categorical_crossentropy',
              optimizer=optimizer,
              metrics=['accuracy'])


# ## 4. Train

# In[ ]:


history = model.fit_generator(generator=train_generator,
                              #steps_per_epoch = 4, # nur für dry run da ja gar nich alles berücksichtigt wird
                              steps_per_epoch=ceil(249762/ 32),  
                              epochs=5,
                              validation_data=validation_generator,
                              validation_steps= 25,
                              #callbacks = [EarlyStopping(monitor='val_loss', patience=3)]
                             )


# In[ ]:


print(history.history.keys())


# In[ ]:


plt.figure(1, figsize = (15,8)) 
    
plt.subplot(221)  
plt.plot(history.history['acc'])  
plt.plot(history.history['val_acc'])  
plt.title('model accuracy')  
plt.ylabel('accuracy')  
plt.xlabel('epoch')  
plt.legend(['train', 'valid']) 
    
plt.subplot(222)  
plt.plot(history.history['loss'])  
plt.plot(history.history['val_loss'])  
plt.title('model loss')  
plt.ylabel('loss')  
plt.xlabel('epoch')  
plt.legend(['train', 'valid']) 

plt.show()


# In[ ]:




