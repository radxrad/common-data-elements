#!/usr/bin/python3

required_fields = {"Variable / Field Name", "Field Label", "Section Header", "Field Type", "Unit", "Choices, Calculations, OR Slider Labels", "Field Note", "CDE Reference"}

def download_data_element_templates():
    import pandas as pd

    # Parse minimum common data elements for RADx-rad projects
    min_cdes = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/1LaGrgk1N8B2EclU1w2bduqHJ6p1pN4Mq/export?format=csv",
        keep_default_na=False,
    )
    min_cdes["template"] = "Minimum CDEs"
    #print("Minimum CDEs", min_cdes.shape)

    # Parse technology description data elements
    technology_description = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/1DETG54TF83vPhvrW-MLN5p9QJiMlVA3j/export?format=csv",
        keep_default_na=False,
    )
    technology_description["template"] = "Technology Description"
    #print("Technology Description", technology_description.shape)

    # Parse data elements for PCR data
    pcr = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/1iJo9uu3FcvBngxrSM0JCqmXDNghMMxcr/export?format=csv",
        keep_default_na=False,
    )
    pcr["template"] = "PCR"
    #print("PCR", pcr.shape)

    # Parse data elements for spiked samples
    spiked_samples = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/13eew7mJOp0fbh_hs8SbUGHtnZvZ7giqp/export?format=csv",
        keep_default_na=False,
    )
    spiked_samples["template"] = "Spiked Samples"
    #print("Spiked Samples", spiked_samples.shape)

    # Parse data elements for clinical samples
    clinical_samples = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/1uNN9MaEjgkhHX4rY-HujbzltlilY_NCN/export?format=csv",
        keep_default_na=False,
    )
    clinical_samples["template"] = "Clinical Samples"
    #print("Clinical Samples", clinical_samples.shape)

    # Parse data elements for wastewater projects
    waste_water = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/1Si4YHCZ0Hh2EFM--VMFaDWi0SAcGl96c-qes82nV2tA/export?format=csv",
        keep_default_na=False,
    )
    waste_water["template"] = "Waste Water"
    #print("Waste Water", waste_water.shape)

    # Parse data elements for test results
    test_results = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/1m8dkOrerxwaT8xOUWwR5ZE0VPeVvsu04/export?format=csv",
        keep_default_na=False,
    )
    test_results["template"] = "Test Results"
    #print("Test Results", test_results.shape)

    # Parse data elements for performance metrics
    # https://docs.google.com/spreadsheets/d/1yJG7Vt0AmXQkxForxsezgT-9EDRZJwnH/edit?usp=sharing&ouid=112820493940716707493&rtpof=true&sd=true
    performance_metrics = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/1yJG7Vt0AmXQkxForxsezgT-9EDRZJwnH/export?format=csv",
        keep_default_na=False,
    )
    
    # performance_metrics = pd.read_csv("../RADx-rad_Performance_Metrics_Data_Element_Template_v000.xlsx - RADxrad_Data_Element_Template_v.csv")
    performance_metrics["template"] = "Performance Metrics"
    #print("Performance Metrics", performance_metrics.shape)

    # Concatenate all data elements into a single dataframe
    data_elements = pd.concat(
        [
            min_cdes,
            technology_description,
            pcr,
            spiked_samples,
            clinical_samples,
            waste_water,
            test_results,
            performance_metrics,
        ]
    )

    return data_elements


def match_minimum_cdes(data_elements, column_names):
    min_cdes = data_elements[data_elements["template"] == "Minimum CDEs"].copy()
    min_cdes.drop(columns=["template"], inplace=True)
    min_cde_matches = min_cdes.merge(column_names, on="Variable / Field Name")
    min_cde_matches.drop_duplicates(subset=["Variable / Field Name"], inplace=True)

    return min_cde_matches


def add_field_label(field_name):
    if field_name.endswith("_unit"):
        field_label = "Unit of " + field_name.split("_unit")[0]
    else:
        field_label = ""

    return field_label


def get_undefined_data_elements(data_elements, column_names):
    undefined = column_names.merge(
        data_elements, on="Variable / Field Name", how="left", indicator=True
    )
    undefined = undefined.query("_merge == 'left_only'")
    undefined = undefined[["Variable / Field Name", "File Name"]]
    # undefined["Variable / Field Name"] = undefined["Variable / Field Name"].str.strip()
    undefined.drop_duplicates(
        subset="Variable / Field Name", keep="first", inplace=True
    )
    undefined["Field Label"] = undefined["Variable / Field Name"].apply(add_field_label)

    return undefined


def check_empty_field(field_name, data_elements):
    fields = set(data_elements.columns)
    if field_name in fields:
        empty_fields = data_elements[data_elements[field_name] == ""]
        if empty_fields.shape[0] == 0:
            return False
        else:
            print(f"ERROR: Data missing in field: {field_name}")
            return True
    else:
        print(f"ERROR: Data field missing: {field_name}")
        return True


def check_whitespace(field_name, data_elements):
    whitespace = data_elements[data_elements[field_name].str.contains(" ")]
    if whitespace.shape[0] == 0:
        print(f"{field_name}: ok")
        return

    print(f"Data elements with whitespace in {field_name}:")
    return whitespace


def check_field_types(data_elements):
    allowed_types = {
        "text",
        "integer",
        "float",
        "date",
        "time",
        "timezone",
        "zipcode",
        "url",
        "sequence",
        "list",
        "category",
        "yesno",
        "radio",
        "dropdown",
        "checkbox",
    }
    field_types = set(data_elements["Field Type"].unique())
    invalid_field_types = field_types - allowed_types

    if len(invalid_field_types) > 0:
        print(f"ERROR: Invalid Field Type: {invalid_field_types}")
        print(f"INFO : Allowed Field Types: {allowed_types}")
        
    return invalid_field_types


def check_required_fields(data_elements):
    fields = set(data_elements.columns)
    missing_fields = required_fields - fields
    if len(missing_fields) > 0:
        print(f"ERROR: Data field missing: {missing_fields}")
        print(f"INFO : Extra fields: {fields - required_fields}")
    return missing_fields
        

def download_excel_and_parse_column_names(excel_file_name):
    import pandas as pd
    import os
    
    directory, file_path = os.path.split(excel_file_name)
    file_name, extension = os.path.splitext(file_path)

    # download all sheets into a dictionary
    data_sheets = pd.read_excel(excel_file_name, sheet_name=None)

    # extract column and sheet names
    records = []
    for sheet in data_sheets.items():
        columns = sheet[1].columns
        sheet_name = sheet[0]
        print(f"{excel_file_name} - {sheet_name}")
        for column in columns:
            records.append([column, sheet_name])

    # create a dataframe with the column and sheet names
    column_names = pd.DataFrame(records)
    column_names.columns = ["Variable / Field Name", "File Name"]

    return column_names, directory, file_name


def download_google_sheet_excel_and_parse_column_names(google_doc_id, data_dir):
    import pandas as pd
    
    # download all sheets into a dictionary
    data_sheets =  pd.read_excel(f"https://docs.google.com/spreadsheets/d/{google_doc_id}/export?format=xlsx", sheet_name=None)

    # extract column and sheet names
    records = []
    for sheet in data_sheets.items():
        columns = sheet[1].columns
        sheet_name = sheet[0]
        print(f"{google_doc_id} - {sheet_name}")
        for column in columns:
            records.append([column, sheet_name])

    # create a dataframe with the column and sheet names
    column_names = pd.DataFrame(records)
    column_names.columns = ["Variable / Field Name", "File Name"]

    return column_names, data_dir, google_doc_id


def download_excel_dir_and_parse_column_names(excel_dir_path_name):
    import os
    import glob
    import pandas as pd
    
    directory = excel_dir_path_name
    file_name = directory.rsplit("/", 1)[1]
    
    # extract column names from all excel files
    records = []
    # accept both .xls and .xlsx extensions
    for path in glob.glob(os.path.join(excel_dir_path_name, "*xls*")):
        print(path)
        columns = list(pd.read_excel(path).columns)
        print(os.path.split(path)[1], columns)
        
        for column in columns:
            records.append([column, os.path.split(path)[1]])

    # create a dataframe with the column and sheet names
    column_names = pd.DataFrame(records)
    column_names.columns = ["Variable / Field Name", "File Name"]
    
    return column_names, directory, file_name


def download_csv_dir_and_parse_column_names(csv_dir_path_name):
    import os
    import glob
    import pandas as pd
    
    directory = csv_dir_path_name
    file_name = directory.rsplit("/", 1)[1]
    
    # extract column names from all csv files
    records = []
    for path in glob.glob(os.path.join(csv_dir_path_name, "*.csv")):
        # ignore existing output files
        if path.endswith("_DICT.csv") or path.endswith("_UNDEFINED.csv") or path.endswith("_UNITS.csv"):
            continue
            
        print(path)
        columns = list(pd.read_csv(path).columns)
        print(os.path.split(path)[1], columns)
        
        for column in columns:
            records.append([column, os.path.split(path)[1]])

    # create a dataframe with the column and sheet names
    column_names = pd.DataFrame(records)
    column_names.columns = ["Variable / Field Name", "File Name"]
    
    return column_names, directory, file_name
    