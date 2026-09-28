"""
Model Evaluation and Comparison module.
Evaluates the three trained classification models against the testing dataset
using Accuracy, Precision, Recall, and F1-score, and generates visualizations.
"""
import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Import metrics from scikit-learn
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    confusion_matrix, 
    classification_report
)

def load_test_data(base_dir):
    """
    Loads the preprocessed testing datasets.
    """
    data_dir = os.path.join(base_dir, 'data')
    try:
        X_test = pd.read_csv(os.path.join(data_dir, 'X_test.csv'))
        y_test = pd.read_csv(os.path.join(data_dir, 'y_test.csv')).squeeze()
        return X_test, y_test
    except Exception as e:
        print(f"Error loading testing data: {e}")
        return None, None

def load_models(base_dir):
    """
    Loads the trained machine learning models from disk.
    Returns a dictionary of models.
    """
    models_dir = os.path.join(base_dir, 'models')
    models = {}
    
    model_files = {
        'Logistic Regression': 'logistic_regression.pkl',
        'Decision Tree': 'decision_tree.pkl',
        'Random Forest': 'random_forest.pkl'
    }
    
    for name, filename in model_files.items():
        path = os.path.join(models_dir, filename)
        try:
            models[name] = joblib.load(path)
        except Exception as e:
            print(f"Failed to load {name} from {path}: {e}")
            
    return models

def evaluate_model(model_name, model, X_test, y_test):
    """
    Generates predictions and calculates Accuracy, Precision, Recall, and F1-Score.
    Positive class is 1 (High Risk).
    """
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    # Using zero_division=0 to handle edge cases in small datasets gracefully
    precision = precision_score(y_test, y_pred, pos_label=1, zero_division=0)
    recall = recall_score(y_test, y_pred, pos_label=1, zero_division=0)
    f1 = f1_score(y_test, y_pred, pos_label=1, zero_division=0)
    
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['Low Risk (0)', 'High Risk (1)'], zero_division=0)
    
    return {
        'Model': model_name,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1_Score': f1,
        'Confusion_Matrix': cm,
        'Classification_Report': report
    }

def generate_confusion_matrix(cm, model_name, save_dir):
    """
    Creates and saves a confusion matrix visualization using Seaborn.
    """
    plt.figure(figsize=(6, 5))
    
    # Labels for the matrix
    x_labels = ['Predicted Low Risk', 'Predicted High Risk']
    y_labels = ['Actual Low Risk', 'Actual High Risk']
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=x_labels, yticklabels=y_labels)
    plt.title(f'Confusion Matrix: {model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    # Format filename (e.g., "Logistic Regression" -> "logistic_regression_confusion_matrix.png")
    filename = f"{model_name.lower().replace(' ', '_')}_confusion_matrix.png"
    plt.savefig(os.path.join(save_dir, filename), bbox_inches='tight')
    plt.close()

def save_comparison_results(results_list, base_dir):
    """
    Saves the comparison metrics to a CSV file.
    """
    # Extract only the flat metrics for the table
    table_data = [
        {
            'Model': r['Model'],
            'Accuracy': round(r['Accuracy'], 4),
            'Precision': round(r['Precision'], 4),
            'Recall': round(r['Recall'], 4),
            'F1_Score': round(r['F1_Score'], 4)
        } 
        for r in results_list
    ]
    
    df = pd.DataFrame(table_data)
    output_path = os.path.join(base_dir, 'data', 'model_comparison.csv')
    df.to_csv(output_path, index=False)
    
    return df

def evaluate_all_models():
    """
    Main orchestration function to run the full evaluation pipeline.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    vis_dir = os.path.join(base_dir, 'visualizations', 'model_evaluation')
    
    # Ensure visualization directory exists
    if not os.path.exists(vis_dir):
        os.makedirs(vis_dir)
        
    print("==================================================")
    print("MODEL EVALUATION")
    print("==================================================")
    
    X_test, y_test = load_test_data(base_dir)
    models = load_models(base_dir)
    
    if X_test is None or not models:
        print("Aborting evaluation due to missing data or models.")
        return
        
    all_results = []
    
    for name, model in models.items():
        # Evaluate metrics
        results = evaluate_model(name, model, X_test, y_test)
        all_results.append(results)
        
        # Save visualization
        generate_confusion_matrix(results['Confusion_Matrix'], name, vis_dir)
        
        # Print detailed report
        print(f"\n{name}")
        print("-" * len(name))
        print(f"Accuracy  : {results['Accuracy']:.4f}")
        print(f"Precision : {results['Precision']:.4f}")
        print(f"Recall    : {results['Recall']:.4f}")
        print(f"F1-Score  : {results['F1_Score']:.4f}")
        print("\nClassification Report:")
        print(results['Classification_Report'])
        print("Confusion Matrix:")
        print(results['Confusion_Matrix'])
        print("\n" + "="*50)
        
    # Save and display final comparison table
    comparison_df = save_comparison_results(all_results, base_dir)
    
    print("\n==================================================")
    print("COMPARISON TABLE")
    print("==================================================")
    
    # Print the DataFrame as a string table
    print(comparison_df.to_string(index=False))
    
    print("\n[Disclaimer]")
    print("Because this is a small academic dataset of only 100 records with a 20-record test set,")
    print("these evaluation results should be interpreted cautiously. Different metrics represent")
    print("different aspects of classification performance (e.g., Recall focuses on minimizing")
    print("false negatives, while Precision minimizes false positives). These results are for")
    print("educational demonstration and are not evidence of real-world loan performance.")

if __name__ == "__main__":
    evaluate_all_models()
