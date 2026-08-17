# FMCG Social Sensor API

Prototype FastAPI backend for detecting brand-relevant trends and real-time cultural opportunities.

## Current sources
- NewsAPI
- GDELT
- Ollama (optional; local LLM)

Reddit is intentionally left out until approved API credentials are available.

## 1. Create environment

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
```

## 2. Install

```bash
pip install -r requirements.txt
```

## 3. Configure

Copy `.env.example` to `.env` and add your NewsAPI key.

For AI insights, install Ollama and pull a model:

```bash
ollama pull llama3.2
```

The application has a fallback insight generator if Ollama is unavailable.

## 4. Run

```bash
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000/docs

## 5. Test

POST `/api/social-sensor`

Example:

```json
{
  "brand": "Rexona",
  "category": "Deodorants",
  "event": {
    "event_type": "substitution",
    "minute": 67,
    "match": "Brazil vs Germany",
    "team": "Brazil",
    "player_in": "Player B",
    "player_out": "Player A"
  },
  "competitors": [
    "NIVEA Men",
    "Wild Stone",
    "Park Avenue"
  ],
  "lookback_days": 7
}
```

## Important prototype limitation

`mention_velocity_pct` currently uses a temporary baseline derived from the current result count. A real-time sensor should store timestamped observations in a database and compare the current 5-minute window against historical windows.

Also, a live sports/event API is needed to automatically trigger events such as substitutions. The current endpoint accepts the event as input so the complete insight pipeline can be tested first.
