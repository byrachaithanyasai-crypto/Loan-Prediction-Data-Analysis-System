from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes_prediction import router as prediction_router
from api.routes_analysis import router as analysis_router
from api.routes_models import router as models_router
from fastapi.middleware.cors import CORSMiddleware

import os

app = FastAPI(title="Loan Prediction Data Analysis System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://loan-prediction-data-analysis-system-1.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
# Temporarily allow all during development if env var is *, otherwise strictly enforce
if "*" in allowed_origins:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Loan Prediction Data Analysis System API"}

app.include_router(prediction_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
app.include_router(models_router, prefix="/api")