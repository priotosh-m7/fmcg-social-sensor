import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","")
GEMINI_MODEL=os.getenv("GEMINI_MODEL","")
GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL","")
YOUTUBE_API_KEY  = os.getenv("YOUTUBE_API_KEY", "")
GOOGLE_SEARCH_ENABLED = os.getenv("GOOGLE_SEARCH_ENABLED","")
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)

GOOGLE_CREDENTIALS = os.getenv(
    "GOOGLE_CREDENTIALS",
    "credentials/google-service-account.json"
)

GA4_PROPERTY_ID = os.getenv(
    "GA4_PROPERTY_ID",
    ""
)

SEARCH_CONSOLE_SITE_URL = os.getenv(
    "SEARCH_CONSOLE_SITE_URL",
    ""
)

GOOGLE_ADS_ENABLED = os.getenv(
    "GOOGLE_ADS_ENABLED",
    "false"
).lower() == "true"

GOOGLE_TRENDS_ENABLED = os.getenv(
    "GOOGLE_TRENDS_ENABLED",
    "false"
).lower() == "true"

GOOGLE_ADS_CUSTOMER_ID = os.getenv(
    "GOOGLE_ADS_CUSTOMER_ID",
    ""
)

GOOGLE_ADS_LOCATION_ID = os.getenv(
    "GOOGLE_ADS_LOCATION_ID",
    "2356"
)

GOOGLE_ADS_LANGUAGE_ID = os.getenv(
    "GOOGLE_ADS_LANGUAGE_ID",
    "1000"
)

CLOUDINARY_CLOUD_NAME=os.getenv("CLOUDINARY_CLOUD_NAME","")
CLOUDINARY_API_KEY=os.getenv("CLOUDINARY_API_KEY","")
CLOUDINARY_API_SECRET=os.getenv("CLOUDINARY_API_SECRET","")

BUFFER_API_KEY = os.getenv("BUFFER_API_KEY","")
BUFFER_CHANNEL_ID = os.getenv("BUFFER_CHANNEL_ID","")