"""
Loan Risk Prediction module.
Provides a reusable API for the upcoming Streamlit dashboard to predict
applicant risk using trained Machine Learning models.
"""
import pandas as pd
import numpy as np
import os
import joblib

def load_models(base_dir):
    """
    Loads all available trained machine learning models from disk.
    """
    models_dir = os.path.join(base_dir, 'models')
    models = {}
    
    # Clean display-name to filename mapping
    model_mapping = {
        'Random Forest': 'random_forest.pkl',
        'Logistic Regression': 'logistic_regression.pkl',
        'Decision Tree': 'decision_tree.pkl'
    }
    
    for display_name, filename in model_mapping.items():
        try:
            filepath = os.path.join(models_dir, filename)
            if os.path.exists(filepath):
                models[display_name] = joblib.load(filepath)
        except Exception as e:
            print(f"Error loading {display_name}: {e}")
            
    return models

def load_scaler(base_dir):
    """
    Loads the fitted StandardScaler from disk.
    """
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    try:
        scaler = joblib.load(scaler_path)
        return scaler
    except Exception as e:
        print(f"Error loading scaler: {e}")
        return None

def validate_input(applicant_data):
    """
    Validates user input against business rules.
    Returns (True, "") if valid, (False, "Error message") if invalid.
    """
    if not (18 <= applicant_data.get('Age', 0) <= 100):
        return False, "Validation Error: Age must be between 18 and 100."
        
    if applicant_data.get('Income', 0) <= 0:
        return False, "Validation Error: Income must be greater than 0."
        
    if not (300 <= applicant_data.get('Credit_Score', 0) <= 900):
        return False, "Validation Error: Credit Score must be between 300 and 900."
        
    if applicant_data.get('Loan_Amount', 0) <= 0:
        return False, "Validation Error: Loan Amount must be greater than 0."
        
    if not (12 <= applicant_data.get('Loan_Term_Months', 0) <= 60):
        return False, "Validation Error: Loan Term must be between 12 and 60 months."
        
    valid_emp_status = ['Employed', 'Self-Employed', 'Unemployed']
    if applicant_data.get('Employment_Status') not in valid_emp_status:
        return False, f"Validation Error: Employment Status must be one of {valid_emp_status}."
        
    return True, "Valid"

def prepare_input(applicant_data, scaler, model_name):
    """
    Converts raw applicant data into a Machine Learning compatible feature array.
    Handles Employment Status one-hot encoding.
    Applies scaling for Logistic Regression, bypasses scaling for Tree-based models.
    """
    # 1. Handle Employment Status (One-Hot Encoding)
    emp = applicant_data['Employment_Status']
    emp_employed = 1 if emp == 'Employed' else 0
    emp_self = 1 if emp == 'Self-Employed' else 0
    emp_unemployed = 1 if emp == 'Unemployed' else 0
    
    # 2. Structure data in the exact column order used during training
    # Feature columns: Age, Income, Credit_Score, Loan_Amount, Loan_Term_Months, Emp_Employed, Emp_Self, Emp_Unemployed
    input_df = pd.DataFrame([{
        'Age': applicant_data['Age'],
        'Income': applicant_data['Income'],
        'Credit_Score': applicant_data['Credit_Score'],
        'Loan_Amount': applicant_data['Loan_Amount'],
        'Loan_Term_Months': applicant_data['Loan_Term_Months'],
        'Employment_Status_Employed': emp_employed,
        'Employment_Status_Self-Employed': emp_self,
        'Employment_Status_Unemployed': emp_unemployed
    }])
    
    # 3. Scale only if the model requires it
    # Note: If the tree models were trained on scaled data, they would normally require scaled inputs too.
    # However, per strict academic project instructions, we scale ONLY for Logistic Regression here.
    if model_name == 'Logistic Regression' and scaler is not None:
        num_cols = ['Age', 'Income', 'Credit_Score', 'Loan_Amount', 'Loan_Term_Months']
        input_df[num_cols] = scaler.transform(input_df[num_cols])
        
    return input_df

def get_prediction_probability(model, prepared_input):
    """
    Attempts to get prediction probabilities if the model supports it.
    """
    try:
        # predict_proba returns array like [[prob_class_0, prob_class_1]]
        probs = model.predict_proba(prepared_input)[0]
        # Return probability of the predicted class (max probability)
        return max(probs)
    except Exception:
        # Fallback if model doesn't support predict_proba
        return None

def predict_risk(applicant_data, models, scaler, model_name="Random Forest"):
    """
    Core prediction orchestrator.
    Validates, prepares, and predicts using the specified model.
    """
    # 1. Validate Input
    is_valid, msg = validate_input(applicant_data)
    if not is_valid:
        return {"error": msg}
        
    # 2. Select Model
    if model_name not in models:
        return {"error": f"Model '{model_name}' not found."}
        
    model = models[model_name]
    
    # 3. Prepare Input
    prepared_input = prepare_input(applicant_data, scaler, model_name)
    
    # 4. Predict
    prediction_code = int(model.predict(prepared_input)[0])
    prediction_label = "High Risk" if prediction_code == 1 else "Low Risk"
    probability = get_prediction_probability(model, prepared_input)
    
    return {
        "risk_label": prediction_label,
        "risk_code": prediction_code,
        "prediction_probability": round(probability * 100, 2) if probability else None,
        "model_name": model_name
    }

if __name__ == "__main__":
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    # Load Models & Scaler
    models = load_models(base_dir)
    scaler = load_scaler(base_dir)
    
    if not models or scaler is None:
        print("Initialization failed: Missing models or scaler.")
    else:
        # Sample Applicant Data
        sample_applicant = {
            'Age': 35,
            'Income': 75000,
            'Credit_Score': 650,
            'Loan_Amount': 20000,
            'Loan_Term_Months': 36,
            'Employment_Status': 'Employed'
        }
        
        # Test 1: Successful Prediction
        print("\n==================================================")
        print("LOAN RISK PREDICTION")
        print("==================================================")
        
        print("\nApplicant Details")
        print(f"Age              : {sample_applicant['Age']}")
        print(f"Income           : ${sample_applicant['Income']}")
        print(f"Credit Score     : {sample_applicant['Credit_Score']}")
        print(f"Loan Amount      : ${sample_applicant['Loan_Amount']}")
        print(f"Loan Term        : {sample_applicant['Loan_Term_Months']} months")
        print(f"Employment       : {sample_applicant['Employment_Status']}")
        
        # Run prediction
        result = predict_risk(sample_applicant, models, scaler, model_name="Random Forest")
        
        if "error" in result:
            print(f"\n[ERROR] {result['error']}")
        else:
            print("\nPrediction")
            print(f"Risk Status      : {result['risk_label']} (Code: {result['risk_code']})")
            if result['prediction_probability']:
                print(f"Probability      : {result['prediction_probability']}%")
            print(f"Model Used       : {result['model_name']}")
            
        print("==================================================\n")
        
        # Test 2: Validation Check (Intentional Failure)
        print("--- Testing Validation Logic ---")
        invalid_applicant = sample_applicant.copy()
        invalid_applicant['Credit_Score'] = 200 # Below 300 minimum
        
        invalid_result = predict_risk(invalid_applicant, models, scaler)
        print(f"Testing invalid Credit Score (200) -> {invalid_result.get('error', 'Failed to catch error')}")
