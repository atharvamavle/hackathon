# Sophiie AI Agents Hackathon 2026

## Your Submission

> **Instructions:** Fill out this section in your forked repo. This is what judges will see first.

### Participant

| Field | Your Answer |
|-------|-------------|
| **Name** | |
| **University / Employer** | |

### Project

| Field | Your Answer |
|-------|-------------|
| **Project Name** | |
| **One-Line Description** | |
| **Demo Video Link** | |
| **Tech Stack** | |
| **AI Provider(s) Used** | |

# StudyMate — Learn Any GitHub Repo With a Socratic AI Tutor

StudyMate is a web app that helps you understand unfamiliar codebases by chatting with an AI “study buddy” that teaches using the Socratic method (questions, guided hints, and progressive explanations). It’s built for hackathon speed, but structured like a real product: a FastAPI backend + Streamlit UI.

Repo: https://github.com/atharvamavle/hackathon.git

---

## The problem we solved

Reading a new repository is hard because you don’t know:
- Where to start.
- Which files matter.
- How components connect.
- What to ask next.

StudyMate turns a repo URL into an interactive learning session, so you can ask questions like “What does this function do?”, “How does the architecture work?”, and “What should I read next?”

---

## What we built

### Components
- `api/` — FastAPI backend with session creation and chat endpoints.
- `agent/` — core teaching agent logic (LLM wrapper + prompts + tools).
- `ui/` — Streamlit front-end for a polished chat UX.

This repository is forked from the Sophiie AI Agents Hackathon repo template.

---

## Live deployment

- Backend (Render): https://hackathon-24mr.onrender.com
- Backend docs: https://hackathon-24mr.onrender.com/docs
- Health check: https://hackathon-24mr.onrender.com/health

---

## Tech stack
- Python
- FastAPI
- Streamlit
- OpenAI API
- LangChain `ChatOpenAI`

---

## How to run locally

### 1) Clone & install
```bash
git clone https://github.com/atharvamavle/hackathon.git
cd hackathon
python -m venv .venv
# Windows:
. .venv/Scripts/activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 2) Configure environment variables
Create a `.env` locally (do not commit it):
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

### 3) Run the backend (FastAPI)
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Verify:
- http://localhost:8000/health
- http://localhost:8000/docs

### 4) Run the UI (Streamlit)
```bash
streamlit run ui/app.py
```

---

## How to deploy (Render + Streamlit Community Cloud)

### Backend on Render
1. Create a new Render “Web Service” connected to this GitHub repo.
2. Set env vars in Render:
   - `OPENAI_API_KEY` (required)
   - `OPENAI_MODEL` (optional)
3. Set the health check path to `/health`.

### UI on Streamlit Community Cloud
1. Create a new Streamlit app pointing to `ui/app.py`.
2. Add Streamlit secrets:
```toml
API_BASE_URL = "https://hackathon-24mr.onrender.com"
```
3. In `ui/app.py`, set `API_BASE = st.secrets["API_BASE_URL"].rstrip("/")`.

---

## API endpoints

- `GET /health`
- `POST /session/create`
- `POST /chat`
- `GET /session/{session_id}/history`
- `GET /session/{session_id}/progress`

---

## Future work
- Clone + index GitHub repos server-side and add retrieval (RAG) grounded in actual files.
- Add streaming responses, citations, and “trace call path” / “explain file” tools.
- Persist sessions and progress tracking in a database.
- Add auth, rate limiting, and safer CORS defaults.

---

## Security
- Never commit API keys.
- Store secrets in Render/Streamlit secret managers.
- Rotate keys if they were ever pushed to GitHub.

---

## Credits
Built for the Sophiie AI Agents Hackathon 2026.


[sophiie.com](https://sophiie.com)

---

**Good luck. Build something that makes us say "wow."**
