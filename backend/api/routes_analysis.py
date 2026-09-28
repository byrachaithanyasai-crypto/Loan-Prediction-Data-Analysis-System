from fastapi import APIRouter, BackgroundTasks
import pandas as pd
import os
import numpy as np

router = APIRouter()

def generate_viz_bg(df, viz_dir):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import sys
        
        # Robust path resolution for backend root
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        src_dir = os.path.join(base_dir, 'src')
        if not os.path.exists(src_dir):
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
            src_dir = os.path.join(base_dir, 'src')
            
        if src_dir not in sys.path:
            sys.path.append(src_dir)
            
        from visualization import generate_all_visualizations
        generate_all_visualizations(df, viz_dir)
    except Exception as e:
        print(f"Failed to regenerate visualizations: {e}")

@router.get('/dashboard/stats')
def get_stats():
    try:
        from api.state import LIVE_PREDICTIONS
        
        total = len(LIVE_PREDICTIONS)
        
        if total == 0:
            return {
                'total_applicants': 0,
                'low_risk': 0,
                'high_risk': 0,
                'avg_income': 0,
                'avg_credit_score': 0,
                'avg_loan_amount': 0
            }
            
        live_df = pd.DataFrame(LIVE_PREDICTIONS)
        
        # Risk column
        risk_col = 'Risk_Status'
        
        low_risk = int(live_df[live_df[risk_col].isin(['Low', 'Low Risk'])].shape[0]) if risk_col in live_df.columns else 0
        high_risk = int(live_df[live_df[risk_col].isin(['High', 'High Risk'])].shape[0]) if risk_col in live_df.columns else 0
            
        # Means
        avg_income = float(live_df['Income'].mean(skipna=True)) if 'Income' in live_df.columns else 0.0
        avg_credit = float(live_df['Credit_Score'].mean(skipna=True)) if 'Credit_Score' in live_df.columns else 0.0
        avg_loan = float(live_df['Loan_Amount'].mean(skipna=True)) if 'Loan_Amount' in live_df.columns else 0.0
        
        # Handle case where all values are NaN
        avg_income = 0.0 if pd.isna(avg_income) else avg_income
        avg_credit = 0.0 if pd.isna(avg_credit) else avg_credit
        avg_loan = 0.0 if pd.isna(avg_loan) else avg_loan

        return {
            'total_applicants': total,
            'low_risk': low_risk,
            'high_risk': high_risk,
            'avg_income': round(avg_income, 2),
            'avg_credit_score': round(avg_credit, 2),
            'avg_loan_amount': round(avg_loan, 2)
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {'error': str(e)}


@router.get('/analysis/summary')
def get_summary(background_tasks: BackgroundTasks):
    try:
        from api.state import LIVE_PREDICTIONS
        
        employed = self_employed = unemployed = 0
        risk_by_income = []
        
        if len(LIVE_PREDICTIONS) == 0:
            return {
                'employment_distribution': [
                    {'name': 'Employed', 'value': 0},
                    {'name': 'Self-Employed', 'value': 0},
                    {'name': 'Unemployed', 'value': 0}
                ],
                'risk_by_income': []
            }
            
        df = pd.DataFrame(LIVE_PREDICTIONS)
        
        # Trigger visualization regeneration in background
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        viz_dir = os.path.join(base_dir, 'frontend', 'public', 'visualizations')
        if not os.path.exists(os.path.join(base_dir, 'frontend')):
            # Fallback for Render
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
            viz_dir = os.path.join(base_dir, 'frontend', 'public', 'visualizations')
            
        os.makedirs(viz_dir, exist_ok=True)
        if len(df) > 1: # Only try to generate plots if there is enough data for statistics
            background_tasks.add_task(generate_viz_bg, df.copy(), viz_dir)
            
        # 1. Calculate Employment Distribution
        if 'Employment_Status' in df.columns:
            counts = df['Employment_Status'].value_counts(dropna=True)
            employed = int(counts.get('Employed', 0))
            self_employed = int(counts.get('Self-Employed', 0))
            unemployed = int(counts.get('Unemployed', 0))
            
        employment_data = [
            {'name': 'Employed', 'value': employed},
            {'name': 'Self-Employed', 'value': self_employed},
            {'name': 'Unemployed', 'value': unemployed}
        ]
            
        # 2. Calculate Risk by Income Bucket
        risk_col = 'Risk_Status'
        
        if risk_col in df.columns and 'Income' in df.columns:
            # Handle NaNs
            safe_income = df['Income'].fillna(df['Income'].median() if not df['Income'].isna().all() else 0)
            
            try:
                # Need at least 4 unique values for 4 quantiles, else fallback
                if len(safe_income.unique()) < 4:
                    raise ValueError("Not enough unique income values for quantiles")
                    
                df['Income_Bucket'] = pd.qcut(safe_income, q=4, duplicates='drop')
                buckets = df['Income_Bucket'].cat.categories
                
                labels = ['Low', 'Medium', 'High', 'Very High'][:len(buckets)]
                df['Income_Bucket'] = pd.qcut(safe_income, q=4, labels=labels, duplicates='drop')
                
                for bucket in labels:
                    bucket_df = df[df['Income_Bucket'] == bucket]
                    low_risk = int(bucket_df[bucket_df[risk_col].isin(['Low', 'Low Risk'])].shape[0])
                    high_risk = int(bucket_df[bucket_df[risk_col].isin(['High', 'High Risk'])].shape[0])
                    risk_by_income.append({
                        'bucket': bucket,
                        'Low Risk': low_risk,
                        'High Risk': high_risk
                    })
            except Exception:
                # Fallback if qcut fails (too few data points)
                low_risk = int(df[df[risk_col].isin(['Low', 'Low Risk'])].shape[0])
                high_risk = int(df[df[risk_col].isin(['High', 'High Risk'])].shape[0])
                risk_by_income = [{
                    'bucket': 'All Incomes',
                    'Low Risk': low_risk,
                    'High Risk': high_risk
                }]
        
        return {
            'employment_distribution': employment_data,
            'risk_by_income': risk_by_income
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {'error': str(e)}