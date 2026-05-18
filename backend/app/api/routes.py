from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app.api.schemas import (
    UserCreate, UserResponse, Token,
    ChatRequest, ChatResponse, TicketResponse
)
from app.services.rag_service import rag_service
from app.db.session import get_db
from app.db.models import User, SupportTicket, Conversation
from app.core.security import hash_password, verify_password, create_access_token, decode_token
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == int(payload.get("sub"))).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/health")
def health():
    return {"status": "healthy", "service": "contextual-chatbot"}

@router.post("/auth/register", response_model=UserResponse, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=user_in.email,
        name=user_in.name,
        hashed_password=hash_password(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/auth/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        result = rag_service.generate_response(
            user_message=request.message,
            user_id=request.user_id,
            db=db
        )
        return ChatResponse(
            response=result["response"],
            sentiment=result["sentiment"]["category"],
            sentiment_score=result["sentiment"]["score"],
            sources=result["sources"],
            escalated=result["escalated"]
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}/history")
def get_history(
    user_id: int,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    convos = (db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
        .limit(limit).all())
    return [{"id": c.id, "message": c.message,
             "response": c.response, "sentiment": c.sentiment,
             "created_at": str(c.created_at)} for c in convos]

@router.get("/users/{user_id}/tickets", response_model=List[TicketResponse])
def get_tickets(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(SupportTicket).filter(
        SupportTicket.user_id == user_id
    ).all()