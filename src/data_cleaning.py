"""
Data cleaning and preprocessing module.
Handles missing values, duplicates, outliers, and categorical encoding.
"""
import pandas as pd
import numpy as np
import os

# Import the data loader function
from data_loader import load_data

def handle_missing_values(df):
    """
    Fills missing values in the dataset.
    Uses median imputation for numerical columns like Income and Credit_Score 
    because median is robust to outliers compared to the mean.
    """
    df_clean = df.copy()
    
    # We use median because income and credit scores can be skewed
    if 'Income' in df_clean.columns:
        df_clean['Income'] = df_clean['Income'].fillna(df_clean['Income'].median())
        
    if 'Credit_Score' in df_clean.columns:
        df_clean['Credit_Score'] = df_clean['Credit_Score'].fillna(df_clean['Credit_Score'].median())
        
    return df_clean

def remove_duplicates(df):
    """
    Detects and removes duplicate rows safely.
    Reports the number of duplicates removed.
    """
    duplicates_count = df.duplicated().sum()
    if duplicates_count > 0:
        print(f"[*] Found {duplicates_count} duplicate rows. Removing them...")
        df_clean = df.drop_duplicates(keep='first').copy()
    else:
        print("[*] No duplicate rows found.")
        df_clean = df.copy()
        
    return df_clean

def handle_outliers(df):
    """
    Identifies and handles potential outliers using the IQR (Interquartile Range) method.
    We cap extreme values instead of deleting them to avoid losing valid high-income
    or high-loan applicants.
    """
    df_clean = df.copy()
    numerical_cols = ['Income', 'Loan_Amount']
    
    for col in numerical_cols:
        if col in df_clean.columns:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Capping outliers to upper and lower bounds rather than dropping them
            df_clean[col] = np.where(df_clean[col] > upper_bound, upper_bound, df_clean[col])
            df_clean[col] = np.where(df_clean[col] < lower_bound, lower_bound, df_clean[col])
            
    return df_clean

def encode_categorical_data(df):
    """
    Converts categorical text variables into machine-learning-compatible numerical representations.
    Uses One-Hot Encoding for Employment_Status.
    Leaves Risk_Status untouched for later ML label processing.
    """
    df_clean = df.copy()
    
    if 'Employment_Status' in df_clean.columns:
        # Use pandas get_dummies for one-hot encoding
        df_clean = pd.get_dummies(df_clean, columns=['Employment_Status'], drop_first=False)
        
        # Convert the resulting boolean columns to integers (0 and 1) for better compatibility
        # (Only targeting the newly created Employment_Status columns)
        dummy_cols = [col for col in df_clean.columns if col.startswith('Employment_Status_')]
        df_clean[dummy_cols] = df_clean[dummy_cols].astype(int)
        
    return df_clean

def clean_data(df):
    """
    Executes the full cleaning pipeline sequentially:
    Missing Values -> Duplicates -> Outliers -> Categorical Encoding
    """
    print("--- Starting Data Cleaning Pipeline ---")
    
    # 1. Missing Values
    print("\n[1/4] Handling missing values...")
    df = handle_missing_values(df)
    
    # 2. Duplicate Removal
    print("[2/4] Removing duplicates...")
    df = remove_duplicates(df)
    
    # 3. Outlier Handling
    print("[3/4] Handling outliers (Capping extreme values)...")
    df = handle_outliers(df)
    
    # 4. Categorical Encoding
    print("[4/4] Encoding categorical variables...")
    df = encode_categorical_data(df)
    
    print("\n--- Data Cleaning Pipeline Complete ---")
    return df

if __name__ == "__main__":
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_path = os.path.join(base_dir, 'data', 'loan_data.csv')
    output_path = os.path.join(base_dir, 'data', 'cleaned_loan_data.csv')
    
    try:
        # Load Raw Data
        raw_df = load_data(input_path)
        
        if raw_df is not None:
            print("\n================ BEFORE CLEANING ================")
            print(f"Original Shape: {raw_df.shape}")
            print("\nMissing values before cleaning:")
            print(raw_df.isnull().sum())
            
            # Execute Pipeline
            print("\n================ EXECUTING PIPELINE ================\n")
            cleaned_df = clean_data(raw_df)
            
            print("\n================ AFTER CLEANING ================")
            print(f"Final Shape: {cleaned_df.shape}")
            print("\nMissing values after cleaning:")
            print(cleaned_df.isnull().sum())
            
            print("\nFinal Column Names:")
            print(list(cleaned_df.columns))
            
            print("\nFinal Data Types:")
            print(cleaned_df.dtypes)
            
            # Save Cleaned Data
            cleaned_df.to_csv(output_path, index=False)
            print(f"\n[Success] Cleaned dataset saved to: {output_path}")
            
    except Exception as e:
        print(f"Error during data cleaning pipeline execution: {e}")
