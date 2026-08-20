from typing import List, Optional
from pydantic import BaseModel, Field



class SocialCreative(BaseModel):
    headline: str
    body_copy: str
    cta: str
    hashtags: List[str]


class SocialImage(BaseModel):
    image_url: str


class PublishSocialPostRequest(BaseModel):
    brand: str
    category: str
    format: str = "Instagram Post"
    creative: SocialCreative
    image: SocialImage
    scheduled_at: Optional[str] = None

class PublishSocialPostRequest(BaseModel):
    brand: str
    category: str
    format: str = "Instagram Post"
    creative: SocialCreative
    image: SocialImage
    scheduled_at: Optional[str] = None

class SensorRequest(BaseModel):
    brand: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    market: str = "India"
    language: str = "en"
    lookback_days: int = Field(default=7, ge=1, le=30)

class Opportunity(BaseModel):
    rank: int
    trend: str
    what_is_happening: str
    consumer_relevance: str
    brand_connection: str
    opportunity_score: float
    urgency: str
    confidence: str
    timing: str
    evidence: List[str]

class SensorOutput(BaseModel):
    summary: str
    opportunities: List[Opportunity]
    overall_assessment: str

class CreativeInsight(BaseModel):
    trend: str
    what_is_happening: str
    consumer_relevance: str
    brand_connection: str
    opportunity_score: float
    urgency: str
    confidence: str


class CreativeRequest(BaseModel):
    rank: int
    trend: str
    what_is_happening: str
    consumer_relevance: str
    brand_connection: str
    opportunity_score: float
    urgency: str
    confidence: str
    timing: str
    evidence: List[str]

    brand: str
    category: str
    market: str = "India"
    format: str = "Instagram Post"
    objective: str = "Brand awareness"


class CreativeOutput(BaseModel):
    headline: str
    body_copy: str
    cta: str
    hashtags: List[str]
    creative_direction: str
    visual_prompt: str

class ImageRequest(BaseModel):
    brand: str
    category: str
    visual_prompt: str