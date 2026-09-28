"""
Machine Learning Model Training module.
Trains Logistic Regression, Decision Tree, and Random Forest models
using the preprocessed and scaled training dataset.
"""
import pandas as pd
import os
import joblib

# Import models from scikit-learn
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def load_training_data(base_dir):
    """
    Loads the preprocessed training datasets from the data/ directory.
    """
    data_dir = os.path.join(base_dir, 'data')
    
    try:
        X_train = pd.read_csv(os.path.join(data_dir, 'X_train.csv'))
        y_train = pd.read_csv(os.path.join(data_dir, 'y_train.csv')).squeeze() # Squeeze to 1D Series
        return X_train, y_train
    except Exception as e:
        print(f"Error loading training data: {e}")
        return None, None

def train_models(X_train, y_train, models_dir):
    """
    Trains all three required machine learning models on the training dataset.
    Saves the fitted models to the disk using Joblib.
    """
    print(f"\n--- Initiating Model Training ---")
    print(f"Training Data Shape: X={X_train.shape}, y={y_train.shape}\n")
    
    # 1. Logistic Regression
    print("[1/3] Training Logistic Regression...")
    log_reg = LogisticRegression(random_state=42)
    log_reg.fit(X_train, y_train)
    log_reg_path = os.path.join(models_dir, 'logistic_regression.pkl')
    joblib.dump(log_reg, log_reg_path)
    print(f"      Saved -> {log_reg_path}")
    
    # 2. Decision Tree Classifier
    print("[2/3] Training Decision Tree Classifier...")
    # Limiting depth for simplicity and to prevent extreme overfitting
    tree_clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    tree_clf.fit(X_train, y_train)
    tree_path = os.path.join(models_dir, 'decision_tree.pkl')
    joblib.dump(tree_clf, tree_path)
    print(f"      Saved -> {tree_path}")
    
    # 3. Random Forest Classifier
    print("[3/3] Training Random Forest Classifier...")
    # 100 estimators is a good default balance of performance/speed
    rf_clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf_clf.fit(X_train, y_train)
    rf_path = os.path.join(models_dir, 'random_forest.pkl')
    joblib.dump(rf_clf, rf_path)
    print(f"      Saved -> {rf_path}")
    
    return log_reg_path, tree_path, rf_path

def verify_saved_models(paths):
    """
    Verifies that all models can be successfully loaded from the disk.
    """
    print("\n--- Verifying Saved Models ---")
    all_success = True
    
    for path in paths:
        try:
            model = joblib.load(path)
            model_name = type(model).__name__
            print(f"[Success] Loaded '{model_name}' from {path}")
        except Exception as e:
            print(f"[Error] Failed to load from {path}: {e}")
            all_success = False
            
    if all_success:
        print("\nAll models verified successfully!")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    models_dir = os.path.join(base_dir, 'models')
    
    # Ensure models directory exists
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"Created models directory: {models_dir}")
        
    print("================ ML MODEL TRAINING ================")
    
    X_train, y_train = load_training_data(base_dir)
    
    if X_train is not None and y_train is not None:
        # Train and save models
        saved_paths = train_models(X_train, y_train, models_dir)
        
        # Verify
        verify_saved_models(saved_paths)
    else:
        print("Model training aborted due to missing data.")
        
    print("================ TRAINING COMPLETE ================")
