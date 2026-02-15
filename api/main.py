"""
FastAPI Backend for StudyMate
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime
from typing import Optional
import uuid
import os
from dotenv import load_dotenv

# Force load .env
load_dotenv()

# Verify it's loaded
print(f"🔑 OPENAI_API_KEY loaded: {'✅' if os.getenv('OPENAI_API_KEY') else '❌'}")
print(f"📱 Model: {os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}")
# Import the agent
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent import StudyMateAgent

app = FastAPI(
    title="StudyMate API",
    description="AI Teaching Agent using Questioning Method",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Enable CORS (for Streamlit to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for sessions and agents
sessions = {}
agents = {}

# Request/Response Models
class SessionCreate(BaseModel):
    github_url: str
    student_name: Optional[str] = "Student"
    knowledge_level: Optional[str] = "intermediate"

class ChatMessage(BaseModel):
    session_id: str
    message: str

class SessionResponse(BaseModel):
    session_id: str
    greeting: str
    repo_analyzed: bool

class ChatResponse(BaseModel):
    response: str
    session_id: str


# Root endpoint
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "StudyMate API",
        "version": "1.0.0"
    }


# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "active_sessions": len(sessions),
        "agents_initialized": len(agents),
        "openai_key_configured": bool(os.getenv("OPENAI_API_KEY")),
        "timestamp": datetime.now().isoformat()
    }


# Create session endpoint
@app.post("/session/create", response_model=SessionResponse)
async def create_session(session_data: SessionCreate):
    """
    Creates a new learning session with agent.
    """
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Initialize agent (without repo for now)
        print(f"🔧 Initializing agent for session {session_id}...")
        agent = StudyMateAgent(repo_path=None)
        agents[session_id] = agent
        
        # Store session info
        sessions[session_id] = {
            "id": session_id,
            "github_url": session_data.github_url,
            "student_name": session_data.student_name,
            "knowledge_level": session_data.knowledge_level,
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
        
        # Generate personalized greeting using the agent
        greeting_prompt = f"""Hello! I'm StudyMate. The student's name is {session_data.student_name} and they have {session_data.knowledge_level} level knowledge. They want to explore: {session_data.github_url}

Generate a warm, personalized greeting and ask them what specific aspect interests them most. Keep it conversational and encouraging."""
        
        greeting = agent.teach(greeting_prompt, session_id=session_id)
        
        # Store greeting
        sessions[session_id]["messages"].append({
            "role": "assistant",
            "content": greeting,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"✅ Agent initialized for session {session_id}")
        
        return SessionResponse(
            session_id=session_id,
            greeting=greeting,
            repo_analyzed=False  # True when we add GitHub cloning
        )
        
    except Exception as e:
        print(f"❌ Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(chat_msg: ChatMessage):
    """
    Handles student messages using the agent.
    """
    # Validate session
    if chat_msg.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if chat_msg.session_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not initialized for this session")
    
    session = sessions[chat_msg.session_id]
    agent = agents[chat_msg.session_id]
    
    try:
        # Store student message
        session["messages"].append({
            "role": "user",
            "content": chat_msg.message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Get agent response
        print(f"🤖 Agent processing: {chat_msg.message[:50]}...")
        response = agent.teach(chat_msg.message, session_id=chat_msg.session_id)
        
        # Store response
        session["messages"].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return ChatResponse(
            response=response,
            session_id=chat_msg.session_id
        )
        
    except Exception as e:
        print(f"❌ Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


# Get session history
@app.get("/session/{session_id}/history")
async def get_history(session_id: str):
    """Returns conversation history for a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "messages": sessions[session_id]["messages"],
        "total_messages": len(sessions[session_id]["messages"])
    }


# Get session progress
@app.get("/session/{session_id}/progress")
async def get_progress(session_id: str):
    """Returns learning progress for a session."""
    progress_file = f"data/progress/progress_{session_id}.json"
    
    if not os.path.exists(progress_file):
        return {
            "session_id": session_id,
            "concepts_covered": [],
            "message": "No progress tracked yet"
        }
    
    try:
        import json
        with open(progress_file, 'r') as f:
            progress = json.load(f)
        return progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading progress: {str(e)}")


# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting StudyMate API with Agent Integration...")
    print("📚 Endpoints available:")
    print("   GET  /              - Root")
    print("   GET  /health        - Health check")
    print("   POST /session/create - Create session with agent")
    print("   POST /chat          - Chat with agent")
    print("   GET  /session/{id}/history - Get history")
    print("   GET  /session/{id}/progress - Get progress")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
