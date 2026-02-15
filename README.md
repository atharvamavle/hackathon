# Sophiie AI Agents Hackathon 2026

## Your Submission

> **Instructions:** Fill out this section in your forked repo. This is what judges will see first.

### Participant

| Field | Your Answer |
|-------|-------------|
| **Name** |Atharva Santosh Mavale |
| **University / Employer** | Deakin University |

### Project

| Field | Your Answer |
|-------|-------------|
| **Project Name** |StudyMate AI (AI Questioning Tutor for Code Repos) | 
| **One-Line Description** |An AI-powered **Questioning coding tutor** that helps students understand code (especially intimidating GitHub repositories) by asking the right questions, giving progressive hints, and guiding learning step-by-step. |
| **Live App Link** | https://atharvamavle-hackathon-uiapp-ps07su.streamlit.app/ |
| **Demo Video Link** | https://youtu.be/CJm-7gzGaEs|
| **Tech Stack** | FastAPI Uvicorn, OpenAI ,Python SDK, LangChain|
| **AI Provider(s) Used** | OpenAI , GPT |

# StudyMate  — AI Questioning Tutor for Code Repos

An AI-powered **Questioning coding tutor** that helps students understand code (especially intimidating GitHub repositories) by asking the right questions, giving progressive hints, and guiding learning step-by-step.

This project was built for the **Sophiie AI Agents Hackathon 2026**.

- Backend: FastAPI (deployed on Render)
- Frontend: Streamlit (deployed on Streamlit Community Cloud)
- LLM: OpenAI (configured via `OPENAI_API_KEY`)

---

## The gap we’re solving (real problem)

You’ve identified a massive gap in AI education that most tools don’t solve well:

**Current reality**
- Students copy‑paste AI-generated code without understanding.
- They get stuck when code breaks or needs changes.
- Typical chatbots either dump code or give overwhelming explanations.
- Large GitHub repos feel impossible to start (lots of files, complex structure).
- Traditional step-by-step tutorials don’t adapt to a student’s confusion.

**Our solution**
- A **Questioning AI agent** that teaches by asking questions instead of giving answers.
- Students learn by doing: the agent helps them reason, not copy.
- Adaptive dialogue based on student level (beginner/intermediate/advanced).
- Progressive hints when needed.

---

## Why this is perfect for the hackathon

1) **Unique & impactful**
- Directly addresses the “AI copy‑paste crisis” in education.
- Focuses on understanding and reasoning, not output.

2) **Agentic behavior (not just a chatbot)**
- Multi-turn memory (session-based chat).
- Guided questioning (Questioning method).
- Prompt-driven teaching behavior.

3) **Production-ready architecture**
- Deployed backend + UI.
- Health endpoint and API docs.

---

## Features

- 🤖 **Questioning dialogue**: Probing questions instead of direct answers.
- 💬 **Session-based chat**: Each user gets a `session_id`.
- 🧠 **Adaptive teaching**: Student name + knowledge level influence the tone and depth.
- 🧪 **API docs included**: FastAPI Swagger at `/docs`.
- 🚀 **Deployed**: Backend on Render, UI on Streamlit.

---

## Tech stack

### Backend
- FastAPI
- Uvicorn
- OpenAI Python SDK
- LangChain `ChatOpenAI`

### Frontend
- Streamlit
- Requests

---

## Live application

- Live APP : https://atharvamavle-hackathon-uiapp-ps07su.streamlit.app/
- Backend (Render): https://hackathon-24mr.onrender.com/docs#/default/create_session_session_create_post


---

## Project structure

```text
hackathon/
├── agent/                # Core agent logic
     └── __init__.py
     └── core.py
     └── prompts.py
     └── tools.py          
├── api/                   # FastAPI backend
│   └── main.py            # API routes: /session/create, /chat, /health
├── ui/                    # Streamlit UI
│   └── app.py             # Frontend app
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How it works (core flow)

```text
Student selects a GitHub repo (or future: paste text / upload file)
        ↓
Backend creates a session and agent
        ↓
Agent: “What interests you most about this project?”
        ↓
Student answers
        ↓
Agent asks guided questions + gives hints
        ↓
Student builds understanding step-by-step
```

---

## Prerequisites

- Python 3.9+
- Git
- OpenAI API key

---

## Installation & local run

### 1) Clone
```bash
git clone https://github.com/atharvamavle/hackathon.git
cd hackathon
```

### 2) Create and activate venv
**Windows (PowerShell):**
```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Set environment variables (local)
Create a local `.env` file in the repo root:

```env
OPENAI_API_KEY=sk-your-real-key
OPENAI_MODEL=gpt-4o-mini
```

**Important:** Do not commit `.env`.

### 5) Run backend
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Verify:
- http://localhost:8000/health
- http://localhost:8000/docs

### 6) Run Streamlit UI
```bash
streamlit run ui/app.py
```
Open the URL Streamlit prints (usually http://localhost:8501).

---

## Deploy

### Backend on Render
1. Create a Render **Web Service** connected to this repo.
2. Set environment variables:
   - `OPENAI_API_KEY` = your real key
   - `OPENAI_MODEL` = optional
3. Set Health Check Path to: `/health`
4. Deploy.

### UI on Streamlit Community Cloud
In Streamlit app settings → **Secrets**, add:

```toml
API_BASE_URL = "https://hackathon-24mr.onrender.com"
```

In `ui/app.py`, set:

```python
API_BASE = st.secrets["API_BASE_URL"].rstrip("/")
```

---

## API endpoints

- `GET /` — basic status
- `GET /health` — health + whether `OPENAI_API_KEY` is configured
- `POST /session/create` — start a session, returns `session_id` and greeting
- `POST /chat` — send a message, returns model response
- `GET /session/{session_id}/history` — session transcript
- `GET /session/{session_id}/progress` — progress tracking (if enabled)

---

## Troubleshooting

### 401 Incorrect API key
- Make sure `OPENAI_API_KEY` is set (Render env vars for production, `.env` for local).
- Ensure `.env` is not committed and you are not overriding production env vars.

### UI can’t reach backend
- In Streamlit Cloud, `localhost` won’t work.
- Use `API_BASE_URL` secret pointing to your Render URL.

---

## Future improvements

- Repo cloning + indexing: actually clone GitHub repos server-side.
- Retrieval / RAG grounded in real files and code snippets.
- “Explain this file” and “trace call path” tools using AST parsing.
- Better persistence: database for sessions + progress tracking.
- Streaming responses and richer UI.
- Auth + rate limiting + safer CORS defaults.

---

## Author

Atharva Santosh Mavale

Contact: atharvamavale40@gmail.com

---

**Status:** ✅ Live and deployed


[sophiie.com](https://sophiie.com)

---

