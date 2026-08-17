from pydantic import BaseModel, Field


class SensorRequest(BaseModel):
    """
    User input for the FMCG Social Sensor.
    The sensor discovers trends, events and conversations automatically.
    """

    brand: str = Field(
        ...,
        min_length=1,
        description="Brand to monitor"
    )

    category: str = Field(
        ...,
        min_length=1,
        description="Product category"
    )

    market: str = Field(
        default="India",
        description="Market to monitor"
    )

    language: str = Field(
        default="en",
        description="Language of monitored content"
    )

    lookback_days: int = Field(
        default=7,
        ge=1,
        le=30,
        description="Number of days of historical content to analyze"
    )


class Article(BaseModel):
    """
    Standardized article structure used internally
    by the Social Sensor.
    """

    source: str = ""

    title: str = ""

    description: str = ""

    url: str = ""

    published_at: str = ""