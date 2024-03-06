#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


file_name = "../Data Sharing_FIU_v9_2022-12-29_pr.xlsx"


# In[3]:


data_sheets = pd.read_excel(file_name, sheet_name=None)


# In[4]:


field_names = []
for sheet in data_sheets.items():
    columns = sheet[1].columns
    sheet_name = sheet[0]
    for column in columns:
        field_names.append([column, sheet_name])


# In[5]:


all_fields = pd.DataFrame(field_names)
all_fields.columns = ["Variable / Field Name", "File Name"]
print(f"Number of variables: {all_fields.shape[0]}")


# In[6]:


all_fields.head()


# In[7]:


all_fields.tail(50)


# In[ ]:




