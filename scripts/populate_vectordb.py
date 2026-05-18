import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from app.db.vector_store import vector_store
from app.services.embedding_service import embedding_service

with open("data/raw/knowledge_base.json") as f:
    kb = json.load(f)

print(f"Embedding {len(kb)} FAQ entries into ChromaDB...")
BATCH = 10

for i in range(0, len(kb), BATCH):
    batch = kb[i:i+BATCH]
    texts = [f"{e['question']} {e['answer']}" for e in batch]
    embeddings = embedding_service.create_embeddings_batch(texts)
    vector_store.add_documents(
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"category": e.get("category","General"),
                    "question": e["question"]} for e in batch],
        ids=[f"kb_{i+j}" for j in range(len(batch))]
    )
    print(f"  Embedded {min(i+BATCH, len(kb))}/{len(kb)}")

print(f"ChromaDB now has {vector_store.count()} documents. RAG ready!")
