import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

# BACKEND
write_file('backend/requirements.txt', '''fastapi
uvicorn
pandas
numpy
scikit-learn
joblib
pydantic''')

write_file('backend/main.py', '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes_prediction import router as prediction_router
from api.routes_analysis import router as analysis_router
from api.routes_models import router as models_router

app = FastAPI(title="Loan Prediction Data Analysis System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Loan Prediction Data Analysis System API"}

app.include_router(prediction_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
app.include_router(models_router, prefix="/api")''')

write_file('backend/api/routes_prediction.py', '''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
try:
    from prediction import predict_risk, load_models, load_scaler
except ImportError:
    pass

router = APIRouter()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

try:
    MODELS = load_models(BASE_DIR)
    SCALER = load_scaler(BASE_DIR)
except NameError:
    MODELS, SCALER = {}, None

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
        return {
            "risk_status": res["risk_label"], "risk_code": res["risk_code"],
            "probability": res.get("prediction_probability"), "model_used": res["model_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))''')

write_file('backend/api/routes_analysis.py', '''from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/cleaned_loan_data.csv'))

@router.get("/dashboard/stats")
def get_stats():
    if not os.path.exists(DATA_PATH): return {}
    try:
        df = pd.read_csv(DATA_PATH)
        return {
            "total_applicants": len(df),
            "low_risk": len(df[df['Risk_Status'] == 'Low']),
            "high_risk": len(df[df['Risk_Status'] == 'High']),
            "avg_income": float(df['Income'].mean()),
            "avg_credit_score": float(df['Credit_Score'].mean()),
            "avg_loan_amount": float(df['Loan_Amount'].mean())
        }
    except Exception:
        return {}

@router.get("/analysis/summary")
def get_summary():
    return {"status": "ok"}''')

write_file('backend/api/routes_models.py', '''from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()
PERF_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/model_comparison.csv'))

@router.get("/models")
def get_models():
    return ["Random Forest", "Logistic Regression", "Decision Tree"]

@router.get("/models/performance")
def get_performance():
    if not os.path.exists(PERF_PATH): return []
    try:
        df = pd.read_csv(PERF_PATH)
        return df.to_dict(orient='records')
    except Exception:
        return []''')

# FRONTEND SCAFFOLDING
write_file('frontend/package.json', '''{
  "name": "smart-loan-risk-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.1.4"
  }
}''')

write_file('frontend/vite.config.js', '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})''')

write_file('frontend/index.html', '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Loan Prediction Data Analysis System</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>''')

write_file('frontend/src/main.jsx', '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './styles/global.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)''')

write_file('frontend/src/App.jsx', '''import React from 'react'

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold text-blue-900 mb-4">Loan Prediction Data Analysis System</h1>
      <p className="text-lg text-gray-600">The React frontend is successfully initialized and ready for development.</p>
      <div className="mt-8 p-6 bg-white rounded shadow-md border-t-4 border-blue-500">
        <h2 className="text-xl font-semibold mb-2">Next Steps:</h2>
        <ul className="list-disc pl-5 text-gray-700">
          <li>Install dependencies: <code>npm install</code></li>
          <li>Start dev server: <code>npm run dev</code></li>
          <li>Integrate React Router for navigation</li>
          <li>Connect to FastAPI backend at <code>VITE_API_URL</code></li>
        </ul>
      </div>
    </div>
  )
}

export default App''')

write_file('frontend/src/styles/global.css', '''/* Placeholder for Tailwind or custom CSS */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f8fafc;
}''')

write_file('frontend/.env.example', 'VITE_API_URL=http://localhost:8000')

print("All files created successfully!")
