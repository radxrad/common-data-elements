#!/usr/bin/env python
# coding: utf-8

# # This notebook converts data dictionaries in the  RADx-rad Data Dictionary format to the harmonized RADx Data Dictionary format.

# ### Setup

# In[1]:


import os
import glob
import pandas as pd
import re
import traceback
import sys
from utils import *


# In[2]:


pd.options.display.max_rows = None  # display all rows
pd.options.display.max_columns = None  # display all columns
pd.set_option('display.max_colwidth', None) # don't truncate wide columns


# In[3]:


enum_pattern_int = r"(\d+),\s*([^|]+)\s*(?:\||$)" # Example: 1, Male | 2, Female | 3, Intersex | 4, None of these describe me
enum_pattern_str = r"([A-Z]+),\s*([^|]+)\s*(?:\||$)" # Example: AL, Alabama | AK, Alaska | AS, American Samoa


# In[4]:


required_fields = {"Variable / Field Name", "Field Label", "Section Header", "Field Type", "Unit", "Choices, Calculations, OR Slider Labels", "Field Note", "CDE Reference"}


# In[5]:


column_map = {"Variable / Field Name": "Id", "Field Label": "Label", "Section Header": "Section", "Field Type": "Datatype", "Unit": "Unit", "Choices, Calculations, OR Slider Labels": "Enumeration", "Field Note": "Notes"}


# ## Download RADx-rad data elements

# In[6]:


# remove empty columns: https://gist.github.com/aculich/fb2769414850d20911eb
# https://www.jitsejan.com/find-and-delete-empty-columns-pandas-dataframe


# In[7]:


files = glob.glob("../data/radx-rad-dictionaries/*.csv")


# In[8]:


error_list = []


# In[9]:


def count_empty_cols(data_elements):
    cols = list(data_elements.columns)
    print("all cols:", cols)
    unnamed_cols = list(filter(lambda x: x.startswith("Unnamed"), cols))
    print("unnamed cols:", unnamed_cols)
    return len(unnamed_cols)


# In[10]:


for filename in files:
    print("parsing: ", filename)
    parse_error = False
    missing_fields = ""
    empty_fields = []
    invalid_field_types = ""
    empty_cols = 0
    empty_rows = 0
    utf8_encoded = True

    # check if files is utf8 encoded
    try:
        data_elements = pd.read_csv(filename, dtype=str, encoding='utf8')
    except Exception:
        utf8_encoded = False

    try:
        #data_elements = pd.read_csv(filename, dtype=str, encoding="ISO-8859-1", on_bad_lines="skip", encoding_errors="ignore")
        data_elements = pd.read_csv(filename, dtype=str, encoding="ISO-8859-1")
    except Exception:
        parse_error = True
        print("ERROR: parsing csv file")
        print(traceback.format_exc())

    if not parse_error:
        # Some of the original wastewater dictionaries have a Units field (inherited from CDC).
        # The wastewater directory was updated to "Unit", since it doesn't make sense for a data elements have multiple units.
        data_elements.rename(columns={"Units": "Unit"}, inplace=True)
        all_rows = data_elements.shape[0]
        data_elements = data_elements.dropna(axis=0, how='all')
        empty_rows = all_rows - data_elements.shape[0]
        data_elements.fillna("", inplace=True)
        print("Columns:", data_elements.columns)
    
        # Run data checks
        missing_fields = check_required_fields(data_elements)
        empty_cols = count_empty_cols(data_elements)
    
        # Check that the following fields contain data, they cannot be empty.
        if check_empty_field("Variable / Field Name", data_elements):
            empty_fields.append("Variable / Field Name")
        if check_empty_field("Section Header", data_elements):
            empty_fields.append("Section Header")
        if check_empty_field("Field Type", data_elements):
            empty_fields.append("Field Type")
        if check_empty_field("Field Label", data_elements):
            empty_fields.append("Field Label") 
        # if check_empty_field("CDE Reference", data_elements):
        #     empty_fields.append("CDE Reference") 
    
        # Check that field types match the expected types
        if not check_empty_field("Field Type", data_elements):
            invalid_field_types = check_field_types(data_elements)
    
    # Record results
    if len(empty_fields) == 0:
        empty_fields = ""
            
    error_list.append({"filename": filename.split("/")[-1],
                       "utf8_encoded": utf8_encoded,
                       "parse_error": parse_error,
                       "missing_fields": missing_fields,
                       "empty_fields": empty_fields,
                       "invalid_field_types": invalid_field_types,
                       "empty_cols": empty_cols,
                       "empty_rows": empty_rows})


# In[ ]:


errors = pd.DataFrame(error_list)
errors.head(100)


# In[ ]:


errors.to_csv("radx_dict_errors_2023-08-19.csv", index=False)


# In[ ]:


# Files with parsing errors


# In[ ]:


parse_errors = errors[errors["parse_error"] == True]


# In[ ]:


parse_errors.shape[0]


# In[ ]:




