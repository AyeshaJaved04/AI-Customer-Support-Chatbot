import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings
from typing import List
import logging
import os

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"ChromaDB ready — {self.collection.count()} documents")

    def add_documents(self, documents, embeddings, metadatas, ids):
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Added {len(documents)} docs to ChromaDB")

    def search(self, query_embedding, n_results=5):
        count = self.collection.count()
        if count == 0:
            return {"documents": [], "metadatas": [], "distances": []}
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, count),
            include=["documents", "metadatas", "distances"]
        )
        return {
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "distances": results["distances"][0]
        }

    def count(self):
        return self.collection.count()

vector_store = VectorStore()