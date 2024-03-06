#!/usr/bin/env python
# coding: utf-8

# # This notebook converts data dictionaries in the  RADx-rad Data Dictionary format to the harmonized RADx Data Dictionary format.

# ### Setup

# In[1]:


import os
import glob
import pandas as pd
import re
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


column_map = {"Variable / Field Name": "Id", "Field Label": "Label", "Section Header": "Section", "Field Type": "Datatype", "Unit": "Unit", "Units": "Unit", "Choices, Calculations, OR Slider Labels": "Enumeration", "Field Note": "Notes", "CDE Reference": "Provenance"}


# ## Download RADx-rad data elements

# In[6]:


file_path = "../data/dictionaries/RADx-rad_Dictionary_Template.csv"
data_elements = pd.read_csv(file_path, dtype=str)
data_elements.fillna("", inplace=True)


# In[7]:


check_required_fields(data_elements)


# In[8]:


### Check that field types match the expected types
check_field_types(data_elements)


# In[9]:


### Check that the following fields contain data, they cannot be empty.
check_empty_field("Variable / Field Name", data_elements)
check_empty_field("Section Header", data_elements)
check_empty_field("Field Type", data_elements)
check_empty_field("Field Label", data_elements)
check_empty_field("CDE Reference", data_elements)


# In[10]:


data_elements.rename(columns=column_map, inplace=True)


# In[11]:


data_elements.columns


# In[12]:


data_elements = data_elements[["Id", "Label", "Section", "Datatype", "Unit", "Enumeration", "Notes", "Provenance"]]


# In[13]:


data_elements.drop_duplicates(inplace=True)
print("Number of data elements", data_elements.shape[0])


# In[14]:


data_elements.head()


# In[15]:


data_elements["Datatype"].value_counts()


# In[16]:


def set_cardinality(data_type):
    if data_type == "list":
        return "multiple"
    else:
        return "single"


# In[17]:


def parse_integer_enums(enum):
    # Example: 1, Male | 2, Female | 3, Intersex | 4, None of these describe me
    matches = re.findall(enum_pattern_int, enum)
    parsed_data = [(int(match[0]), match[1].strip()) for match in matches]
    return parsed_data


# In[18]:


def parse_string_enums(enum):
    # Example: AL, Alabama | AK, Alaska | AS, American Samoa
    matches = re.findall(enum_pattern_str, enum)
    parsed_data = [(match[0].strip(), match[1].strip()) for match in matches]
    return parsed_data


# In[19]:


def convert_data_type(row):
    data_type = row["Datatype"]
    enum = row["Enumeration"]
    
    parsed_data = parse_integer_enums(enum)
    if len(parsed_data) > 0:
        return "integer"

    parsed_data = parse_string_enums(enum)
    if len(parsed_data) > 0:
        return "string"
    
    # find enumeration with text values
    if "|" in enum:
        return "string"
    
    if data_type in ["text", "list", "url", "sequence", "category", "yesno", "radio", "dropdown", "checkbox", "zipcode"]:
        return "string"
    
    return data_type  


# In[20]:


def convert_enumeration(enum):
    
    # parse integer and string encoded enumerations
    parsed_data = parse_integer_enums(enum) + parse_string_enums(enum)
    
    if parsed_data and len(parsed_data) > 0:
        enums = []
        for value, label in parsed_data:
            enums.append(f'"{value}"=[{label}]')
            
        return " | ".join(enums)
    
    # parse simple value enumerations. Example: IgA | IgG | IgM
    if "|" in enum:
        enums = []
        values = enum.split("|")
        for value in values:
            value = value.strip()
            enums.append(f'"{value}"=[{value}]')

        return " | ".join(enums)
            
    
    return ""


# In[21]:


def split_provenance(provenance):
    if len(provenance) > 0:
        provenance, sep, see_also = provenance.partition("|")
        return (provenance, see_also)
    else:
        return ("", "")


# In[22]:


# The CDE Reference field was renamed Provenance. Here we split the Provenance (first part of the |-separated list), for the SeeAlso (second part of the list)
data_elements[["Provenance", "SeeAlso"]] = data_elements["Provenance"].str.split('|', n = 1, expand=True)
data_elements["SeeAlso"].fillna("", inplace=True)

data_elements["Cardinality"] = data_elements["Datatype"].apply(set_cardinality)
data_elements["Datatype"] = data_elements.apply(convert_data_type, axis=1)
data_elements["Enumeration"] = data_elements["Enumeration"].apply(convert_enumeration)


# In[23]:


#data_elements.drop(1, axis=0, inplace=True)


# In[24]:


data_elements.columns


# In[25]:


data_elements = data_elements[["Id", "Label", "Section", "Cardinality", "Datatype", "Unit", "Enumeration", "Notes", "Provenance", "SeeAlso"]]


# In[26]:


data_elements.head(1000)


# In[27]:


data_elements.to_csv("RADx-rad_harmonized_dict_2024-03-05.csv", index=False)

