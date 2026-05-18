from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = None
        logger.info("SentimentAnalyzer created — model will load on first use")

    def _load_model(self):
        if self.analyzer is None:
            try:
                from transformers import pipeline
                logger.info(f"Loading sentiment model: {settings.SENTIMENT_MODEL}")
                self.analyzer = pipeline(
                    "sentiment-analysis",
                    model=settings.SENTIMENT_MODEL,
                    device=-1
                )
                logger.info("Sentiment model loaded successfully")
            except Exception as e:
                logger.error(f"Could not load sentiment model: {e}")
                self.analyzer = None

    def analyze(self, text: str) -> dict:
        if not text.strip():
            return {"label": "NEUTRAL", "score": 0.5, "category": "neutral"}
        self._load_model()
        if self.analyzer is None:
            return {"label": "NEUTRAL", "score": 0.5, "category": "neutral"}
        try:
            result = self.analyzer(text[:512])[0]
            label = result["label"]
            score = result["score"]
            urgent_keywords = [
                "urgent", "asap", "immediately", "emergency",
                "critical", "broken", "worst", "lawsuit", "refund now"
            ]
            is_urgent = any(kw in text.lower() for kw in urgent_keywords)
            if is_urgent and label == "NEGATIVE":
                category = "urgent"
            elif label == "POSITIVE" and score > 0.75:
                category = "positive"
            elif label == "NEGATIVE" and score > 0.75:
                category = "negative"
            else:
                category = "neutral"
            return {"label": label, "score": round(score, 4), "category": category}
        except Exception as e:
            logger.error(f"Sentiment error: {e}")
            return {"label": "NEUTRAL", "score": 0.5, "category": "neutral"}

sentiment_analyzer = SentimentAnalyzer()