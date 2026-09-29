from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import sys, os
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

router = APIRouter()

MODELS = {}
SCALER = None

try:
    from prediction import predict_risk, load_models, load_scaler
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    MODELS = load_models(BASE_DIR)
    SCALER = load_scaler(BASE_DIR)
except Exception as e:
    print(f"CRITICAL ERROR LOADING PREDICTION MODULE OR MODELS: {e}")
    traceback.print_exc()

class PredictionRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    income: float = Field(..., gt=0)
    credit_score: int = Field(..., ge=300, le=900)
    loan_amount: float = Field(..., gt=0)
    loan_term_months: int = Field(..., ge=12, le=60)
    employment_status: str
    model: str = "Random Forest"

@router.post("/predict")
def predict(req: PredictionRequest):
    if req.employment_status not in ["Employed", "Self-Employed", "Unemployed"]:
        raise HTTPException(status_code=422, detail="Invalid Employment Status.")
    applicant_data = {
        'Age': req.age, 'Income': req.income, 'Credit_Score': req.credit_score,
        'Loan_Amount': req.loan_amount, 'Loan_Term_Months': req.loan_term_months,
        'Employment_Status': req.employment_status
    }
    try:
        res = predict_risk(applicant_data, MODELS, SCALER, model_name=req.model)
        if "error" in res:
            raise HTTPException(status_code=400, detail=res["error"])
            
        # Append to live in-memory state instead of modifying dataset
        try:
            from api.state import LIVE_PREDICTIONS
            prediction_record = {
                'Age': req.age,
                'Income': req.income,
                'Credit_Score': req.credit_score,
                'Loan_Amount': req.loan_amount,
                'Loan_Term_Months': req.loan_term_months,
                'Employment_Status': req.employment_status,
                'Risk_Status': res["risk_label"],
                'Model': req.model
            }
            LIVE_PREDICTIONS.append(prediction_record)
            
            # Persist to Postgres database
            from api.db import save_prediction
            save_prediction(prediction_record)
            
        except Exception as e:
            print(f"Failed to append to live state or database: {e}")
            
        return {
            "risk_status": res["risk_label"], "risk_code": res["risk_code"],
            "probability": res.get("prediction_probability"), "model_used": res["model_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))