"""
Exploratory Data Analysis (EDA) module.
Calculates statistical summaries and extracts patterns from the cleaned dataset.
"""
import pandas as pd
import numpy as np
import os

# Import data loader
from data_loader import load_data

def dataset_summary(df):
    """
    Displays the shape and basic structural info of the dataset.
    """
    print("\n--- 1. Dataset Summary ---")
    print(f"Total Rows: {df.shape[0]}")
    print(f"Total Columns: {df.shape[1]}")
    print("Features included:", list(df.columns))

def risk_distribution(df):
    """
    Analyzes the target variable 'Risk_Status' distribution.
    """
    print("\n--- 2. Risk Status Distribution ---")
    if 'Risk_Status' in df.columns:
        counts = df['Risk_Status'].value_counts()
        percentages = df['Risk_Status'].value_counts(normalize=True) * 100
        
        dist_df = pd.DataFrame({'Count': counts, 'Percentage (%)': percentages.round(2)})
        print(dist_df)
    else:
        print("'Risk_Status' not found in dataset.")

def numerical_summary(df):
    """
    Calculates summary statistics for numerical features:
    Mean, Median, Min, Max, Std Dev, Count.
    """
    print("\n--- 3. Numerical Summary ---")
    
    # Select numeric columns, excluding ID and dummy categorical columns
    exclude_cols = ['Applicant_ID'] + [col for col in df.columns if col.startswith('Employment_Status')]
    numeric_cols = [col for col in df.select_dtypes(include=[np.number]).columns if col not in exclude_cols]
    
    # Calculate statistics
    summary = df[numeric_cols].describe().T
    summary['median'] = df[numeric_cols].median()
    
    # Reorder for clarity
    summary = summary[['count', 'mean', 'median', 'min', 'max', 'std']]
    summary = summary.round(2)
    print(summary)
    
    return summary

def categorical_summary(df):
    """
    Analyzes relationships between numerical features and Risk_Status.
    """
    print("\n--- 4. Feature vs Risk Status Analysis ---")
    
    if 'Risk_Status' not in df.columns:
        return
        
    features = ['Credit_Score', 'Income', 'Loan_Amount', 'Age', 'Loan_Term_Months']
    
    for feature in features:
        if feature in df.columns:
            print(f"\nAverage {feature} by Risk_Status:")
            print(df.groupby('Risk_Status')[feature].mean().round(2))
            
    # Employment Status vs Risk Status
    employment_cols = [col for col in df.columns if col.startswith('Employment_Status')]
    if employment_cols:
        print("\nRisk_Status Distribution within Employment Categories (Count):")
        for col in employment_cols:
            print(f"\n- {col}:")
            print(pd.crosstab(df[col], df['Risk_Status']))

def correlation_analysis(df):
    """
    Generates a correlation matrix for numerical variables.
    """
    print("\n--- 5. Correlation Matrix ---")
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Drop Applicant_ID as it doesn't provide statistical meaning
    if 'Applicant_ID' in numeric_df.columns:
        numeric_df = numeric_df.drop('Applicant_ID', axis=1)
        
    corr_matrix = numeric_df.corr().round(2)
    print(corr_matrix)
    return corr_matrix

def generate_eda_report(df, output_path):
    """
    Executes all EDA functions and exports the numerical summary to a CSV file.
    """
    print("================ EDA START ================")
    
    dataset_summary(df)
    risk_distribution(df)
    num_summary = numerical_summary(df)
    categorical_summary(df)
    correlation_analysis(df)
    
    # Save numerical summary
    num_summary.to_csv(output_path)
    print(f"\n[Success] Numerical EDA Summary saved to: {output_path}")
    
    print("================ EDA COMPLETE ================")

if __name__ == "__main__":
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_path = os.path.join(base_dir, 'data', 'cleaned_loan_data.csv')
    output_path = os.path.join(base_dir, 'data', 'eda_summary.csv')
    
    try:
        # Load cleaned data
        df = load_data(input_path)
        
        if df is not None and not df.empty:
            generate_eda_report(df, output_path)
        else:
            print("Failed to load cleaned dataset for EDA.")
            
    except Exception as e:
        print(f"Error during EDA execution: {e}")
