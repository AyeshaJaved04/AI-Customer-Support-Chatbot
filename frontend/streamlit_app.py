import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide"
)

# Session state
if "token" not in st.session_state:
    st.session_state.token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []

def login(email, password):
    try:
        r = requests.post(f"{API_URL}/auth/login",
            data={"username": email, "password": password}, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def register(email, name, password):
    try:
        r = requests.post(f"{API_URL}/auth/register",
            json={"email": email, "name": name, "password": password}, timeout=10)
        if r.status_code == 201:
            return r.json()
        return None
    except:
        return None

def send_message(message, user_id, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.post(f"{API_URL}/chat",
            json={"user_id": user_id, "message": message},
            headers=headers, timeout=60)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            st.session_state.token = None
            return None
        return None
    except:
        return None

def get_tickets(user_id, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(f"{API_URL}/users/{user_id}/tickets",
            headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
        return []
    except:
        return []

def get_sentiment_emoji(sentiment):
    emojis = {"positive": "😊", "negative": "😟", "neutral": "😐", "urgent": "🚨"}
    return emojis.get(sentiment, "😐")

# Sidebar
with st.sidebar:
    st.title("🤖 AI Support Chat")
    st.caption("Contextual Customer Support Chatbot")
    st.divider()

    if not st.session_state.token:
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            login_email = st.text_input("Email", value="testuser1@example.com", key="le")
            login_pass = st.text_input("Password", type="password", value="testpass123", key="lp")
            if st.button("Login", use_container_width=True, type="primary"):
                result = login(login_email, login_pass)
                if result:
                    st.session_state.token = result["access_token"]
                    st.session_state.user_id = 1
                    st.session_state.user_name = login_email.split("@")[0]
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        with tab2:
            reg_name = st.text_input("Name", key="rn")
            reg_email = st.text_input("Email", key="re")
            reg_pass = st.text_input("Password", type="password", key="rp")
            if st.button("Register", use_container_width=True):
                if reg_name and reg_email and reg_pass:
                    result = register(reg_email, reg_name, reg_pass)
                    if result:
                        st.success("Registered! Now login.")
                    else:
                        st.error("Registration failed")
    else:
        st.success(f"Welcome, {st.session_state.user_name}!")
        st.divider()
        st.subheader("Quick Messages")
        quick_msgs = [
            "Where is my order?",
            "I want a refund",
            "How do I return a product?",
            "URGENT: Product broken!",
            "What payment methods do you accept?",
            "I want to speak to a manager"
        ]
        for msg in quick_msgs:
            if st.button(msg, use_container_width=True, key=f"q_{msg}"):
                st.session_state.quick_msg = msg
                st.rerun()
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Tickets", use_container_width=True):
                st.session_state.show_tickets = True
                st.rerun()
        with col2:
            if st.button("Logout", use_container_width=True):
                st.session_state.token = None
                st.session_state.messages = []
                st.rerun()

# Main area
if not st.session_state.token:
    st.title("🤖 AI Customer Support")
    st.markdown("### Welcome! Please login to start chatting.")
    st.info("Test account: testuser1@example.com / testpass123")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 💬 Smart Chat")
        st.caption("AI-powered responses using your purchase history")
    with col2:
        st.markdown("#### 🎯 Sentiment Detection")
        st.caption("Detects mood and auto-escalates urgent issues")
    with col3:
        st.markdown("#### 📋 Ticket System")
        st.caption("Automatic ticket creation for escalations")
else:
    st.title("💬 Customer Support Chat")

    if st.session_state.get("show_tickets"):
        st.subheader("Your Support Tickets")
        tickets = get_tickets(st.session_state.user_id, st.session_state.token)
        if tickets:
            for t in tickets:
                with st.expander(f"Ticket #{t['id']} - {t['subject']}"):
                    st.write(f"**Priority:** {t['priority']}")
                    st.write(f"**Status:** {t['status']}")
                    st.write(f"**Created:** {t['created_at']}")
        else:
            st.info("No tickets yet.")
        if st.button("Back to Chat"):
            st.session_state.show_tickets = False
            st.rerun()
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                if msg["role"] == "assistant" and "sentiment" in msg:
                    s = msg["sentiment"]
                    emoji = get_sentiment_emoji(s)
                    cols = st.columns([1, 1, 2])
                    with cols[0]:
                        st.caption(f"{emoji} {s.upper()}")
                    with cols[1]:
                        if msg.get("sources"):
                            st.caption(f"Sources: {', '.join(set(msg['sources']))}")
                    with cols[2]:
                        if msg.get("escalated"):
                            st.warning("⚡ Escalated to human agent")

        quick_msg = st.session_state.pop("quick_msg", None)
        user_input = st.chat_input("Type your message...")
        message = user_input or quick_msg

        if message:
            st.session_state.messages.append({"role": "user", "content": message})
            with st.chat_message("user"):
                st.write(message)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = send_message(message, st.session_state.user_id, st.session_state.token)
                if result:
                    st.write(result["response"])
                    s = result["sentiment"]
                    emoji = get_sentiment_emoji(s)
                    cols = st.columns([1, 1, 2])
                    with cols[0]:
                        st.caption(f"{emoji} {s.upper()}")
                    with cols[1]:
                        st.caption(f"Sources: {', '.join(set(result['sources']))}")
                    with cols[2]:
                        if result.get("escalated"):
                            st.warning("⚡ Escalated to human agent")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["response"],
                        "sentiment": result["sentiment"],
                        "sources": result["sources"],
                        "escalated": result.get("escalated", False)
                    })
                else:
                    st.error("Failed to get response. Is the API running?")