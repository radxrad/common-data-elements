#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

doc_id = "14JjBoqKAOsSfXy93K0yG2EWteF1j5h92"


# In[4]:


def download_google_sheet_excel(doc_id):
    return pd.read_excel(f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=xlsx", sheet_name=None)


# In[5]:


data = download_google_sheet_excel(doc_id)


# In[6]:


data


# In[ ]:


def download_google_sheet(doc_id, grid_id):
    return pd.read_csv(
    f"https://docs.google.com/spreadsheets/d/{doc_id}/export?gid={grid_id}&format=csv",
     keep_default_na=False
    )


# In[2]:


def download_google_sheet_tab(doc_id, grid_id):
    return pd.read_csv(
    f"https://docs.google.com/spreadsheets/d/{doc_id}/export?gid={grid_id}&format=csv",
     keep_default_na=False
    )


# In[3]:


def get_column_names(doc_id, grid_id):
    data = download_google_sheet_tab(doc_id, grid_id)
    return data.columns


# In[4]:


field_names = [[get_column_names(doc_id, grid_id), grid_id] for grid_id in grid_ids]


# In[5]:


all_fields = pd.DataFrame(field_names)
all_fields.columns = ["Variable / Field Name", "File Name"]
print(f"Number of variables: {all_fields.shape[0]}")


# In[6]:


all_fields.head()


# In[7]:


all_fields.tail()


# In[ ]:




