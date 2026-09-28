"""
Feature Engineering and Machine Learning Data Preparation module.
Splits data, scales features, and prepares inputs for ML models.
"""
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from data_loader import load_data

def prepare_features(df):
    """
    Separates the dataset into input features (X) and target variable (y).
    Removes 'Applicant_ID' (not predictive) and extracts 'Risk_Status'.
    """
    print("\n[1/5] Separating features (X) and target (y)...")
    
    # Exclude identifier and target from X
    cols_to_drop = ['Risk_Status']
    if 'Applicant_ID' in df.columns:
        cols_to_drop.append('Applicant_ID')
        
    X = df.drop(columns=cols_to_drop)
    y = df['Risk_Status'].copy()
    
    print(f"Features included in X ({len(X.columns)}): {list(X.columns)}")
    return X, y

def encode_target(y):
    """
    Converts categorical target into binary numerical values.
    Low Risk -> 0
    High Risk -> 1
    """
    print("[2/5] Encoding target variable...")
    y_encoded = y.map({'Low': 0, 'High': 1})
    
    # If mapping failed due to different casing, fallback to lambda
    if y_encoded.isnull().any():
        y_encoded = y.apply(lambda x: 0 if str(x).strip().lower() == 'low' else 1)
        
    return y_encoded

def split_data(X, y):
    """
    Splits the dataset into 80% training and 20% testing data.
    Uses stratification to maintain the ratio of Low/High risk applicants.
    """
    print("[3/5] Splitting data into Training (80%) and Testing (20%)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42, 
        stratify=y # Critical for imbalanced datasets
    )
    return X_train, X_test, y_train, y_test

def scale_features(X_train, X_test, scaler_path):
    """
    Applies StandardScaler to numerical features to normalize ranges.
    Fits ONLY on X_train to prevent Data Leakage.
    Transforms both X_train and X_test.
    """
    print("[4/5] Scaling features (Standardization) to prevent data leakage...")
    
    scaler = StandardScaler()
    
    # Identify which columns are numerical (excluding one-hot encoded categories)
    numerical_cols = ['Age', 'Income', 'Credit_Score', 'Loan_Amount', 'Loan_Term_Months']
    
    # Ensure columns exist in dataset
    numerical_cols = [col for col in numerical_cols if col in X_train.columns]
    
    # Create copies to avoid SettingWithCopy warning
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    # Fit scaler strictly on training data
    scaler.fit(X_train_scaled[numerical_cols])
    
    # Transform both datasets
    X_train_scaled[numerical_cols] = scaler.transform(X_train_scaled[numerical_cols])
    X_test_scaled[numerical_cols] = scaler.transform(X_test_scaled[numerical_cols])
    
    # Save the fitted scaler
    joblib.dump(scaler, scaler_path)
    print(f"      Fitted Scaler saved to: {scaler_path}")
    
    return X_train_scaled, X_test_scaled

def save_processed_data(X_train, X_test, y_train, y_test, base_dir):
    """
    Saves the processed splits to CSV files for reproducibility.
    """
    print("[5/5] Saving processed splits to disk...")
    
    data_dir = os.path.join(base_dir, 'data')
    
    X_train.to_csv(os.path.join(data_dir, 'X_train.csv'), index=False)
    X_test.to_csv(os.path.join(data_dir, 'X_test.csv'), index=False)
    y_train.to_csv(os.path.join(data_dir, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(data_dir, 'y_test.csv'), index=False)
    
    print("      Data successfully saved to data/ directory.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_path = os.path.join(base_dir, 'data', 'cleaned_loan_data.csv')
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    
    try:
        df = load_data(input_path)
        
        if df is not None and not df.empty:
            print("\n================ FEATURE ENGINEERING & ML PREP ================")
            
            # Print Original
            print(f"Original columns ({len(df.columns)}): {list(df.columns)}")
            
            # Step 1: Prepare X and y
            X, y = prepare_features(df)
            
            # Step 2: Encode Target
            y = encode_target(y)
            
            # Step 3: Split
            X_train, X_test, y_train, y_test = split_data(X, y)
            
            # Step 4: Scale
            X_train_scaled, X_test_scaled = scale_features(X_train, X_test, scaler_path)
            
            # Step 5: Save
            save_processed_data(X_train_scaled, X_test_scaled, y_train, y_test, base_dir)
            
            print("\n================ PREPARATION COMPLETE ================")
            print("\n--- Summary ---")
            print(f"X shape: {X.shape}")
            print(f"y shape: {y.shape}")
            print(f"Training set shape (X, y): {X_train_scaled.shape}, {y_train.shape}")
            print(f"Testing set shape  (X, y): {X_test_scaled.shape}, {y_test.shape}")
            
            print("\n--- Target Class Distribution (0: Low Risk, 1: High Risk) ---")
            print("Training Data:\n", y_train.value_counts(normalize=True).round(2))
            print("Testing Data:\n", y_test.value_counts(normalize=True).round(2))
            
            print("\n--- Validation Checks ---")
            assert 'Applicant_ID' not in X_train_scaled.columns, "Failed: Applicant_ID still in X"
            assert 'Risk_Status' not in X_train_scaled.columns, "Failed: Risk_Status still in X"
            assert list(X_train_scaled.columns) == list(X_test_scaled.columns), "Failed: Train/Test columns mismatch"
            assert X_train_scaled.isnull().sum().sum() == 0, "Failed: Missing values found in Training set"
            assert X_test_scaled.isnull().sum().sum() == 0, "Failed: Missing values found in Testing set"
            print("All validation checks PASSED successfully.")
            
        else:
            print("Failed to load dataset.")
            
    except Exception as e:
        print(f"Error during feature engineering execution: {e}")
