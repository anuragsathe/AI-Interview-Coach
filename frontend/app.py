import streamlit as st
import requests
import json
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Persona Coach | Interview Mastery",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Premium Global Styles ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    :root {
        --primary: #6366f1;
        --secondary: #a855f7;
        --accent: #f43f5e;
        --background: #0f172a;
        --surface: #1e293b;
        --text: #f8fafc;
        --text-dim: #94a3b8;
    }

    .stApp {
        background-color: var(--background);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, h4, .stSlider label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        background: linear-gradient(to right, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glassmorphism Containers */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    .glass-card:hover {
        border: 1px solid rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
    }

    /* Custom Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        width: 100%;
        height: 3.5rem;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -10px var(--primary);
    }

    .stButton > button:active {
        transform: scale(0.98);
    }

    /* Secondary/Outline Buttons */
    div.stButton > button.secondary-btn {
        background: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: var(--text) !important;
    }

    /* Input Styling */
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: var(--text) !important;
        font-size: 1.1rem !important;
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, var(--primary), var(--secondary)) !important;
    }

    /* Reports Styles */
    .score-badge {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .feedback-pill {
        padding: 1rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        border: 1px solid transparent;
    }

    .strength-pill {
        background: rgba(34, 197, 94, 0.1);
        border-color: rgba(34, 197, 94, 0.2);
    }
    
    .weakness-pill {
        background: rgba(239, 68, 68, 0.1);
        border-color: rgba(239, 68, 68, 0.2);
    }

    .suggestion-pill {
        background: rgba(245, 158, 11, 0.1);
        border-color: rgba(245, 158, 11, 0.2);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeIn 0.5s ease forwards;
    }
</style>
""", unsafe_allow_html=True)

# --- Constants & State Management ---
API_BASE_URL = "http://localhost:8000/api"

def init_session():
    states = {
        "step": "landing",
        "session_id": None,
        "questions": [],
        "current_q_idx": 0,
        "results": [],
        "final_report": None,
        "difficulty": "Intermediate",
        "selected_roles": []
    }
    for key, val in states.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# --- Logic Handlers ---
def api_request(method, endpoint, payload=None):
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        if method == "POST":
            response = requests.post(url, json=payload, timeout=30)
        else:
            response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection Failed: {str(e)}")
        return None

def start_interview_process():
    if not st.session_state.selected_roles:
        st.warning("Please select at least one role to proceed.")
        return

    payload = {"roles": st.session_state.selected_roles}
    data = api_request("POST", "generate-questions", payload)
    
    if data:
        st.session_state.questions = data["questions"]
        st.session_state.session_id = data["session_id"]
        st.session_state.step = "interview"
        st.session_state.current_q_idx = 0
        st.rerun()

def submit_answer(answer):
    if not answer.strip():
        st.warning("Please share your thoughts before proceeding.")
        return

    payload = {
        "session_id": st.session_state.session_id,
        "question_index": st.session_state.current_q_idx,
        "answer": answer
    }
    
    data = api_request("POST", "evaluate-answer", payload)
    if data:
        st.session_state.current_q_idx += 1
        if st.session_state.current_q_idx >= len(st.session_state.questions):
            show_final_report()
        else:
            st.rerun()

def show_final_report():
    data = api_request("POST", "get-final-report", {"session_id": st.session_state.session_id})
    if data:
        st.session_state.final_report = data
        st.session_state.step = "report"
        st.rerun()

def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- Component Functions ---
def render_header():
    cols = st.columns([1, 4, 1])
    with cols[1]:
        st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-bottom: 0;'>AI Persona Coach</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: var(--text-dim); font-size: 1.2rem;'>Master your interview skills with real-time AI feedback</p>", unsafe_allow_html=True)
        st.write("")

def ensure_list_to_markdown(val):
    if not val:
        return ""
    if isinstance(val, list):
        return "\n".join([f"• {i}" for i in val])
    if isinstance(val, dict):
        # Recursively format dict keys into a clean string
        return "\n".join([f"**{str(k).replace('_', ' ').title()}:** {ensure_list_to_markdown(v)}" for k, v in val.items()])
    return str(val)

# --- UI Views ---

# 1. Landing / Role Selection
if st.session_state.step == "landing":
    render_header()
    
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown('<div class="glass-card animate-in">', unsafe_allow_html=True)
        st.subheader("Configure Your Session")
        
        roles_list = ["Banking & Finance", "IT / Software", "Data Science", "AI Engineer", "Teaching", "Sales / Marketing", "Product Manager", "UI/UX Designer", "DevOps Engineer"]
        st.session_state.selected_roles = st.multiselect("Target Roles", roles_list, placeholder="Select your career paths...")
        
        st.session_state.difficulty = st.select_slider("Interview Rigor", options=["Graduate", "Associate", "Senior", "Executive"], value="Associate")
        
        st.write("")
        if st.button("Generate Interview Session"):
            start_interview_process()
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Benefits / Features
        fcols = st.columns(3)
        with fcols[0]:
            st.markdown("🎯 **Targeted**\nRole-specific challenges")
        with fcols[1]:
            st.markdown("🧠 **Smart**\nDeep-dive analysis")
        with fcols[2]:
            st.markdown("📈 **Actionable**\nPersonalized roadmaps")

# 2. Main Interview Flow
elif st.session_state.step == "interview":
    render_header()
    
    total = len(st.session_state.questions)
    curr = st.session_state.current_q_idx
    
    # Progress Top Bar
    st.progress((curr) / total)
    st.markdown(f"<p style='text-align: right; color: var(--text-dim);'>Challenge {curr + 1} of {total}</p>", unsafe_allow_html=True)

    cols = st.columns([1, 5, 1])
    with cols[1]:
        st.markdown('<div class="glass-card animate-in">', unsafe_allow_html=True)
        
        # Display Question
        st.markdown(f"<p style='color: var(--primary); font-weight: 600; text-transform: uppercase;'>The Challenge</p>", unsafe_allow_html=True)
        st.markdown(f"### {st.session_state.questions[curr]}")
        st.write("")
        
        # User Answer
        user_input = st.text_area("Your Response", 
                                height=250, 
                                placeholder="Structure your answer clearly. Explain your reasoning and use technical terms where applicable...",
                                key=f"q_{curr}")
        
        st.write("")
        bcols = st.columns([2, 1, 2])
        with bcols[0]:
            if st.button("Submit Response"):
                submit_answer(user_input)
        with bcols[2]:
            if st.button("End Session Early", help="Calculate results based on completed questions"):
                show_final_report()
                
        st.markdown('</div>', unsafe_allow_html=True)

# 3. Comprehensive Report View
elif st.session_state.step == "report":
    if "balloons_triggered" not in st.session_state:
        st.balloons()
        st.session_state.balloons_triggered = True

    report = st.session_state.final_report
    score = int(report.get('avg_score', 0))
    feedback = report.get('overall_feedback', {})
    
    # Header
    cols = st.columns([2, 1])
    with cols[0]:
        st.markdown("## 📊 Performance Analytics")
        st.markdown("Your comprehensive career readiness report is ready.")
    with cols[1]:
        if st.button("Start New Session", key="new_session_top"):
            reset_app()

    # Score Hero Section
    st.markdown('<div class="glass-card animate-in">', unsafe_allow_html=True)
    scols = st.columns([1, 2])
    with scols[0]:
        st.markdown("<p style='text-transform: uppercase; color: var(--text-dim); letter-spacing: 2px;'>Overall Rank</p>", unsafe_allow_html=True)
        st.markdown(f"<span class='score-badge'>{score}%</span>", unsafe_allow_html=True)
        
        perf_text = "EXPERT" if score >= 85 else "PROFICIENT" if score >= 70 else "DEVELOPING" if score >= 40 else "BEGINNER"
        perf_color = "#22c55e" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
        st.markdown(f"<p style='color: {perf_color}; font-weight: 700; font-size: 1.4rem;'>{perf_text}</p>", unsafe_allow_html=True)
        
    with scols[1]:
        st.markdown("<p style='color: var(--primary); font-weight: 600; text-transform: uppercase; font-size: 0.8rem; margin-bottom: 0.5rem;'>Coach Insights</p>", unsafe_allow_html=True)
        st.markdown("#### Career Coach Executive Summary")
        summary_raw = feedback.get('overall_score_summary', 'Analysis of your performance is complete.')
        if isinstance(summary_raw, (dict, list)):
            st.markdown(ensure_list_to_markdown(summary_raw))
        else:
            st.write(summary_raw)
    st.markdown('</div>', unsafe_allow_html=True)

    # Strengths / Weaknesses Grid
    st.markdown("### 🔍 Technical Deep-Dive")
    grid = st.columns(2)
    
    with grid[0]:
        st.markdown('<div class="feedback-pill strength-pill">', unsafe_allow_html=True)
        st.markdown("#### 🌟 Key Strengths")
        st.write(ensure_list_to_markdown(feedback.get('strengths')))
        st.markdown('</div>', unsafe_allow_html=True)

    with grid[1]:
        st.markdown('<div class="feedback-pill weakness-pill">', unsafe_allow_html=True)
        st.markdown("#### ⚠️ Growth Areas")
        st.write(ensure_list_to_markdown(feedback.get('weak_areas')))
        st.markdown('</div>', unsafe_allow_html=True)

    # Roadmaps
    st.markdown("### 🚀 Strategic Growth Roadmap")
    road_cols = st.columns(2)
    with road_cols[0]:
        st.markdown('<div class="feedback-pill suggestion-pill">', unsafe_allow_html=True)
        st.markdown("#### 💡 Pro Tips for Improvement")
        st.write(ensure_list_to_markdown(feedback.get('suggestions_to_improve')))
        st.markdown('</div>', unsafe_allow_html=True)
        
    with road_cols[1]:
        st.markdown('<div class="glass-card" style="padding: 1.5rem;">', unsafe_allow_html=True)
        st.markdown("#### 📚 Recommended Study Topics")
        st.write(ensure_list_to_markdown(feedback.get('recommended_topics_to_study')))
        st.markdown('</div>', unsafe_allow_html=True)

    # Question-by-Question Breakdown
    st.markdown("<br>### 📍 Granular Response Analysis", unsafe_allow_html=True)
    
    for i, item in enumerate(report.get('per_question', [])):
        with st.expander(f"Question {i+1}: {item['question'][:80]}...", expanded=(i==0)):
            st.markdown(f"**Question:** {item['question']}")
            
            # Sub-grid for q analysis
            qcols = st.columns(2)
            with qcols[0]:
                st.markdown("**Your Answer**")
                st.info(item['user_answer'])
                
                st.markdown(f"**Score:** `{item['score']}/100`")
            
            with qcols[1]:
                st.markdown("**Coach Feedback**")
                st.success(item['feedback'])
                
                st.markdown("**Benchmark Answer**")
                st.caption(item['ideal_answer'])

    st.write("")
    if st.button("Back to Homepage", key="home_btn"):
        reset_app()
    st.write("")
