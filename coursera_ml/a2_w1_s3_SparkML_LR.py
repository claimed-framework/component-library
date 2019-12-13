#!/usr/bin/env python
# coding: utf-8

# In case you want to learn how ETL is done, please run the following notebook first and update the file name below accordingly
# 
# https://github.com/IBM/coursera/blob/master/coursera_ml/a2_w1_s3_ETL.ipynb
# 

# In[1]:


# delete files from previous runs
get_ipython().system('rm -f hmp.parquet*')

# download the file containing the data in PARQUET format
get_ipython().system('wget https://github.com/IBM/coursera/raw/master/hmp.parquet')
    
# create a dataframe out of it
df = spark.read.parquet('hmp.parquet')

# register a corresponding query table
df.createOrReplaceTempView('df')


# In[2]:


df_energy = spark.sql("""
select sqrt(sum(x*x)+sum(y*y)+sum(z*z)) as label, class from df group by class
""")      
df_energy.createOrReplaceTempView('df_energy')          


# In[3]:


df_join = spark.sql('select * from df inner join df_energy on df.class=df_energy.class')


# In[4]:


df_join.show()


# In[5]:



from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import Normalizer


vectorAssembler = VectorAssembler(inputCols=["x","y","z"],
                                  outputCol="features")
normalizer = Normalizer(inputCol="features", outputCol="features_norm", p=1.0)


# In[6]:


from pyspark.ml.regression import LinearRegression

lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)


# In[7]:


from pyspark.ml import Pipeline
pipeline = Pipeline(stages=[vectorAssembler, normalizer,lr])


# In[ ]:


model = pipeline.fit(df_join)


# In[ ]:


prediction = model.transform(df_join)


# In[ ]:


prediction.show()


# In[ ]:


model.stages[2].summary.r2

