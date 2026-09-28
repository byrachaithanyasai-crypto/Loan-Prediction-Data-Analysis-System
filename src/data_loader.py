"""
Data loading module for the Loan Prediction Data Analysis System System.
Responsible for reading the dataset safely and providing basic information.
"""
import pandas as pd
import os

def load_data(file_path):
    """
    Loads the loan dataset from the specified path into a Pandas DataFrame.
    
    Args:
        file_path (str): The relative or absolute path to the CSV dataset.
        
    Returns:
        pd.DataFrame or None: Returns the DataFrame if successful, else None.
    """
    if not os.path.exists(file_path):
        print(f"Error: Dataset not found at '{file_path}'. Please ensure the file exists.")
        return None
    
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded dataset from '{file_path}'")
        return df
    except Exception as e:
        print(f"An unexpected error occurred while loading the dataset: {e}")
        return None

def get_basic_info(df):
    """
    Displays basic structural and statistical information about the dataset.
    
    Args:
        df (pd.DataFrame): The dataset to inspect.
    """
    if df is None or df.empty:
        print("No data available to display.")
        return
        
    print("\n--- Dataset Basic Information ---")
    
    # Display shape
    rows, cols = df.shape
    print(f"Shape: {rows} rows, {cols} columns")
    
    # Display column names
    print(f"\nColumn Names:\n{list(df.columns)}")
    
    # Display first 5 rows
    print("\nFirst 5 Rows:")
    print(df.head())
    
    # Display data types
    print("\nData Types:")
    print(df.dtypes)
    
    # Display missing-value counts
    print("\nMissing Values Count:")
    print(df.isnull().sum())

if __name__ == "__main__":
    # Test the module directly
    # Ensure the path is correct relative to where the script is executed
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'loan_data.csv')
    
    print("Testing data_loader module...")
    df = load_data(dataset_path)
    get_basic_info(df)
