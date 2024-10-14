To update RADx-rad Data Dictionaries:

1. Update the data dictionary Google Sheets in [RADx-rad Google Drive](https://drive.google.com/drive/folders/1XVCfnA8fSwrlozXOxiEq1LA0qM8QzU4e?usp=sharing)
2. Run CheckDataElementTemplates.ipynb
   * Check notebook for error messages
3. Run ConcatenateRADx-radDicts.ipynb
   * This notebook concatenates the Google Sheets into the file RADx-rad_legacy_dict_YYYY-MM-DD.csv
4. Run DictConverter.ipynb
   * This notebook converts Tier 2 data elements to the RADx Global Codebook format: RADx-rad_tier2_dict_YYYY-MM-DD.csv
5. Run AssignOntologyMapping.ipynb
   * Add ontology terms to the  RADx-rad_tier2_dict_YYYY-MM-DD.csv file.
   * This notebook takes the onology mappings from ../ontology/ontology_mappings_2024-10-08.csv and maps them to the Tier2 data elements.
   * If new data elements are added, the ontology mapping file needs to be updated.