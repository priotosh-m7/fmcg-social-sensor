from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="FMCG Social Sensor API",
    description="Prototype API for detecting brand-relevant trends and real-time cultural opportunities.",
    version="0.1.0",
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"name": "FMCG Social Sensor", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "ok"}
