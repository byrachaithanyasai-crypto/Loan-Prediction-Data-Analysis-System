from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()
PERF_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/model_comparison.csv'))

@router.get('/models')
def get_models():
    return ['Random Forest', 'Logistic Regression', 'Decision Tree']

@router.get('/models/performance')
def get_performance():
    models_list = ['Random Forest', 'Logistic Regression', 'Decision Tree']
    result = {}
    
    # Initialize all metrics to 0
    for m in models_list:
        result[m] = {
            'Accuracy': 0.0,
            'Precision': 0.0,
            'Recall': 0.0,
            'F1 Score': 0.0
        }
        
    try:
        from api.state import LIVE_PREDICTIONS
        if len(LIVE_PREDICTIONS) == 0:
            return result
            
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
        from api.routes_prediction import MODELS, SCALER
        from prediction import predict_risk
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        for m in models_list:
            model_records = [p for p in LIVE_PREDICTIONS if p.get('Model') == m]
            
            if len(model_records) == 0:
                continue
                
            y_true = [1 if p['Risk_Status'] in ['High', 'High Risk'] else 0 for p in model_records]
            
            y_pred = []
            for p in model_records:
                # predict_risk expects applicant_data
                res = predict_risk(p, MODELS, SCALER, model_name=m)
                if "error" in res:
                    y_pred.append(0) # fallback
                else:
                    y_pred.append(res['risk_code'])
                    
            acc = accuracy_score(y_true, y_pred)
            prec = precision_score(y_true, y_pred, pos_label=1, zero_division=0)
            rec = recall_score(y_true, y_pred, pos_label=1, zero_division=0)
            f1 = f1_score(y_true, y_pred, pos_label=1, zero_division=0)
            
            result[m] = {
                'Accuracy': round(acc, 4),
                'Precision': round(prec, 4),
                'Recall': round(rec, 4),
                'F1 Score': round(f1, 4)
            }
            
        return result
    except Exception as e:
        print('Error calculating live performance:', e)
        return result
