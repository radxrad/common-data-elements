#!/usr/bin/env python
# coding: utf-8

# In[ ]:


csv_dir = ""
excel_file = ""
excel_dir = ""
google_doc_id = ""


# ### Specify path to example data files
# Specify either a csv directory name, an excel file name, or a Google document id to an excel file. See examples below

# #### For csv files specify the path to the directory that contains the csv files

# In[ ]:


# csv_dir = "../data/path_to_csv_dir"


# #### For an Excel (.xlsx) file specify the path to the file with multiple sheets

# In[ ]:


# excel_file = "../data/path_to_excel_file"


# In[ ]:


#### For a directory of Excel files


# In[ ]:


# excel_dir = "../data/path_to_excel_dir"


# #### For an Excel file in Google Sheets (as Excel file) specify the google_doc_id and a local data directory to store the results.

# In[ ]:


# Example of google doc id
# google_doc_id = "10SOtm2860aE7vTpgJaudERa0KIxdEvwx"
# https://docs.google.com/spreadsheets/d/10SOtm2860aE7vTpgJaudERa0KIxdEvwx/edit#gid=1722872060


# In[ ]:


# google_doc_id = "10SOtm2860aE7vTpgJaudERa0KIxdEvwx"
# data_dir = "../data/path_to_result_files


# ---

# ### Setup

# In[ ]:


import os
import glob
import pandas as pd
from utils import *


# In[ ]:


pd.options.display.max_rows = None  # display all rows
pd.options.display.max_columns = None  # display all columns
pd.set_option('display.max_colwidth', None) # don't truncate wide columns


# ## Collect field names from the example data files

# In[ ]:


if csv_dir:
    column_names, directory, file_name = download_csv_dir_and_parse_column_names(csv_dir)
if excel_dir:
    print(f"Processing {excel_dir}")
    column_names, directory, file_name = download_excel_dir_and_parse_column_names(excel_dir)
if excel_file:
    print(f"Processing {excel_file}")
    column_names, directory, file_name = download_excel_and_parse_column_names(excel_file)
if google_doc_id:
    column_names, directory, file_name = download_google_sheet_excel_and_parse_column_names(google_doc_id, data_dir)
    


# In[ ]:


print(f"Number of column names: {column_names.shape[0]}")
column_names


# ## Parse RADx-rad Data Dictionaries

# In[ ]:


data_elements = download_data_element_templates()
data_elements["template"].value_counts()


# In[ ]:


print(f"Total Data Elements:      {data_elements.shape[0]}")


# ## Check for presence of Minimum CDEs

# In[ ]:


min_cde_matches = match_minimum_cdes(data_elements, column_names)
print(f"Number of Min CDE matches: {min_cde_matches.shape[0]} out of 46")
min_cde_matches


# ## Create Data Dictionary

# In[ ]:


data_dict = data_elements.merge(column_names, on="Variable / Field Name")
data_dict.drop(columns=["template", "File Name"], inplace=True)
data_dict.drop_duplicates(subset=["Variable / Field Name"], keep="first", inplace=True)
print(f"Number of matched data elements: {data_dict.shape[0]}")


# #### Add all minimum CDEs
# They are required even if not all or any minimum CDEs are in the data files.

# In[ ]:


min_cdes = data_elements[data_elements["template"] == "Minimum CDEs"].copy()
min_cdes.drop(columns=["template"], inplace=True)
data_dict = pd.concat([min_cdes, data_dict])
data_dict.drop_duplicates(subset=["Variable / Field Name"], keep="first", inplace=True)


# In[ ]:


data_dict.head()


# In[ ]:


dict_file_name = os.path.join(directory, f"{file_name}_DICT.csv")
print(f"Data dictionary saved to: {dict_file_name}")
data_dict.to_csv(dict_file_name, index=False)


# ## Create table of undefined data elements

# In[ ]:


undefined = get_undefined_data_elements(data_elements, column_names)
print(f"Number of undefined data elements: {undefined.shape[0]}")


# In[ ]:


undefined


# ## Create data elements for units

# In[ ]:


units = undefined[undefined["Variable / Field Name"].str.endswith("_unit")].copy()


# In[ ]:


units["Section Header"] = "Technology Metadata"
units["Field Type"] = "text"
units["Choices, Calculations, OR Slider Labels"] = ""
units["Field Note"] = ""
units["Text Validation Type OR Show Slider Number"] = ""
units["Text Validation Min"] = ""
units["Text Validation Max"] = ""
units["Branching Logic (Show field only if...)"] = ""
units["Unit"] = ""
units["CDE Reference"] = "RADx-rad DCC"
units = units[["Variable / Field Name", "Section Header", "Field Type", "Field Label", 
             "Choices, Calculations, OR Slider Labels", "Field Note", 
             "Text Validation Type OR Show Slider Number", "Text Validation Min",
             "Text Validation Max", "Branching Logic (Show field only if...)",
             "Unit","CDE Reference"]]
units


# In[ ]:


units_file_name = os.path.join(directory, f"{file_name}_UNITS.csv")
print(f"Units data elements saved to: {units_file_name}")
units.to_csv(units_file_name, index=False)


# In[ ]:


undefined = undefined[["Variable / Field Name", "Field Label"]]
undefined["Field Type"] = "Field Type"
undefined = undefined[undefined["Field Label"] == ""]


# In[ ]:


undef_file_name = os.path.join(directory, f"{file_name}_UNDEFINED.csv")
print(f"Undefined data elements saved to: {undef_file_name}")
undefined.to_csv(undef_file_name, index=False)


# In[ ]:





# In[ ]:




