# Loan Prediction Data Analysis System

## Project Overview
The Loan Prediction Data Analysis System is a modern Data Analytics Essentials academic project. It evaluates the default risk of loan applicants based on financial history using Machine Learning, providing an interactive dashboard for risk assessment and statistical analytics.

## Problem Statement
Financial institutions need reliable mechanisms to predict whether an applicant is a high-risk or low-risk candidate for a loan to minimize financial loss and streamline the approval process.

## Objectives
- Build an end-to-end Machine Learning pipeline.
- Evaluate multiple classification algorithms.
- Provide a robust, real-time prediction REST API.
- Deliver a premium, responsive Full-Stack web application for visualization.

## Key Features
- **Interactive Risk Prediction**: Real-time risk probability calculation.
- **Exploratory Data Analysis**: Deep insights into the financial dataset.
- **Model Evaluation**: Transparent comparison of ML algorithms (Accuracy, Precision, Recall, F1).

## System Architecture
**Frontend**: React, Vite, Tailwind CSS, Recharts
**Backend**: FastAPI, Python
**Machine Learning**: Scikit-learn, Pandas, Joblib

## Dataset Description
- 100 historical loan applicant records.
- **Features**: Age, Income, Credit Score, Loan Amount, Loan Term, Employment Status.
- **Target**: `Risk_Status` (0 = Low Risk, 1 = High Risk).

## Project Structure
```text
smart-loan-risk/
├── backend/                  # FastAPI Application
├── frontend/                 # React UI
├── data/                     # Cleaned Datasets & Comparison Metrics
├── models/                   # Pre-trained ML Models & Scalers (.pkl)
├── src/                      # Core ML Training & Pipeline Logic
└── visualizations/           # Pre-computed Analytics Charts
```

## Local Setup

### Backend Setup
```bash
cd backend
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
*API Docs available at `http://localhost:8000/docs`*

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
Configure `frontend/.env.example` as `.env` and `backend/.env`.
- `VITE_API_URL`: Path to the FastAPI backend (e.g., `http://localhost:8000`)
- `ALLOWED_ORIGINS`: CORS whitelist for the backend (e.g., `http://localhost:5173`)

## Deployment
- **Backend (Render)**: Set root to `backend/`. Build: `pip install -r requirements.txt`. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
- **Frontend (Vercel)**: Framework `Vite`. Root `frontend/`. Add `VITE_API_URL` to Vercel environment variables pointing to the Render URL.

## Limitations
- **Data Size**: Model is trained on a 100-record dataset. 

## Academic Disclaimer
This platform is built as an educational/academic project. The model performance and risk predictions should not be interpreted as real-world financial advice or production-grade lending rules.
