#!/usr/bin/env python
# coding: utf-8

# # Merges two data dictionaries

# In[1]:


import pandas as pd


# In[2]:


filename1 = "../data/Exosome/Wong/EFIRM_NAB_2023-01-11/EFIRM Neutralizing Antibody_U18_UCLA_2023_01_11 - without IDs_DICT.csv"
filename2 = "../data/Exosome/Wong/SERS_2013-01-14/SERS template_1_13_2023_pr3_DICT.csv"
filename = "../data/Exosome/Wong/EFIRM_NAB_SERS_2023-01-14/EFIRM_NAB_SERS_2023-01-14_DICT.csv"


# In[3]:


df1 = pd.read_csv(filename1, keep_default_na=False,)
print(f"{filename1} dimensions: {df1.shape}")
df1.head()


# In[4]:


df2 = pd.read_csv(filename2, keep_default_na=False,)
print(f"{filename1} dimensions: {df2.shape}")
df2.head()


# In[5]:


df = pd.concat([df1, df2])
df.drop_duplicates(df, inplace=True)
print(f" dimensions: {df.shape}")


# In[6]:


print(f"{filename1} dimensions: {df.shape}")
df.head(1000)


# In[8]:


df.to_csv(filename, index=False)


# In[ ]:




