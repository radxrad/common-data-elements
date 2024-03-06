#!/usr/bin/env python
# coding: utf-8

# # CheckDataElementTemplates
# This notebooks check the RADx-rad Data Element template files for empty fields and does consistency checks.
# 
# Author: Peter W. Rose, pwrose@ucsd.edu

# In[1]:


import pandas as pd
from utils import download_data_element_templates, check_empty_field, check_whitespace, check_field_types


# In[2]:


pd.options.display.max_rows = None  # display all rows
pd.options.display.max_columns = None  # display all columsns
pd.set_option('display.max_colwidth', None)


# ### Download the RADx-rad Data Element template files
# The templates are concatenated into a single dataframe.

# In[3]:


data_elements = download_data_element_templates()


# # Check for empty columns
# The following columns must contain text.

# In[4]:


check_empty_field("Variable / Field Name", data_elements)


# In[5]:


check_empty_field("Section Header", data_elements)


# In[6]:


check_empty_field("Field Type", data_elements)


# In[7]:


check_empty_field("Field Label", data_elements)


# In[8]:


check_empty_field("CDE Reference", data_elements)


# # Check for whitespace in Field Names
# Field Names should not contain whitespace.

# In[9]:


# data_elements


# In[10]:


check_whitespace("Variable / Field Name", data_elements)


# # Check Field Types
# Check that field types match the defined field types.

# In[11]:


check_field_types(data_elements)

