#!/usr/bin/env python
# coding: utf-8

# # ConcatenateRADx-radDicts
# This notebook concatenates the individual RADx-rad data dictionary template files (Google sheets) and saves the data elements in a .csv file.

# In[1]:


import os
from utils import *


# ### Read and concatenate the RADx-rad data dictionary template files

# In[2]:


data_elements = download_data_element_templates()
data_elements.drop_duplicates(inplace=True)
print("Number of data elements:", data_elements.shape[0])


# In[3]:


### Save as a csv file


# In[4]:


directory = "../data/dictionaries"
os.makedirs(directory, exist_ok=True)
data_elements.to_csv("../data/dictionaries/RADx-rad_Dictionary_Template.csv", index=False)

