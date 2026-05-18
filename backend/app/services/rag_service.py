from groq import Groq
from app.core.config import settings
from app.services.sentiment_service import sentiment_analyzer
from app.db.models import User, Conversation, Purchase, SupportTicket
from sqlalchemy.orm import Session
import json
import os
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a helpful, empathetic customer support assistant.
You have access to the customer's purchase history and past conversations.
Always personalize your response using this context.
Be concise, accurate, and solution-focused.
If you cannot solve the issue, offer to escalate to a human agent."""

class RAGService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.knowledge_base = []
        try:
            kb_path = "data/raw/knowledge_base.json"
            if os.path.exists(kb_path):
                with open(kb_path) as f:
                    self.knowledge_base = json.load(f)
                logger.info(f"Loaded {len(self.knowledge_base)} KB entries")
        except Exception as e:
            logger.error(f"KB load error: {e}")

    def get_user_context(self, user_id: int, db: Session) -> str:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return "New customer - no history available."
        recent = (db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .limit(3).all())
        purchases = (db.query(Purchase)
            .filter(Purchase.user_id == user_id)
            .order_by(Purchase.purchase_date.desc())
            .limit(5).all())
        ctx = f"Customer: {user.name} ({user.email})\n"
        if purchases:
            ctx += "Recent purchases:\n"
            for p in purchases:
                ctx += f"  - {p.product_name} (${p.price:.2f}) Status: {p.status}\n"
        if recent:
            ctx += "Recent interactions:\n"
            for c in recent:
                ctx += f"  Q: {c.message[:100]}\n  A: {c.response[:100]}\n"
        return ctx

    def retrieve_knowledge(self, query: str):
        if not self.knowledge_base:
            return [], []
        query_lower = query.lower()
        scored = []
        for entry in self.knowledge_base:
            q = entry["question"].lower()
            a = entry["answer"].lower()
            score = 0
            for word in query_lower.split():
                if word in q:
                    score += 2
                if word in a:
                    score += 1
            if score > 0:
                scored.append((score, entry))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:5]
        docs = [f"Q: {e['question']}\nA: {e['answer']}" for _, e in top]
        sources = [e.get("category", "General") for _, e in top]
        return docs, sources

    def should_escalate(self, sentiment: str, message: str) -> bool:
        if sentiment == "urgent":
            return True
        escalation_phrases = [
            "speak to human", "real person", "manager",
            "supervisor", "complaint", "legal action"
        ]
        return any(p in message.lower() for p in escalation_phrases)

    def generate_response(self, user_message: str, user_id: int, db: Session) -> dict:
        sentiment = sentiment_analyzer.analyze(user_message)
        user_context = self.get_user_context(user_id, db)
        kb_docs, sources = self.retrieve_knowledge(user_message)
        knowledge_context = "\n\n".join(kb_docs) if kb_docs else "No relevant KB articles found."

        sys_prompt = SYSTEM_PROMPT
        if sentiment["category"] == "urgent":
            sys_prompt += "\n\nWARNING: Customer is urgent/frustrated. Prioritize speed and empathy."
        elif sentiment["category"] == "negative":
            sys_prompt += "\n\nNote: Customer seems unhappy. Be extra supportive."

        user_prompt = f"""CUSTOMER CONTEXT:
{user_context}

KNOWLEDGE BASE:
{knowledge_context}

CUSTOMER MESSAGE: {user_message}

Respond helpfully using the above context."""

        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        reply = response.choices[0].message.content

        convo = Conversation(
            user_id=user_id,
            message=user_message,
            response=reply,
            sentiment=sentiment["category"],
            sentiment_score=sentiment["score"],
            metadata_={"sources": sources, "model": settings.LLM_MODEL}
        )
        db.add(convo)

        escalate = self.should_escalate(sentiment["category"], user_message)
        if escalate:
            ticket = SupportTicket(
                user_id=user_id,
                subject="Auto-escalated conversation",
                description=user_message,
                priority="high",
                status="open"
            )
            db.add(ticket)
            reply += "\n\nI have flagged this for a human agent to follow up shortly."

        db.commit()
        return {
            "response": reply,
            "sentiment": sentiment,
            "sources": sources,
            "escalated": escalate
        }

rag_service = RAGService()