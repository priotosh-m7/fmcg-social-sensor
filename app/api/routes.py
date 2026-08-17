from fastapi import APIRouter, HTTPException
from app.schemas import SensorRequest
from app.services.sensor import run_sensor

router = APIRouter()

@router.post("/social-sensor")
async def social_sensor(request: SensorRequest):
    try:
        return await run_sensor(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
