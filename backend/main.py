from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes_prediction import router as prediction_router
from api.routes_analysis import router as analysis_router
from api.routes_models import router as models_router

app = FastAPI(title="Loan Prediction Data Analysis System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://loan-prediction-data-analysis-system-1.onrender.com",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "Loan Prediction Data Analysis System API"
    }


app.include_router(prediction_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
app.include_router(models_router, prefix="/api")