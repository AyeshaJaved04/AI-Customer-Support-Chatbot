from openai import OpenAI
from app.core.config import settings
import redis
import json
import hashlib
import logging
from typing import List

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL
        self.cache = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.cache_ttl = 86400

    def _cache_key(self, text: str) -> str:
        return f"emb:{hashlib.md5(text.encode()).hexdigest()}"

    def create_embedding(self, text: str) -> List[float]:
        key = self._cache_key(text)
        try:
            cached = self.cache.get(key)
            if cached:
                return json.loads(cached)
        except Exception:
            pass
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        embedding = response.data[0].embedding
        try:
            self.cache.setex(key, self.cache_ttl, json.dumps(embedding))
        except Exception:
            pass
        return embedding

    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [item.embedding for item in response.data]

embedding_service = EmbeddingService()