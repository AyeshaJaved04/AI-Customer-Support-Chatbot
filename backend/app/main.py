from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router
import logging

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s %(name)s %(levelname)s %(message)s"
)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Contextual Customer Support Chatbot with RAG + Sentiment"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router, prefix="/api/v1", tags=["chatbot"])

@app.on_event("startup")
async def startup():
    logging.info(f"Starting {settings.APP_NAME}")

from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )