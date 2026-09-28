from fastapi import FastAPI
from backend.routes.factcheck import router as factcheck_router


app = FastAPI(
    title="VeritasAI API",
    description="Autonomous Multimodal Fact-Checking & Deepfake Audit Platform",
    version="1.0.0"
)


app.include_router(
    factcheck_router,
    prefix="/api/factcheck",
    tags=["Fact Checking"]
)


@app.get("/")
def home():
    return {
        "message": "Welcome to VeritasAI!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
