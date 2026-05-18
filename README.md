# AI Customer Support Chatbot

Enterprise customer support system with RAG-based contextual responses, sentiment analysis, and automated escalation. Built for handling customer inquiries using purchase history and knowledge base integration.

## Architecture

```text
┌─────────────┐
│   Client    │
│ (HTML/UI)   │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────────────────────┐
│      FastAPI Backend        │
│  ┌────────────────────────┐ │
│  │   Auth / JWT Layer     │ │
│  └───────────┬────────────┘ │
│              ▼               │
│  ┌────────────────────────┐ │
│  │   RAG Service          │ │
│  │   Sentiment Analysis   │ │
│  └───────────┬────────────┘ │
│              ▼               │
│  ┌────────────────────────┐ │
│  │   Groq LLM API         │ │
│  │   (Llama 3.1)          │ │
│  └────────────────────────┘ │
└──────────┬──────────────────┘
           │
           ▼
    ┌────────────┐
    │ PostgreSQL │
    │   Redis    │
    └────────────┘
```

**Flow:**
1. User submits query via frontend
2. Backend authenticates request (JWT)
3. Sentiment analysis detects emotion
4. RAG retrieves context (purchase history + knowledge base)
5. LLM generates personalized response
6. Auto-escalation creates ticket if urgent
7. Response stored and returned

## Features

- Context-aware responses using customer purchase history
- Real-time sentiment analysis (positive/negative/urgent)
- Automatic ticket creation for escalated issues
- RAG pipeline with knowledge base integration
- JWT-based authentication
- Conversation logging and analytics
- Prometheus/Grafana monitoring

## Tech Stack

**Frontend**
- HTML/CSS/JavaScript
- Streamlit (alternative UI)

**Backend**
- FastAPI
- SQLAlchemy ORM
- Pydantic validation
- uvicorn ASGI server

**Database**
- PostgreSQL 15
- Redis (caching)

**AI/ML**
- Groq API (Llama 3.1 8B)
- HuggingFace Transformers (DistilBERT sentiment)
- Custom RAG implementation

**Infrastructure**
- Docker Compose
- Prometheus
- Grafana
- pytest

## Project Structure

```
AI-Customer-Support-Chatbot/
├── backend/
│   └── app/
│       ├── api/              
│       ├── core/             
│       ├── db/               
│       ├── services/         
│       └── main.py
├── frontend/
│   ├── index.html
│   └── streamlit_app.py
├── database/
│   └── data/
│       └── raw/
│           └── knowledge_base.json
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── prometheus.yml
├── scripts/
│   ├── init_db.py
│   └── seed_data.py
├── tests/
│   ├── test_api.py
│   ├── test_sentiment.py
│   └── conftest.py
├── .env.example
├── requirements.txt
└── README.md
```
## Setup

### Prerequisites

- Python 3.11+
- Docker Desktop
- PostgreSQL 15+ (or use Docker)

### Clone Repository

```bash
git clone https://github.com/AyeshaJaved04/AI-Customer-Support-Chatbot.git
cd AI-Customer-Support-Chatbot
```

### Backend Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

```env
DATABASE_URL=postgresql://chatbot:chatbot123@127.0.0.1:5433/chatbot_db
REDIS_URL=redis://127.0.0.1:6379/0
SECRET_KEY=your-secret-key-minimum-32-characters
GROQ_API_KEY=your-groq-api-key
LLM_MODEL=llama-3.1-8b-instant
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database Setup

```bash
cd docker
docker compose up -d
cd ..
python scripts/init_db.py
python scripts/seed_data.py
```

### Frontend Setup

```bash
cd frontend
python -m http.server 8501
```

## Running the Application

**Development:**
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Production (Docker):**
```bash
docker compose -f docker/docker-compose.yml up -d
```

**Access Points:**
- Frontend: `http://localhost:8501/`
- API Docs: `http://localhost:8000/docs`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

**Test Credentials:**
- Email: `testuser1@example.com`
- Password: `testpass123`

## API Overview

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/auth/register` | POST | Create user account |
| `/api/v1/auth/login` | POST | Obtain JWT token |
| `/api/v1/chat` | POST | Send message, get AI response |
| `/api/v1/users/{id}/history` | GET | Retrieve conversation history |
| `/api/v1/users/{id}/tickets` | GET | List support tickets |
| `/api/v1/health` | GET | Health check |
| `/metrics` | GET | Prometheus metrics |

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=backend --cov-report=html
```

## Security

- JWT authentication with token expiry (30 min)
- bcrypt password hashing (cost factor 12)
- Environment variable protection (`.env` git-ignored)
- SQL injection prevention via SQLAlchemy ORM
- Input validation with Pydantic schemas
- CORS configuration
- Rate limiting infrastructure (Redis-backed)

## Deployment

**Docker:**
```bash
docker compose -f docker/docker-compose.yml up -d
```

**Cloud Platforms:**
- Render.com (Free tier)
- Railway.app
- AWS/Azure/GCP (containerized)

**Required Environment Variables:**
- `DATABASE_URL`
- `REDIS_URL`
- `SECRET_KEY`
- `GROQ_API_KEY`

## Monitoring

- **Prometheus** (`http://localhost:9090`) - Metrics collection
- **Grafana** (`http://localhost:3000`) - Dashboards

**Tracked Metrics:**
- Request count by endpoint
- Response time percentiles
- Error rates
- Active sessions

