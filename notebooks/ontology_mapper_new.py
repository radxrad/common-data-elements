"""
This module provides functions to map terms to concepts in an ontology.

Author: Peter W Rose (pwrose@ucsd.edu)
Created: 2024-03-03
"""
import os
import requests
from dotenv import load_dotenv
import pandas as pd
import inflection
import time

CHUNK_SIZE = 250

def map_ontology(apikey, keywords, ontologies=[], topn=1):
    """
    Map terms from a DataFrame column to concepts in an ontology.

    Parameters
    ----------
    df (pandas.DataFrame): The DataFrame containing the data to be mapped.
    input_col (str): The name of the column in `df` containing terms to be mapped.
    output_col (str): The name of the column in `df` to store the mapped ontology concepts.
    ontology (Ontology): Name of the ontology

    Returns
    -------
    pandas.DataFrame: The DataFrame with mapped ontology concepts in the `output_col` column.

    Notes
    -----
    Make sure to set the `BIOPORTAL_API_KEY` variable in the .env file.
    Create a BioPortal account to get an API key.

    Example
    -------
    >>> import os
    >>> import pandas as pd
    >>> from dotenv import load_dotenv
    >>> import ontology_mapper
    >>>
    >>> # get BioPortal API key
    >>> load_dotenv(<path to .env file>)
    >>> apikey = os.getenv("BIOPORTAL_API_KEY")
    >>>
    >>> # Sample DataFrame (may contain other columns)
    >>> df = pd.DataFrame({"terms": ["liver", "brain", "zygote"]})
    >>> ontologies = ["UBERON"]
    topn = 1
    >>> mapped_df = ontology_mapper.map_ontology(df, "terms", "mapped_concepts", ontologies, topn, apikey)
    >>> print(mapped_df)
            terms     mapped_concepts
    0       liver     UBERON:0002107
    1       brain     UBERON:0000955
    2      zygote     CL:0010017
    
    """

    df = pd.DataFrame(keywords)
    df.columns = ["keyword"]

    df["matched_keyword"] = df["keyword"].str.lower()

    # If a keyword is plural, add a signular form.
    # Most keywords in ontologies are in singular form
    df = add_singular_rows(df)

    df = mapper(df, ontologies, apikey)
    
    # TODO Where do the duplicates originate from??
    df.drop_duplicates(inplace=True)

    # convert URI to CURIE
    df["class"] = df["class"].str.replace("http://purl.obolibrary.org/obo/", "", regex=False)
    df["class"] = df["class"].str.replace("_", ":", regex=False)

    df.drop(columns="matched_keyword", inplace=True)

    df = df.groupby("keyword").head(topn)
    
    return df
    

def add_singular_rows(df):
    new_rows = []
    
    for idx, row in df.iterrows():
        singular_form = inflection.singularize(row["matched_keyword"])
        if singular_form != row['matched_keyword']:
            new_rows.append({"keyword": row["keyword"], "matched_keyword": singular_form})
    
    # Create a DataFrame with singular forms and append to original dataframe
    if new_rows:
        new_df = pd.DataFrame(new_rows)
        df = pd.concat([df, new_df], ignore_index=True)
    
    return df


def mapper(df, ontologies, apikey):
    terms = list(df["matched_keyword"].unique())
    chunks = create_chunks(terms, CHUNK_SIZE)
    
    matched_chunks = []

    for chunk in chunks:
        time.sleep(2)
        matches = match_terms(terms, ontologies, apikey)
        if matches is None or len(matches) == 0:
             continue

        matches[["pref_label", "synonyms", "definition"]] = matches["url"].apply(
                lambda x: pd.Series(get_details(x, apikey))
        )
        matched_chunks.append(matches)

    
    all_matches = pd.concat(matched_chunks)

    # Keep only a subset of the data
    all_matches = all_matches[["matched_keyword","pref_label", "synonyms", "definition", "class"]].copy()                                                                                                                
    df = df.merge(all_matches, on="matched_keyword", how="left")
    return df


def match_terms(terms, ontologies, apikey):
    data_all = get_recommendation(terms, ontologies, apikey)
        
    if not data_all or len(data_all) == 0:
        return None

    matches = []
    for data in data_all:
        match = pd.json_normalize(data["coverageResult"], record_path="annotations", errors="ignore")
        match.rename(columns={"text": "matched_keyword", "annotatedClass.@id": "class", "annotatedClass.links.self": "url"}, inplace=True)
        matches.append(match)

    matches_df = pd.concat(matches)
    matches_df["matched_keyword"] = matches_df["matched_keyword"].str.lower()
    
    return matches_df[["matched_keyword", "class", "url"]].copy()


def get_details(url, apikey):
    empty_return = ("", "", "")
    if url == "":
        return empty_return
        
    params = {"apikey": apikey}
    
    # Make the GET request to the API
    response = requests.get(url, params=params)
    time.sleep(1)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract the required fields
        prefLabel = data.get('prefLabel', '')
        synonyms = tuple(data.get('synonym', []))
        definition = tuple(data.get('definition', []))

        return (prefLabel, synonyms, definition)
    else:
        print(f"ERROR: Unable to fetch data (status code {response.status_code})")
        return empty_return


def create_chunks(data, chunk_size):
    """
    Split a list into smaller chunks of a specified size.

    Args:
        data (list): The input list to be divided into chunks.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        list: A list of chunks, where each chunk is a sublist of 'data'.

    Example:
        >>> data = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> chunk_size = 3
        >>> create_chunks(data, chunk_size)
        [[1, 2, 3], [4, 5, 6], [7, 8]]
    """
    # split list into chunks of max size: chunk_size
    # return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def get_recommendation(terms, ontologies, apikey):
    """
    Get ontology recommendations based on input terms.

    Parameters
    ----------
    terms : str
        Input terms for which ontology recommendations are needed.
        Can be a single term or a list of terms separated by comma.
    ontologies : str
        Ontologies to consider for recommendations.
        Can be a single ontology or a list of ontologies separated by comma.
    apikey : str
        BipPortal API key.

    Returns
    -------
    dict
        A dictionary containing ontology recommendations based on the input terms.

    Raises
    ------
    requests.exceptions.HTTPError
        If the HTTP request to the recommender API fails (e.g., invalid API key, server error).
    requests.exceptions.RequestException
        If there is a general request exception while communicating with the recommender API.

    Notes
    -----
    This function sends a POST request to the BioPortal Recommender API
    (https://bioportal.bioontology.org/recommender) to get ontology recommendations
    based on the provided input terms and ontologies.

    The API requires authentication via an API key, and the function uses the provided API key
    for authorization. Make sure to set the 'APIKEY' variable with a valid BioPortal API key
    before calling this function. Create a BioPortal account to get an API key.

    Example
    -------
    >>> APIKEY = "your_api_key"
    >>> terms = ["apple], "orange"]
    >>> ontologies = ["FOODON"]
    >>> recommendations = get_recommendation(terms, ontologies, apikey)
    """
    URL = "https://data.bioontology.org/recommender"
    HEADERS = {"accept": "application/json", "Authorization": f"apikey token={apikey}"}

    # create input parameters for API call
    terms_string = ",".join(terms)
    ontology_string = ",".join(ontologies)

    if ontologies and len(ontologies) > 0:
        params = {"input": terms_string, "input_type": "2", "ontologies": ontologies}
    else:
        params = {"input": terms_string, "input_type": "2"}

    try:
        response = requests.post(URL, headers=HEADERS, json=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as error:
        print(f"ERROR: {error}")
        raise
    except requests.exceptions.RequestException as error:
        print(f"ERROR: {error}")
        raise

    return data
