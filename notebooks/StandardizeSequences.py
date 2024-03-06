#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df = pd.read_csv("../data/Exosome/Das/rad_018_780-01_v001/rad_018_780-01_DATA_PrimerSet_v001.csv", dtype=str)


# In[3]:


df.head()


# In[4]:


df["target_organism_taxonomy_id"] = df["target_organism_taxonomy_id"].astype(str)
df["target_organism_taxonomy_id"] = df["target_organism_taxonomy_id"].str.replace(".0","")
df["target_analyte_sequence"] = df["target_analyte_sequence"].str.upper()
df["target_analyte_sequence"] = "5'-" + df["target_analyte_sequence"] + "-3'"
df["primer_sequence"] = df["primer_sequence"].str.upper()
df["primer_sequence"] = "5'-" + df["primer_sequence"] + "-3'"
df.dropna(how='all', inplace=True)
df.dropna(how='all', axis=1, inplace=True)


# In[5]:


df.head()


# In[6]:


df.to_csv("../data/Exosome/Das/rad_018_780-01_v001/rad_018_780-01_DATA_PrimerSet_v001_pr.csv", index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




