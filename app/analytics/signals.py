from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

def sentiment_score(texts):
    if not texts:
        return 0.0
    scores = [_analyzer.polarity_scores(t)["compound"] for t in texts if t.strip()]
    return round(sum(scores) / len(scores), 3) if scores else 0.0

def growth_pct(current, baseline):
    if baseline <= 0:
        return 100.0 if current else 0.0
    return round(((current - baseline) / baseline) * 100, 2)

def opportunity_score(velocity, sentiment, brand_relevance, event_relevance):
    velocity = max(0, min(100, velocity))
    sentiment_0_100 = ((sentiment + 1) / 2) * 100
    return round(
        velocity * 0.30 +
        sentiment_0_100 * 0.15 +
        brand_relevance * 0.30 +
        event_relevance * 0.25, 2
    )
