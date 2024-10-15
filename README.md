# RADx-rad Data Dictionaries

The `cdes` directory contains harmonized Common Data Elements (CDEs) for the [RADx-rad project](https://www.radxrad.org/).

The data elements define the columns in the data files within the [NIH RADx Data Hub](https://radxdatahub.nih.gov/). An overview of the RADx-rad project data is [available](https://www.youtube.com/watch?v=97DsbJCvktE).

Data elements are provided in two formats:

1. **[RADx format](https://github.com/bmir-radx/radx-data-dictionary-specification)**: A standardized format common to all RADx projects (RADx-DHT, RADx-rad, RADx-Tech, RADx-UP) within the NIH RADx Data Hub.

2. **[RADx-rad format](cdes/RADx-rad_Data_Dictionary_Guide_v000.pdf)**: The original format in which data elements were collected by the RADx Data Coordination Center.


**RADx format Data Dictionaries**
| File name | Description |
|------------------------------------|------------------------------------|
| RADx-global_tier1_dict_YYYY-MM-DD.csv | RADx global project data elements (Tier1 for transformcopy file) |
| RADx-rad_tier1_dict_YYYY-MM-DD.csv | RADx-rad project minimum common data elements for patient data (Tier1 for origcopy files) |
| RADx-rad_tier2_dict_YYYY-MM-DD.csv | RADx-rad project specific data elements (Tier2 for origcopy files) |


**RADx-rad format Data Dictionaries**
| File name | Description |
|------------------------------------|---------------------------------------------|
| RADx-rad_legacy_dict_YYYY-MM-DD.csv | RADx-rad Tier1 and Tier 2 data elements in legacy format |