from fastapi import APIRouter, BackgroundTasks
import pandas as pd
import os

router = APIRouter()
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/cleaned_loan_data.csv'))

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
        
        low_risk = sum(1 for p in LIVE_PREDICTIONS if p['Risk_Status'] in ['Low', 'Low Risk'])
        high_risk = sum(1 for p in LIVE_PREDICTIONS if p['Risk_Status'] in ['High', 'High Risk'])
        avg_income = sum(p['Income'] for p in LIVE_PREDICTIONS) / total
        avg_credit = sum(p['Credit_Score'] for p in LIVE_PREDICTIONS) / total
        avg_loan = sum(p['Loan_Amount'] for p in LIVE_PREDICTIONS) / total
        
        return {
            'total_applicants': total,
            'low_risk': low_risk,
            'high_risk': high_risk,
            'avg_income': round(avg_income, 2),
            'avg_credit_score': round(avg_credit, 2),
            'avg_loan_amount': round(avg_loan, 2)
        }
    except Exception as e:
        return {'error': str(e)}

def generate_viz_bg(df, viz_dir):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import sys
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        src_dir = os.path.join(base_dir, 'src')
        if src_dir not in sys.path:
            sys.path.append(src_dir)
        from visualization import generate_all_visualizations
        generate_all_visualizations(df, viz_dir)
    except Exception as e:
        print(f"Failed to regenerate visualizations: {e}")

@router.get('/analysis/summary')
def get_summary(background_tasks: BackgroundTasks):
    if not os.path.exists(DATA_PATH): return {}
    try:
        df = pd.read_csv(DATA_PATH)
        
        # Trigger visualization regeneration in background so it doesn't block
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        viz_dir = os.path.join(base_dir, 'frontend', 'public', 'visualizations')
        background_tasks.add_task(generate_viz_bg, df, viz_dir)
            
        # Identify risk column
        risk_col = 'Risk_Status'
        
        # Calculate Employment Distribution from current analyzed dataset (live predictions)
        from api.state import LIVE_PREDICTIONS
        
        employed = sum(1 for p in LIVE_PREDICTIONS if p.get('Employment_Status') == 'Employed')
        self_employed = sum(1 for p in LIVE_PREDICTIONS if p.get('Employment_Status') == 'Self-Employed')
        unemployed = sum(1 for p in LIVE_PREDICTIONS if p.get('Employment_Status') == 'Unemployed')
        
        employment_data = [
            {'name': 'Employed', 'value': employed},
            {'name': 'Self-Employed', 'value': self_employed},
            {'name': 'Unemployed', 'value': unemployed}
        ]
            
        # Calculate Risk by Income Bucket
        df['Income_Bucket'] = pd.qcut(df['Income'], q=4, labels=['Low', 'Medium', 'High', 'Very High'])
        risk_by_income = []
        for bucket in ['Low', 'Medium', 'High', 'Very High']:
            bucket_df = df[df['Income_Bucket'] == bucket]
            low_risk = len(bucket_df[bucket_df[risk_col].isin(['Low', 'Low Risk'])])
            high_risk = len(bucket_df[bucket_df[risk_col].isin(['High', 'High Risk'])])
            risk_by_income.append({
                'bucket': bucket,
                'Low Risk': low_risk,
                'High Risk': high_risk
            })
            
        return {
            'employment_distribution': employment_data,
            'risk_by_income': risk_by_income
        }
    except Exception as e:
        return {'error': str(e)}
