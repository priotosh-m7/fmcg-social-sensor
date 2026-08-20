from fastapi import FastAPI, HTTPException
from app.schemas import SensorRequest, CreativeRequest, ImageRequest, PublishSocialPostRequest
from app.services.sensor import run_sensor
from app.services.creative import generate_creative
from app.services.image import create_image
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.services.buffer import publish_to_buffer,test_buffer_channel
from app.services.buffer_insights import get_post_metrics

app = FastAPI(
    title="FMCG Social Sensor",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://hul-wss7-nu.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "FMCG Social Sensor"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.post("/api/social-sensor")
async def social_sensor(request: SensorRequest):
    try:
        return await run_sensor(request)

    except Exception as e:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}"
        )

@app.post("/api/creative-generator")
async def creative_generator(request: CreativeRequest):
    try:
        return await generate_creative(request)

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}"
        )

@app.post("/api/creative-generator/image")
async def creative_image(request: ImageRequest):
    try:
        result = await create_image(
            brand=request.brand,
            category=request.category,
            visual_prompt=request.visual_prompt
        )

        return {
            "brand": request.brand,
            "category": request.category,
            "image": result
        }

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}"
        )
@app.get("/api/buffer/test-channel")
async def test_channel():
    return await test_buffer_channel()


@app.get("/api/social/insights/{post_id}")
async def social_insights(post_id: str):
    try:
        return await get_post_metrics(post_id)

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}"
        )

@app.post("/api/social/publish")
async def publish_social_post(request: PublishSocialPostRequest):
    try:
        caption = (
            f"{request.creative.headline}\n\n"
            f"{request.creative.body_copy}\n\n"
            f"👉 {request.creative.cta}\n\n"
            f"{' '.join(request.creative.hashtags)}"
        )

        result = await publish_to_buffer(
            image_url=request.image.image_url,
            caption=caption,
            scheduled_at=request.scheduled_at
        )

        return {
            "status": "success",
            "platform": "instagram",
            "brand": request.brand,
            "image_url": request.image.image_url,
            "caption": caption,
            "scheduled_at": request.scheduled_at,
            "buffer_response": result
        }

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}"
        )
