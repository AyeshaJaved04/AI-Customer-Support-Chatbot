# 🤖 AI Customer Support Chatbot

AI-powered customer support system with RAG (Retrieval Augmented Generation), sentiment analysis, and intelligent auto-escalation.

## ✨ Features

- **Context-Aware Responses**: Uses customer purchase history for personalized support
- **Sentiment Analysis**: Detects customer mood (positive/negative/urgent)
- **Auto-Escalation**: Automatically creates support tickets for urgent issues
- **RAG Pipeline**: Combines knowledge base with real-time data retrieval
- **Premium UI**: Clean, modern black-themed interface
- **Real-time Monitoring**: Prometheus + Grafana dashboards

## 🛠️ Tech Stack

**Backend:**
- FastAPI (REST API)
- PostgreSQL (Database)
- Redis (Caching)
- SQLAlchemy (ORM)

**AI/ML:**
- Groq (Llama 3.1 - FREE LLM)
- HuggingFace Transformers (Sentiment Analysis)
- RAG Pipeline (Knowledge Base + Purchase History)

**Frontend:**
- HTML/CSS/JavaScript (Premium black UI)
- Streamlit (Alternative UI)

**DevOps:**
- Docker Compose
- Prometheus (Metrics)
- Grafana (Monitoring)
- pytest (Testing)

## 📦 Installation

### Prerequisites
- Python 3.11+
- Docker Desktop
- PostgreSQL (or use Docker)

### Setup

1. **Clone repository**
```bash
git clone https://github.com/AyeshaJaved04/AI-Customer-Support-Chatbot.git
cd AI-Customer-Support-Chatbot
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Start Docker containers**
```bash
cd docker
docker compose up -d
```

6. **Initialize database**
```bash
python scripts/init_db.py
python scripts/seed_data.py
```

7. **Run API**
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

8. **Open frontend**
