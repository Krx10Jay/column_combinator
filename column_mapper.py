import streamlit as st
import pandas as pd
from io import StringIO


def column_maper(col1: str, col2: str, dataframe=None, path=None, doc_type: str = "csv", ):#output_path: str = "new_csv.csv"):
    """
    Links each individual row of the one column to the all rows available in the 2nd choice column.
    
    Parameters:
        path (str): Path to the input CSV or Excel file.
        doc_type (str): Type of the document - "csv" or "excel".
        output_path (str): Path to save the output CSV file. Default is 'new_csv.csv'.
        col1 & col2 (str): The columns of interest in your file
    
    Returns:
        pd.DataFrame: DataFrame with each warehouse id mapped to all SKU ids.
    """
    
    if path:
        # Load the file based on the document type
        if doc_type == "csv":
        # path = file_as_str = StringIO(path.getvalue().decode("utf-8"))
            df = pd.read_csv(path)
        elif doc_type == "excel":
            df = pd.read_excel(path)
        else:
            st.error("Document type not supported. Please use 'csv' or 'excel'.")
            #return None
            print("doc_type not supported. Please use 'csv' or 'excel'.")
            return None
    else:
        df = dataframe
    # Identify the required columns in the file
    first_col = None
    second_col = None
    
    for col in df.columns:
        if col1.lower() in col.lower():
            first_col = col
        if col2.lower() in col.lower():
            second_col = col
    
    # Ensure both columns are found
    if not first_col or not second_col:
        st.error(f"Could not find appropriate columns for {col1} or {col2}.")
        print(f"Could not find appropriate columns for {col1} or {col2}.")
        return None
    
    # Drop NaN values
    col1_unique_entries = df[first_col].dropna().unique()  # Get unique entries
    col2_unique_entries = df[second_col].dropna().unique()  # Get unique entries
    
    # Create a new DataFrame mapping each entry in col2 to all entries in col1
    expanded_df = pd.DataFrame([(col2_entry, col1_entry) for col2_entry in col2_unique_entries for col1_entry in col1_unique_entries], 
                               columns=[f'{col2}', f'{col1}'])
    
    # Save the new DataFrame to CSV
    # expanded_df.to_csv(output_path, index=False)
    # expanded_df.head()
    # print(f"File saved as {output_path}")
    
    return expanded_df