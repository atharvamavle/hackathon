import streamlit as st
import requests
import base64

API_BASE = st.secrets["API_BASE_URL"].rstrip("/")

st.set_page_config(page_title="StudyMate", page_icon="🧠", layout="wide")

# ---------- STATE ----------
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_input_value" not in st.session_state:
    st.session_state.chat_input_value = ""

# ---------- GLOBAL STYLE ----------
st.markdown(
    """
    <style>
    .stApp {
        background: #020617;
        color: #e5e7eb;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 1100px;
    }

    .app-title {
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: 0.03em;
    }
    .app-subtitle {
        font-size: 0.85rem;
        opacity: 0.7;
        margin-bottom: 1.4rem;
    }

    /* Cards */
    .left-card, .right-panel {
        background: #020617;
        border-radius: 16px;
        border: 1px solid #111827;
        box-shadow: 0 18px 40px rgba(0,0,0,0.7);
        padding: 18px 20px;
    }
    .left-title {
        font-size: 1.0rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Inputs – flat */
    .stTextInput > div > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div > div,
    .stFileUploader > div {
        background-color: #020617 !important;
        border-radius: 10px !important;
        border: 1px solid #1f2937 !important;
        color: #e5e7eb !important;
        font-size: 0.9rem !important;
    }

    /* Primary buttons */
    .stButton > button {
        border-radius: 999px;
        border: none;
        background: #22c55e;
        color: #020617;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 10px 25px rgba(34,197,94,0.4);
    }
    .stButton > button:hover {
        background: #16a34a;
    }

    /* Secondary buttons */
    .outline-btn > button {
        border-radius: 999px;
        border: 1px solid #4b5563;
        background: transparent;
        color: #e5e7eb;
        font-weight: 500;
        font-size: 0.85rem;
        box-shadow: none;
    }

    /* Chat bubbles */
    .bubble-user {
        background: #0b1120;
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 10px;
        font-size: 0.9rem;
    }
    .bubble-assistant {
        background: #020617;
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 10px;
        border: 1px solid #1f2937;
        font-size: 0.9rem;
    }
    .bubble-header {
        font-size: 0.8rem;
        opacity: 0.7;
        margin-bottom: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
st.markdown('<div class="app-title">🧠 StudyMate</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Learn code through guided discovery from GitHub repos, pasted notes, or uploaded files.</div>',
    unsafe_allow_html=True,
)

# ---------- LAYOUT ----------
left_col, right_col = st.columns([1, 2.4])

# ---------- LEFT: SESSION PANELS ----------
with left_col:
    # Top card: input + start
    st.markdown('<div class="left-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="left-title">📚 Learning Session</div>', unsafe_allow_html=True
    )

    mode = st.radio(
        "What do you want to learn from?",
        ["GitHub repository", "Paste text / notes", "Upload code file (.py, .txt)"],
    )

    github_url = ""
    pasted_text = ""
    file_bytes = None
    file_name = None

    if mode == "GitHub repository":
        github_url = st.text_input(
            "GitHub Repo URL",
            value="https://github.com/pallets/flask",
        )
    elif mode == "Paste text / notes":
        pasted_text = st.text_area(
            "Paste text / notes",
            height=140,
            placeholder="Paste code, documentation, or notes here...",
        )
    else:
        uploaded = st.file_uploader(
            "Upload code file (.py, .txt)",
            type=["py", "txt"],
        )
        if uploaded is not None:
            file_bytes = uploaded.read()
            file_name = uploaded.name
            st.success(f"Loaded file: {file_name}")

    student_name = st.text_input("Your Name", value="Atharva")
    knowledge_level = st.selectbox(
        "Knowledge Level", ["beginner", "intermediate", "advanced"], index=0
    )

    start_btn = st.button("🎓 Start Learning", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Bottom card: status + new session
    st.markdown('<div class="left-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="left-title">📘 Session Status</div>', unsafe_allow_html=True
    )
    if st.session_state.session_id:
        st.success(f"Session Active: {st.session_state.session_id[:8]}...")
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
        if st.button("🔄 New Session", key="new_session", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No active session yet. Start one above to begin.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- HANDLE START ----------
if start_btn:
    try:
        payload = {
            "github_url": github_url,
            "student_name": student_name,
            "knowledge_level": knowledge_level,
            "input_mode": mode,
            "pasted_text": pasted_text or "",
            "file_name": file_name or "",
            "file_content_b64": (
                base64.b64encode(file_bytes).decode("utf-8")
                if file_bytes is not None
                else ""
            ),
        }
        resp = requests.post(f"{API_BASE}/session/create", json=payload)
        if resp.status_code == 200:
            data = resp.json()
            st.session_state.session_id = data["session_id"]
            st.session_state.messages = [
                {"role": "assistant", "content": data["greeting"]}
            ]
            st.success("Session created!")
            st.rerun()
        else:
            st.error(f"Error starting session: {resp.status_code} – {resp.text}")
    except Exception as e:
        st.error(f"Could not reach backend: {e}")

# ---------- RIGHT: CHAT PANEL ----------
with right_col:
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)

    # Chat history
    chat_box = st.container()
    with chat_box:
        for m in st.session_state.messages:
            if m["role"] == "user":
                st.markdown(
                    f'<div class="bubble-user"><div class="bubble-header">You</div>{m["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="bubble-assistant"><div class="bubble-header">StudyMate</div>{m["content"]}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("<br/>", unsafe_allow_html=True)

    if st.session_state.session_id:
        with st.form("chat_form"):
            st.markdown("**What do you want to understand?**")
            user_msg = st.text_area(
                "",
                key="chat_input",
                height=110,
                value=st.session_state.chat_input_value,
                placeholder="Ask about specific functions, architecture, or best practices...",
            )

            col_send, col_clear = st.columns(2)
            with col_send:
                send = st.form_submit_button("💭 Ask", use_container_width=True)
            with col_clear:
                st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
                clear = st.form_submit_button(
                    "🗑 Clear Chat", use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

        # Ask
        if send and user_msg.strip():
            st.session_state.messages.append({"role": "user", "content": user_msg})
            st.session_state.chat_input_value = ""  # clear for next question

            try:
                r = requests.post(
                    f"{API_BASE}/chat",
                    json={
                        "session_id": st.session_state.session_id,
                        "message": user_msg,
                    },
                )
                if r.status_code == 200:
                    data = r.json()
                    st.session_state.messages.append(
                        {"role": "assistant", "content": data["response"]}
                    )
                else:
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": f"Sorry, API error: {r.status_code}",
                        }
                    )
            except Exception as e:
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": f"Sorry, I couldn’t reach the backend: {e}",
                    }
                )
            st.rerun()

        # Clear Chat
        if clear:
            if st.session_state.messages:
                st.session_state.messages = [st.session_state.messages[0]]
            st.session_state.chat_input_value = ""
            st.rerun()
    else:
        st.info("Start a learning session on the left to begin chatting with StudyMate.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("<br/>", unsafe_allow_html=True)
st.caption("Made for Sophiie Hackathon 2026 • Learn code through Questioning discovery")
