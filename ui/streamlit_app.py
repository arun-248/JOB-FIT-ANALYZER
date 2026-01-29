"""
Premium Job Fit Analyzer - Fixed Dark Blue Version
"""

import streamlit as st
import sys
from pathlib import Path
import json
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.pipeline import CandidateIntelligencePipeline

# Page config
st.set_page_config(
    page_title="Job Fit Analyzer",
    page_icon="🎯",
    layout="wide"
)

# Dark Blue Gradient CSS - FIXED VERSION
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* CONSISTENTLY VERY DARK BLUE BACKGROUND */
    .stApp {
        background: linear-gradient(180deg, #0a0e27 0%, #0f1629 50%, #1a1f3a 100%);
        background-attachment: fixed;
    }
    
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    /* Clean header */
    .header-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        animation: fadeInDown 0.8s ease;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* MAIN HEADING - Cyan to white gradient */
    .header-box h1 {
        background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        margin: 0 !important;
        letter-spacing: -1px;
    }
    
    /* SUBTITLE - Emerald to cyan gradient */
    .header-box .subtitle {
        background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 0.8rem !important;
    }
    
    /* Upload Documents heading - Yellow/Orange gradient */
    .upload-heading {
        background: linear-gradient(135deg, #fbbf24 0%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        margin: 2rem 0 1.5rem 0 !important;
        text-align: center;
    }
    
    /* Section headings - different colors */
    .section-title-purple {
        background: linear-gradient(135deg, #a78bfa 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        margin: 2rem 0 1.5rem 0 !important;
    }
    
    .section-title-cyan {
        background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        margin: 2rem 0 1.5rem 0 !important;
    }
    
    .section-title-green {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        margin: 2rem 0 1.5rem 0 !important;
    }
    
    .section-title-pink {
        background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        margin: 2rem 0 1.5rem 0 !important;
    }
    
    /* Premium input cards - PROPER BOXES */
    .input-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.4s ease;
        animation: fadeInUp 0.6s ease;
        margin-bottom: 1.5rem;
        position: relative;
    }
    
    /* Ensure all Streamlit elements inside input-card are contained */
    .input-card * {
        position: relative;
        z-index: 1;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .input-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
    }
    
    /* Resume card - Cyan border and glow */
    .resume-card {
        border-color: rgba(6, 182, 212, 0.5);
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(34, 211, 238, 0.08) 100%);
    }
    
    .resume-card:hover {
        border-color: rgba(6, 182, 212, 0.8);
        box-shadow: 0 20px 50px rgba(6, 182, 212, 0.3);
    }
    
    .resume-card h3 {
        color: #22d3ee !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1.2rem !important;
        margin-top: 0 !important;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(34, 211, 238, 0.6);
        background: none !important;
        -webkit-text-fill-color: #22d3ee !important;
        text-shadow: 0 0 10px rgba(34, 211, 238, 0.5);
    }
    
    /* JD card - Emerald border and glow */
    .jd-card {
        border-color: rgba(16, 185, 129, 0.5);
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(52, 211, 153, 0.08) 100%);
    }
    
    .jd-card:hover {
        border-color: rgba(16, 185, 129, 0.8);
        box-shadow: 0 20px 50px rgba(16, 185, 129, 0.3);
    }
    
    .jd-card h3 {
        color: #34d399 !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1.2rem !important;
        margin-top: 0 !important;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(52, 211, 153, 0.6);
        background: none !important;
        -webkit-text-fill-color: #34d399 !important;
        text-shadow: 0 0 10px rgba(52, 211, 153, 0.5);
    }
    
    /* Text visibility */
    p, span, label, div {
        color: white !important;
    }
    
    h3 {
        color: white !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        margin-top: 0 !important;
    }
    
    h4 {
        background: linear-gradient(135deg, #fbbf24 0%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
    }
    
    /* Radio buttons */
    .stRadio > label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    .stRadio [role="radiogroup"] {
        background: rgba(255, 255, 255, 0.06);
        padding: 0.6rem;
        border-radius: 10px;
        gap: 0.8rem;
    }
    
    /* File uploader - GREY/ASH COLOR FOR DRAG DROP TEXT */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px dashed rgba(255, 255, 255, 0.25) !important;
        border-radius: 14px !important;
        padding: 1.8rem !important;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }
    
    .stFileUploader label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* DRAG AND DROP TEXT - GREY/ASH COLOR */
    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #9ca3af !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] span {
        color: #9ca3af !important;
    }
    
    .stFileUploader small {
        color: #9ca3af !important;
    }
    
    /* Text area */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 2px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.2);
    }
    
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.35) !important;
    }
    
    .stTextArea label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* STUNNING analyze button */
    .stButton > button {
        background: linear-gradient(135deg, #f59e0b 0%, #fb923c 50%, #f97316 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1rem 3rem !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        box-shadow: 0 10px 30px rgba(251, 146, 60, 0.4) !important;
        transition: all 0.4s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(251, 146, 60, 0.6) !important;
        background: linear-gradient(135deg, #fb923c 0%, #f97316 100%) !important;
    }
    
    /* Premium tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(10px);
        padding: 0.6rem;
        border-radius: 14px;
        gap: 0.4rem;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.6) !important;
        border-radius: 10px;
        padding: 0.75rem 1.3rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.06);
        color: white !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4);
    }
    
    /* Stunning score card */
    .score-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.06) 100%);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        padding: 2.5rem;
        border-radius: 24px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin: 2rem 0;
        animation: scaleIn 0.6s ease;
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .score-value {
        font-size: 4.5rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
    }
    
    .score-label {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    .score-recommendation {
        background: rgba(255, 255, 255, 0.12);
        padding: 0.9rem 2rem;
        border-radius: 12px;
        font-size: 1.15rem;
        font-weight: 700;
        color: white;
        margin-top: 1rem;
    }
    
    /* Component boxes */
    .component-box {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.12);
        transition: all 0.3s ease;
    }
    
    .component-box:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: white !important;
        font-weight: 800 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }
    
    /* Info boxes */
    .info-box, .success-box, .warning-box, .danger-box {
        backdrop-filter: blur(10px);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border-left-color: #3b82f6;
    }
    
    .success-box {
        background: rgba(34, 197, 94, 0.1);
        border-left-color: #22c55e;
    }
    
    .warning-box {
        background: rgba(251, 146, 60, 0.1);
        border-left-color: #fb923c;
    }
    
    .danger-box {
        background: rgba(239, 68, 68, 0.1);
        border-left-color: #ef4444;
    }
    
    .info-box:hover, .success-box:hover, .warning-box:hover, .danger-box:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Skill pills */
    .skill-pill {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.7) 0%, rgba(34, 211, 238, 0.7) 100%);
        color: white;
        padding: 0.5rem 1.1rem;
        border-radius: 18px;
        margin: 0.35rem;
        display: inline-block;
        font-weight: 600;
        font-size: 0.88rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    
    .skill-pill:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(6, 182, 212, 0.4);
        background: linear-gradient(135deg, rgba(34, 211, 238, 0.8) 0%, rgba(6, 182, 212, 0.8) 100%);
    }
    
    /* Gap cards */
    .gap-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border-left: 4px solid;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .gap-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateX(5px);
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.7) 0%, rgba(34, 211, 238, 0.7) 100%) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 20px rgba(6, 182, 212, 0.4) !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        margin: 2.5rem 0 !important;
    }
    
    /* JSON viewer */
    .stJson {
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
if 'report' not in st.session_state:
    st.session_state.report = None


def initialize_pipeline():
    """Initialize pipeline"""
    if st.session_state.pipeline is None:
        with st.spinner("🔄 Loading AI models..."):
            st.session_state.pipeline = CandidateIntelligencePipeline()
        st.success("✅ System Ready!")


def display_results(report):
    """Display analysis results"""
    
    score = report['overall_score']
    recommendation = report['recommendation']
    
    # Color based on score
    if score >= 75:
        score_gradient = "linear-gradient(135deg, #22c55e 0%, #16a34a 100%)"
    elif score >= 60:
        score_gradient = "linear-gradient(135deg, #fb923c 0%, #f97316 100%)"
    else:
        score_gradient = "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
    
    st.markdown(f"""
        <div class="score-card">
            <div class="score-label">Overall Match Score</div>
            <div class="score-value" style="background: {score_gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{score}</div>
            <div class="score-recommendation">{recommendation}</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 0.92rem; margin-top: 1rem; font-weight: 500;">
                Confidence: {report['confidence']}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # COLORFUL HEADING - Purple
    st.markdown('<h2 class="section-title-purple">📊 Performance Breakdown</h2>', unsafe_allow_html=True)
    
    cols = st.columns(5)
    scores = report['component_scores']
    icons = ['🎯', '💼', '📝', '🎓', '📚']
    
    score_keys = list(scores.keys())
    labels = []
    for key in score_keys:
        if 'skill' in key.lower():
            labels.append('Skills')
        elif 'experience' in key.lower():
            labels.append('Experience')
        elif 'relevance' in key.lower():
            labels.append('Relevance')
        elif 'education' in key.lower():
            labels.append('Education')
        elif 'learning' in key.lower():
            labels.append('Learning')
        else:
            labels.append(key.replace('_', ' ').title())
    
    for idx, (key, icon, label) in enumerate(zip(score_keys, icons, labels)):
        with cols[idx]:
            value = scores[key]
            if value >= 75:
                color = "#22c55e"
            elif value >= 60:
                color = "#fb923c"
            else:
                color = "#ef4444"
            
            st.markdown(f"""
                <div class="component-box">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="font-size: 0.82rem; color: rgba(255,255,255,0.65); margin-bottom: 0.5rem; font-weight: 600;">
                        {label}
                    </div>
                    <div style="font-size: 2rem; font-weight: 800; color: {color};">
                        {value}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Skills Analysis", "💼 Experience Profile", "💪 Strengths & Gaps", "📄 Full Report"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Skills Found", report['skill_analysis']['total_skills_found'])
        with col2:
            st.metric("Match Rate", f"{report['skill_analysis']['match_percentage']}%")
        with col3:
            st.metric("Missing Skills", len(report['skill_analysis']['missing_skills']))
        
        st.markdown('<h4 style="margin-top: 1.5rem;">✅ Matched Skills</h4>', unsafe_allow_html=True)
        matched = report['skill_analysis']['matched_skills'][:15]
        if matched:
            pills = ' '.join([f'<span class="skill-pill">{s}</span>' for s in matched])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.info("No matched skills found")
        
        st.markdown('<h4 style="margin-top: 1.5rem;">⚠️ Skill Gaps to Address</h4>', unsafe_allow_html=True)
        if report['top_gaps']:
            for gap in report['top_gaps'][:5]:
                colors = {'easy': '#22c55e', 'medium': '#fb923c', 'hard': '#ef4444'}
                emojis = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}
                
                st.markdown(f"""
                    <div class="gap-card" style="border-left-color: {colors[gap['difficulty']]};">
                        <strong style="font-size: 1.05rem;">{emojis[gap['difficulty']]} {gap['skill']}</strong><br>
                        <small style="color: rgba(255,255,255,0.6);">
                            {gap['category'].replace('_', ' ').title()} • 
                            {gap['difficulty'].upper()} • 
                            ~{gap['learning_days']} days to learn
                        </small>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No significant skill gaps identified")
    
    with tab2:
        exp = report['experience_analysis']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Experience", f"{exp['total_years']} years")
        with col2:
            st.metric("Seniority Level", exp['seniority_level'].title())
        with col3:
            st.metric("Number of Roles", exp['number_of_roles'])
        
        if exp['total_years'] > 0:
            st.markdown(f"""
                <div class="success-box">
                    <strong>✅ Experienced Professional</strong><br>
                    Has {exp['total_years']} years of experience at {exp['seniority_level']} level
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="info-box">
                    <strong>ℹ️ Entry Level Candidate</strong><br>
                    Limited professional experience. Likely fresh graduate or career changer.
                </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 class="section-title-green">💪 Key Strengths</h2>', unsafe_allow_html=True)
        if report['strengths']:
            for strength in report['strengths']:
                st.markdown(f"""
                    <div class="success-box">
                        <strong>✅ {strength}</strong>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No significant strengths identified")
        
        st.markdown('<h2 class="section-title-cyan">🎯 Hiring Recommendation</h2>', unsafe_allow_html=True)
        
        if score >= 75:
            st.markdown("""
                <div class="success-box">
                    <strong>✅ STRONG HIRE - Excellent Match</strong><br>
                    This candidate demonstrates exceptional alignment with role requirements. 
                    Recommend immediate interview scheduling.
                </div>
            """, unsafe_allow_html=True)
        elif score >= 60:
            st.markdown("""
                <div class="warning-box">
                    <strong>⚠️ POTENTIAL FIT - Good Candidate</strong><br>
                    Solid candidate with some skill gaps. Consider for phone screen to assess 
                    learning ability and cultural fit.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="danger-box">
                    <strong>⚠️ NOT RECOMMENDED - Significant Gaps</strong><br>
                    Substantial skill and experience gaps present. Would require extensive 
                    training and onboarding support.
                </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.json(report)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download JSON Report",
                json.dumps(report, indent=2),
                f"candidate_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json",
                use_container_width=True
            )
        
        with col2:
            summary = f"""CANDIDATE INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERALL SCORE: {score}/100
RECOMMENDATION: {recommendation}
CONFIDENCE: {report['confidence']}

COMPONENT SCORES:
- Skills Match: {report['skill_analysis']['match_percentage']}%
- Experience: {exp['total_years']} years
- Seniority: {exp['seniority_level'].title()}

MATCHED SKILLS: {len(report['skill_analysis']['matched_skills'])}
MISSING SKILLS: {len(report['skill_analysis']['missing_skills'])}
"""
            st.download_button(
                "📥 Download Summary",
                summary,
                f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                use_container_width=True
            )


def main():
    """Main application"""
    
    # Clean header
    st.markdown("""
        <div class="header-box">
            <h1>JOB FIT ANALYZER</h1>
            <div class="subtitle">AI-Powered Candidate Intelligence Platform</div>
        </div>
    """, unsafe_allow_html=True)
    
    initialize_pipeline()
    
    st.markdown("---")
    
    # Upload Documents heading
    st.markdown('<h2 class="upload-heading">📤 Upload Documents</h2>', unsafe_allow_html=True)
    
    # TWO SEPARATE INPUT BOXES - Side by side
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        # Create the resume box with heading inside
        st.markdown("""
            <div class="input-card resume-card">
                <h3>📄 Resume / CV</h3>
            """, unsafe_allow_html=True)
        
        resume_option = st.radio(
            "Input method:", 
            ["Upload File", "Paste Text"], 
            key="resume_method", 
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if resume_option == "Upload File":
            resume_file = st.file_uploader(
                "Upload resume file (PDF or TXT)", 
                type=['pdf', 'txt'], 
                key="resume_file"
            )
            resume_text = None
        else:
            resume_text = st.text_area(
                "Resume Content", 
                height=220, 
                placeholder="Paste the complete resume content here...",
                key="resume_text"
            )
            resume_file = None
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Create the JD box with heading inside
        st.markdown("""
            <div class="input-card jd-card">
                <h3>📋 Job Description</h3>
            """, unsafe_allow_html=True)
        
        jd_option = st.radio(
            "Input method:", 
            ["Upload File", "Paste Text"], 
            key="jd_method", 
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if jd_option == "Upload File":
            jd_file = st.file_uploader(
                "Upload job description file (PDF or TXT)", 
                type=['pdf', 'txt'], 
                key="jd_file"
            )
            jd_text = None
        else:
            jd_text = st.text_area(
                "Job Description Content", 
                height=220, 
                placeholder="Paste the complete job description here...",
                key="jd_text"
            )
            jd_file = None
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analyze Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze = st.button("🚀 ANALYZE CANDIDATE", use_container_width=True)
    
    # Analysis
    if analyze:
        has_resume = resume_file or (resume_text and resume_text.strip())
        has_jd = jd_file or (jd_text and jd_text.strip())
        
        if not has_resume or not has_jd:
            st.error("⚠️ Please provide both Resume and Job Description")
            return
        
        import tempfile
        temp_dir = Path(tempfile.gettempdir())
        
        try:
            # Handle resume
            if resume_file:
                resume_path = temp_dir / f"resume_{resume_file.name}"
                with open(resume_path, 'wb') as f:
                    f.write(resume_file.getbuffer())
            else:
                resume_path = temp_dir / "resume.txt"
                with open(resume_path, 'w', encoding='utf-8') as f:
                    f.write(resume_text)
            
            # Handle JD
            if jd_file:
                jd_path = temp_dir / f"jd_{jd_file.name}"
                with open(jd_path, 'wb') as f:
                    f.write(jd_file.getbuffer())
            else:
                jd_path = temp_dir / "jd.txt"
                with open(jd_path, 'w', encoding='utf-8') as f:
                    f.write(jd_text)
            
            # Run analysis
            with st.spinner("🔄 Analyzing candidate... Please wait"):
                report = st.session_state.pipeline.analyze(resume_path, jd_path)
                st.session_state.report = report
                
                resume_path.unlink()
                jd_path.unlink()
            
            st.success("✅ Analysis Complete!")
            st.balloons()
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return
    
    # Display results
    if st.session_state.report:
        st.markdown("---")
        display_results(st.session_state.report)


if __name__ == "__main__":
    main()