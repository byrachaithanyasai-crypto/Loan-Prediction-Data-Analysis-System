"""
Data Visualization module.
Generates and saves static (Matplotlib/Seaborn) and interactive (Plotly) charts.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

from data_loader import load_data

def reconstruct_employment_status(df):
    """
    Reconstructs the original 'Employment_Status' category from dummy variables
    if it was one-hot encoded, to make plotting easier.
    """
    df_plot = df.copy()
    emp_cols = [col for col in df_plot.columns if col.startswith('Employment_Status_')]
    
    if emp_cols:
        # Revert dummy columns back to a single categorical column
        def get_emp_status(row):
            for col in emp_cols:
                if row[col] == 1:
                    return col.replace('Employment_Status_', '')
            return 'Unknown'
            
        df_plot['Employment_Status'] = df_plot.apply(get_emp_status, axis=1)
        
    return df_plot

def plot_risk_distribution(df, save_dir):
    """A. Risk Status Distribution"""
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='Risk_Status', palette='Set2')
    plt.title('Risk Status Distribution')
    plt.xlabel('Risk Status')
    plt.ylabel('Count')
    plt.savefig(os.path.join(save_dir, 'risk_distribution.png'), bbox_inches='tight')
    plt.close()

def plot_credit_score_analysis(df, save_dir):
    """B. Credit Score Analysis"""
    # Histogram
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Credit_Score'], bins=20, kde=True, color='blue')
    plt.title('Credit Score Distribution')
    plt.xlabel('Credit Score')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(save_dir, 'credit_score_distribution.png'), bbox_inches='tight')
    plt.close()
    
    # Box plot
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='Risk_Status', y='Credit_Score', palette='Set2')
    plt.title('Credit Score by Risk Status')
    plt.xlabel('Risk Status')
    plt.ylabel('Credit Score')
    plt.savefig(os.path.join(save_dir, 'credit_score_vs_risk.png'), bbox_inches='tight')
    plt.close()

def plot_income_analysis(df, save_dir):
    """C. Income Analysis"""
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Income'], bins=20, kde=True, color='green')
    plt.title('Income Distribution')
    plt.xlabel('Income')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(save_dir, 'income_distribution.png'), bbox_inches='tight')
    plt.close()
    
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='Risk_Status', y='Income', palette='Set2')
    plt.title('Income by Risk Status')
    plt.xlabel('Risk Status')
    plt.ylabel('Income')
    plt.savefig(os.path.join(save_dir, 'income_vs_risk.png'), bbox_inches='tight')
    plt.close()

def plot_loan_amount_analysis(df, save_dir):
    """D. Loan Amount Analysis"""
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Loan_Amount'], bins=20, kde=True, color='purple')
    plt.title('Loan Amount Distribution')
    plt.xlabel('Loan Amount')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(save_dir, 'loan_amount_distribution.png'), bbox_inches='tight')
    plt.close()
    
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='Risk_Status', y='Loan_Amount', palette='Set2')
    plt.title('Loan Amount by Risk Status')
    plt.xlabel('Risk Status')
    plt.ylabel('Loan Amount')
    plt.savefig(os.path.join(save_dir, 'loan_amount_vs_risk.png'), bbox_inches='tight')
    plt.close()

def plot_age_analysis(df, save_dir):
    """E. Age Analysis"""
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Age'], bins=15, kde=True, color='orange')
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(save_dir, 'age_distribution.png'), bbox_inches='tight')
    plt.close()
    
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='Risk_Status', y='Age', palette='Set2')
    plt.title('Age by Risk Status')
    plt.xlabel('Risk Status')
    plt.ylabel('Age')
    plt.savefig(os.path.join(save_dir, 'age_vs_risk.png'), bbox_inches='tight')
    plt.close()

def plot_employment_analysis(df, save_dir):
    """F. Employment Analysis"""
    if 'Employment_Status' in df.columns:
        plt.figure(figsize=(8, 5))
        sns.countplot(data=df, x='Employment_Status', hue='Risk_Status', palette='Set2')
        plt.title('Employment Status vs Risk Status')
        plt.xlabel('Employment Status')
        plt.ylabel('Count')
        plt.legend(title='Risk Status')
        plt.savefig(os.path.join(save_dir, 'employment_vs_risk.png'), bbox_inches='tight')
        plt.close()

def plot_loan_term_analysis(df, save_dir):
    """G. Loan Term Analysis"""
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='Loan_Term_Months', palette='viridis')
    plt.title('Loan Term Months Distribution')
    plt.xlabel('Loan Term (Months)')
    plt.ylabel('Count')
    plt.savefig(os.path.join(save_dir, 'loan_term_distribution.png'), bbox_inches='tight')
    plt.close()

def plot_relationship_analysis(df, save_dir):
    """H. Relationship Analysis"""
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x='Income', y='Credit_Score', hue='Risk_Status', palette='Set2', alpha=0.7)
    plt.title('Credit Score vs Income (by Risk Status)')
    plt.xlabel('Income')
    plt.ylabel('Credit Score')
    plt.savefig(os.path.join(save_dir, 'credit_score_vs_income.png'), bbox_inches='tight')
    plt.close()
    
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x='Loan_Amount', y='Credit_Score', hue='Risk_Status', palette='Set2', alpha=0.7)
    plt.title('Credit Score vs Loan Amount (by Risk Status)')
    plt.xlabel('Loan Amount')
    plt.ylabel('Credit Score')
    plt.savefig(os.path.join(save_dir, 'credit_score_vs_loan_amount.png'), bbox_inches='tight')
    plt.close()

def plot_correlation_heatmap(df, save_dir):
    """I. Correlation Heatmap"""
    numeric_df = df.select_dtypes(include=[np.number])
    if 'Applicant_ID' in numeric_df.columns:
        numeric_df = numeric_df.drop('Applicant_ID', axis=1)
        
    plt.figure(figsize=(10, 8))
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.savefig(os.path.join(save_dir, 'correlation_heatmap.png'), bbox_inches='tight')
    plt.close()

def generate_interactive_plotly(df, save_dir):
    """Generates an interactive Plotly HTML for Streamlit usage later (Optional export)."""
    fig = px.scatter(df, x='Income', y='Loan_Amount', color='Risk_Status',
                     hover_data=['Age', 'Credit_Score'],
                     title='Interactive: Income vs Loan Amount by Risk Status')
    fig.write_html(os.path.join(save_dir, 'interactive_income_loan.html'))

def generate_all_visualizations(df, save_dir):
    """Runs all plotting functions sequentially."""
    print("================ VISUALIZATION START ================")
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Created directory: {save_dir}")
        
    df_plot = reconstruct_employment_status(df)
    
    plot_risk_distribution(df_plot, save_dir)
    print("Generated: Risk Distribution (Bar)")
    
    plot_credit_score_analysis(df_plot, save_dir)
    print("Generated: Credit Score Analysis (Hist & Box)")
    
    plot_income_analysis(df_plot, save_dir)
    print("Generated: Income Analysis (Hist & Box)")
    
    plot_loan_amount_analysis(df_plot, save_dir)
    print("Generated: Loan Amount Analysis (Hist & Box)")
    
    plot_age_analysis(df_plot, save_dir)
    print("Generated: Age Analysis (Hist & Box)")
    
    plot_employment_analysis(df_plot, save_dir)
    print("Generated: Employment vs Risk Status (Bar)")
    
    plot_loan_term_analysis(df_plot, save_dir)
    print("Generated: Loan Term Distribution (Bar)")
    
    plot_relationship_analysis(df_plot, save_dir)
    print("Generated: Relationship Scatters (Income/Loan vs Credit Score)")
    
    plot_correlation_heatmap(df_plot, save_dir)
    print("Generated: Correlation Heatmap")
    
    generate_interactive_plotly(df_plot, save_dir)
    print("Generated: Plotly Interactive HTML")
    
    print("\n[Success] All charts saved successfully to the visualizations folder.")
    print("================ VISUALIZATION COMPLETE ================")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_path = os.path.join(base_dir, 'data', 'cleaned_loan_data.csv')
    visualizations_dir = os.path.join(base_dir, 'visualizations')
    
    try:
        df = load_data(input_path)
        if df is not None and not df.empty:
            generate_all_visualizations(df, visualizations_dir)
        else:
            print("Failed to load dataset for visualization.")
    except Exception as e:
        print(f"Error during visualization execution: {e}")
