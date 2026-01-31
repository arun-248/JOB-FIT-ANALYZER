"""
ENHANCED Job Fit Analyzer - COMPLETE UI
Professional version with clean presentation
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

# ═══════════════════════════════════════════════════════════════════════════════
# CSS STYLING
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0a0e27 0%, #0f1629 50%, #1a1f3a 100%);
        background-attachment: fixed;
    }
    
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    .header-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(25px);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
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
    
    .header-box .subtitle {
        background: linear-gradient(135deg, #10b981 0%, #14b8a6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 0.8rem !important;
    }
    
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
    
    .input-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        transition: all 0.4s ease;
        margin-bottom: 1.5rem;
    }
    
    .input-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
    }
    
    .resume-card {
        border-color: rgba(6, 182, 212, 0.5);
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(34, 211, 238, 0.08) 100%);
    }
    
    .resume-card h3 {
        color: #22d3ee !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1.2rem !important;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(34, 211, 238, 0.6);
    }
    
    .jd-card {
        border-color: rgba(16, 185, 129, 0.5);
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(52, 211, 153, 0.08) 100%);
    }
    
    .jd-card h3 {
        color: #34d399 !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1.2rem !important;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(52, 211, 153, 0.6);
    }
    
    p, span, label, div {
        color: white !important;
    }
    
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
    }
    
    .score-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.06) 100%);
        backdrop-filter: blur(25px);
        padding: 2.5rem;
        border-radius: 24px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin: 2rem 0;
    }
    
    .score-value {
        font-size: 4.5rem;
        font-weight: 900;
        margin: 1rem 0;
    }
    
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
    }
    
    .info-box, .success-box, .warning-box, .danger-box {
        backdrop-filter: blur(10px);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid;
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
    
    .skill-pill {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.7) 0%, rgba(34, 211, 238, 0.7) 100%);
        color: white;
        padding: 0.5rem 1.1rem;
        border-radius: 18px;
        margin: 0.35rem;
        display: inline-block;
        font-weight: 600;
        font-size: 0.88rem;
    }
    
    .report-section {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 3px solid rgba(6, 182, 212, 0.6);
    }
    
    .report-section h4 {
        color: #22d3ee !important;
        margin-bottom: 1rem !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# Session State
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


def format_full_report(report):
    """Format report as readable text instead of JSON"""
    
    output = f"""
# 🎯 CANDIDATE INTELLIGENCE REPORT
**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

---

## 📊 OVERALL ASSESSMENT

**Match Score:** {report['overall_score']}/100
**Recommendation:** {report['recommendation']}
**Confidence Level:** {report['confidence']}

---

## 🎯 SKILLS ANALYSIS

**Total Skills Found:** {report['skill_analysis']['total_skills_found']}
**Match Percentage:** {report['skill_analysis']['match_percentage']}%

### ✅ Matched Skills
{', '.join(report['skill_analysis']['matched_skills'][:20]) if report['skill_analysis']['matched_skills'] else 'None'}

### ⚠️ Missing Skills  
{', '.join([gap['skill'] for gap in report['skill_analysis']['missing_skills'][:15]]) if report['skill_analysis']['missing_skills'] else 'None'}

---

## 💼 EXPERIENCE PROFILE

**Total Years:** {report['experience_analysis']['total_years']}
**Seniority Level:** {report['experience_analysis']['seniority_level'].title()}
**Number of Roles:** {report['experience_analysis']['number_of_roles']}

---

## 📈 COMPONENT SCORES
"""
    
    for key, value in report['component_scores'].items():
        score_name = key.replace('_', ' ').title()
        output += f"\n**{score_name}:** {value}/100"
    
    output += "\n\n---\n\n## 💪 KEY STRENGTHS\n"
    if report.get('strengths'):
        for strength in report['strengths']:
            output += f"\n✅ {strength}"
    else:
        output += "\nNo significant strengths identified"
    
    output += "\n\n---\n\n## 🎯 CRITICAL SKILL GAPS\n"
    if report.get('top_gaps'):
        for gap in report['top_gaps'][:5]:
            output += f"\n⚠️ **{gap['skill']}** - {gap['difficulty'].upper()} ({gap['learning_days']} days to learn)"
    else:
        output += "\nNo critical gaps identified"
    
    # Interview Questions
    if 'interview_questions' in report:
        output += "\n\n---\n\n## 💬 INTERVIEW QUESTIONS\n"
        questions = report['interview_questions']
        
        if questions.get('verification_questions'):
            output += "\n### Verification Questions:\n"
            for i, q in enumerate(questions['verification_questions'], 1):
                output += f"\n{i}. {q['question']}"
        
        if questions.get('depth_questions'):
            output += "\n\n### Depth Questions:\n"
            for i, q in enumerate(questions['depth_questions'], 1):
                output += f"\n{i}. {q['question']}"
    
    # Knowledge Graph
    if 'knowledge_graph' in report:
        output += "\n\n---\n\n## 🕸️ SKILL READINESS ANALYSIS\n"
        graph = report['knowledge_graph']
        
        if graph.get('readiness_analysis'):
            for skill_data in graph['readiness_analysis'][:5]:
                output += f"\n**{skill_data['skill']}:** {skill_data['readiness_score']}% ready"
    
    # Depth Analysis
    if 'depth_analysis' in report:
        output += "\n\n---\n\n## 🔍 TOP SKILLS BY DEPTH\n"
        depth = report['depth_analysis']
        
        if depth.get('top_skills'):
            for i, skill in enumerate(depth['top_skills'][:5], 1):
                output += f"\n{i}. **{skill['skill']}** - Depth Score: {skill['depth_score']}/100"
                output += f"\n   Evidence: {'⭐' * skill['evidence_strength']} | Context: {skill['context_quality']}"
    
    # Retention Predictions
    if 'retention_predictions' in report:
        output += "\n\n---\n\n## 🧠 RETENTION FORECAST\n"
        predictions = report['retention_predictions']
        
        high = len([p for p in predictions if p['retention_probability'] >= 70])
        medium = len([p for p in predictions if 40 <= p['retention_probability'] < 70])
        low = len([p for p in predictions if p['retention_probability'] < 40])
        
        output += f"\n**High Retention Skills:** {high}"
        output += f"\n**Medium Retention Skills:** {medium}"
        output += f"\n**Low Retention Skills:** {low}"
        
        if predictions:
            output += "\n\n### Detailed Predictions:\n"
            for pred in predictions[:5]:
                output += f"\n**{pred['skill']}:** {pred['retention_probability']}% retention probability"
                output += f"\n   Category: {pred['retention_category'].upper()}"
    
    output += "\n\n---\n\n## 🎯 HIRING RECOMMENDATION\n\n"
    
    score = report['overall_score']
    if score >= 75:
        output += "✅ **STRONG HIRE** - Excellent match for the role. Proceed to interview."
    elif score >= 60:
        output += "⚠️ **POTENTIAL FIT** - Good candidate with some gaps. Consider for phone screen."
    else:
        output += "❌ **NOT RECOMMENDED** - Significant gaps present. May not be suitable."
    
    output += "\n\n---\n\n*End of Report*"
    
    return output


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
    
    # Score Card
    st.markdown(f"""
        <div class="score-card">
            <div style="font-size: 0.95rem; color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 2px; font-weight: 600;">
                Overall Match Score
            </div>
            <div class="score-value" style="background: {score_gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {score}
            </div>
            <div style="background: rgba(255,255,255,0.12); padding: 0.9rem 2rem; border-radius: 12px; font-size: 1.15rem; font-weight: 700; margin-top: 1rem;">
                {recommendation}
            </div>
            <div style="color: rgba(255,255,255,0.6); font-size: 0.92rem; margin-top: 1rem; font-weight: 500;">
                Confidence: {report['confidence']}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Performance Breakdown
    st.markdown("## 📊 Performance Breakdown")
    
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
        elif 'relevance' in key.lower() or 'semantic' in key.lower():
            labels.append('Semantic')
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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "🎯 Skills Analysis",
        "💼 Experience Profile",
        "💪 Strengths & Gaps",
        "📋 Recommendations",
        "💬 Interview Questions",
        "🕸️ Knowledge Graph",
        "🔍 Skill Depth",
        "🧠 Retention Forecast",
        "📄 Full Report"
    ])
    
    # TAB 1: Skills Analysis
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Skills Found", report['skill_analysis']['total_skills_found'])
        with col2:
            st.metric("Match Rate", f"{report['skill_analysis']['match_percentage']}%")
        with col3:
            st.metric("Missing Skills", len(report['skill_analysis']['missing_skills']))
        
        st.markdown("### ✅ Matched Skills")
        matched = report['skill_analysis']['matched_skills'][:15]
        if matched:
            pills = ' '.join([f'<span class="skill-pill">{s}</span>' for s in matched])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.info("No matched skills found")
        
        st.markdown("### ⚠️ Skill Gaps to Address")
        if report.get('top_gaps'):
            for gap in report['top_gaps'][:5]:
                colors = {'easy': '#22c55e', 'medium': '#fb923c', 'hard': '#ef4444'}
                emojis = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}
                
                st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 12px; 
                                margin: 0.8rem 0; border-left: 4px solid {colors[gap['difficulty']]};">
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
    
    # TAB 2: Experience Profile
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
    
    # TAB 3: Strengths & Gaps
    with tab3:
        st.markdown("## 💪 Key Strengths")
        if report.get('strengths'):
            for strength in report['strengths']:
                st.markdown(f"""
                    <div class="success-box">
                        <strong>✅ {strength}</strong>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No significant strengths identified")
        
        st.markdown("## 🎯 Hiring Recommendation")
        
        if score >= 75:
            st.markdown("""
                <div class="success-box">
                    <strong>✅ STRONG HIRE - Excellent Match</strong><br>
                    This candidate demonstrates exceptional alignment with role requirements.
                </div>
            """, unsafe_allow_html=True)
        elif score >= 60:
            st.markdown("""
                <div class="warning-box">
                    <strong>⚠️ POTENTIAL FIT - Good Candidate</strong><br>
                    Solid candidate with some skill gaps. Consider for phone screen.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="danger-box">
                    <strong>⚠️ NOT RECOMMENDED - Significant Gaps</strong><br>
                    Substantial skill and experience gaps present.
                </div>
            """, unsafe_allow_html=True)
    
    # TAB 4: Recommendations
    with tab4:
        st.markdown("## 💡 Personalized Recommendations")
        
        if 'advanced_recommendations' not in report:
            st.info("Advanced recommendations will be available after pipeline enhancement")
        else:
            recs = report['advanced_recommendations']
            
            st.markdown("### 🔑 Missing Keywords for ATS")
            keywords = recs.get('keyword_suggestions', {})
            if keywords.get('missing_keywords'):
                missing_kw = ', '.join(keywords['missing_keywords'][:8])
                st.warning(f"**Add these:** {missing_kw}")
                
                if keywords.get('recommendations'):
                    for rec in keywords['recommendations'][:5]:
                        st.markdown(f"• {rec}")
            else:
                st.success("✅ All important keywords present")
            
            st.markdown("### 🎯 Job-Specific Advice")
            job_spec = recs.get('job_specific', {})
            if job_spec.get('priority_actions'):
                for action in job_spec['priority_actions']:
                    st.markdown(f"✅ {action}")
    
    # TAB 5: Interview Questions
    with tab5:
        st.markdown("## 💬 Interview Questions")
        
        if 'interview_questions' not in report:
            st.info("💡 Interview questions will be generated when using the enhanced pipeline")
            st.markdown("""
            **This feature will auto-generate:**
            - Verification questions to check resume claims
            - Depth questions to test technical knowledge
            - Practical scenario-based questions
            - Red flag detection for inconsistencies
            """)
        else:
            questions = report['interview_questions']
            
            st.markdown("### ✅ Verification Questions")
            st.caption("Ask these to verify resume claims")
            
            for i, q in enumerate(questions.get('verification_questions', []), 1):
                with st.expander(f"❓ Question {i}: {q.get('skill_tested', 'General')}", expanded=(i==1)):
                    st.markdown(f"**{q['question']}**")
                    st.caption(f"🎯 Difficulty: {q.get('difficulty', 'Medium')} | Purpose: {q.get('purpose', 'Verification')}")
            
            st.markdown("### 🔬 Depth Questions")
            st.caption("Probe how well they know the skills")
            
            for i, q in enumerate(questions.get('depth_questions', []), 1):
                st.markdown(f"**Q{i}:** {q['question']}")
                st.caption(f"Tests: {q.get('skill_tested', 'General knowledge')}")
                st.markdown("---")
            
            st.markdown("### 🛠️ Practical/Scenario Questions")
            for i, q in enumerate(questions.get('practical_questions', []), 1):
                st.markdown(f"**Q{i}:** {q['question']}")
                st.markdown("---")
            
            if questions.get('red_flag_questions'):
                st.markdown("### 🚩 Red Flag Questions")
                st.warning("⚠️ Ask if you suspect exaggeration")
                for i, q in enumerate(questions['red_flag_questions'], 1):
                    st.error(f"**Q{i}:** {q['question']}")
                    st.caption(f"Why: {q.get('rationale', 'Verify claim')}")
    
    # TAB 6: Knowledge Graph
    with tab6:
        st.markdown("## 🕸️ Knowledge Graph & Learning Paths")
        
        if 'knowledge_graph' not in report:
            st.info("💡 Knowledge graph analysis will be available when using the enhanced pipeline")
            st.markdown("""
            **This feature will provide:**
            - Readiness scores for missing skills
            - Prerequisites and skill relationships
            - Optimal learning paths using graph algorithms
            - Transferable skills analysis
            """)
        else:
            graph = report['knowledge_graph']
            
            st.markdown("### 📊 Readiness for Missing Skills")
            st.caption("How close is candidate to learning each missing skill?")
            
            for skill_data in graph.get('readiness_analysis', []):
                skill_name = skill_data['skill']
                score = skill_data['readiness_score']
                prereqs = skill_data.get('prerequisite_skills', [])
                
                if score >= 70:
                    color = "#22c55e"
                    status = "🟢 READY"
                elif score >= 40:
                    color = "#fb923c"
                    status = "🟡 MODERATE"
                else:
                    color = "#ef4444"
                    status = "🔴 CHALLENGING"
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.progress(score/100, text=f"{skill_name}")
                with col2:
                    st.markdown(f"**{score}%**")
                    
                st.caption(f"{status} | Already knows: {', '.join(prereqs[:3]) if prereqs else 'None'}")
                st.markdown("---")
            
            st.markdown("### 🛤️ Optimal Learning Paths")
            st.caption("Step-by-step paths using graph algorithms")
            
            for path in graph.get('learning_paths', []):
                with st.expander(f"📚 Path to: {path['target_skill']}"):
                    steps = path.get('steps', [])
                    if steps:
                        for i, step in enumerate(steps, 1):
                            st.markdown(f"**Step {i}:** {step}")
                    else:
                        st.info("Direct learning path - no prerequisites needed")
                    
                    time = path.get('estimated_weeks', 'Unknown')
                    st.success(f"⏱️ Estimated time: {time} weeks")
    
    # TAB 7: Skill Depth
    with tab7:
        st.markdown("## 🔍 Skill Depth Analysis")
        
        if 'depth_analysis' not in report:
            st.info("💡 Skill depth analysis will be available when using the enhanced pipeline")
            st.markdown("""
            **This feature will analyze:**
            - Evidence strength (1-5 stars)
            - Context quality (theory/hands-on/production)
            - Experience level per skill
            - Proof points (metrics, years, scale)
            """)
        else:
            depth = report['depth_analysis']
            
            st.markdown("### ⭐ Top 5 Skills by Depth")
            
            for i, skill in enumerate(depth.get('top_skills', [])[:5], 1):
                skill_name = skill['skill']
                depth_score = skill['depth_score']
                evidence = skill['evidence_strength']
                context = skill['context_quality']
                proofs = skill.get('proof_points', [])
                
                with st.container():
                    st.markdown(f"#### #{i} {skill_name}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Depth Score", f"{depth_score}/100")
                    with col2:
                        st.metric("Evidence", "⭐" * min(evidence, 5))
                    with col3:
                        st.metric("Context", context.upper())
                    
                    if proofs:
                        st.success(f"**Evidence:** {proofs[0]}")
                    
                    st.markdown("---")
            
            with st.expander("📋 View All Skills Depth Scores"):
                all_skills = depth.get('all_skills', {})
                if all_skills:
                    for skill_name, skill_data in all_skills.items():
                        st.markdown(f"**{skill_name}:** {skill_data['depth_score']}/100")
                else:
                    st.info("No detailed depth analysis available")
    
    # TAB 8: Retention Forecast
    with tab8:
        st.markdown("## 🧠 Skill Retention Forecast")
        
        if 'retention_predictions' not in report:
            st.info("💡 Retention predictions will be available when using the enhanced pipeline")
            st.markdown("""
            **This feature will predict:**
            - Retention probability for each skill
            - Based on cognitive science (forgetting curve)
            - Optimal review schedules
            - Learning strategy recommendations
            """)
        else:
            predictions = report['retention_predictions']
            
            high = len([p for p in predictions if p['retention_probability'] >= 70])
            medium = len([p for p in predictions if 40 <= p['retention_probability'] < 70])
            low = len([p for p in predictions if p['retention_probability'] < 40])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("🟢 High Retention", high)
            col2.metric("🟡 Medium Retention", medium)
            col3.metric("🔴 Low Retention", low)
            
            st.markdown("---")
            st.markdown("### 📊 Detailed Retention Forecast")
            
            for pred in predictions:
                skill = pred['skill']
                prob = pred['retention_probability']
                category = pred['retention_category']
                schedule = pred.get('review_schedule', 'Every 7 days')
                
                if prob >= 70:
                    emoji = "🟢"
                elif prob >= 40:
                    emoji = "🟡"
                else:
                    emoji = "🔴"
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.progress(prob/100, text=f"{emoji} {skill}")
                with col2:
                    st.markdown(f"**{prob}%**")
                
                st.caption(f"Category: {category.upper()} | Review: {schedule}")
                st.markdown("---")
    
    # TAB 9: Full Report (FORMATTED TEXT)
    with tab9:
        st.markdown("## 📄 Complete Analysis Report")
        
        # Format report as text
        formatted_report = format_full_report(report)
        
        # Display in a nice text area
        st.markdown("""
            <div class="report-section">
        """, unsafe_allow_html=True)
        
        st.markdown(formatted_report)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download Full Report (TXT)",
                formatted_report,
                f"candidate_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                "📥 Download JSON Version",
                json.dumps(report, indent=2),
                f"candidate_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json",
                use_container_width=True
            )


def main():
    """Main application"""
    
    st.markdown("""
        <div class="header-box">
            <h1>JOB FIT ANALYZER</h1>
            <div class="subtitle">AI-Powered Candidate Intelligence Platform</div>
        </div>
    """, unsafe_allow_html=True)
    
    initialize_pipeline()
    
    st.markdown("---")
    
    st.markdown('<h2 class="upload-heading">📤 Upload Documents</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
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
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze = st.button("🚀 ANALYZE CANDIDATE", use_container_width=True)
    
    if analyze:
        has_resume = resume_file or (resume_text and resume_text.strip())
        has_jd = jd_file or (jd_text and jd_text.strip())
        
        if not has_resume or not has_jd:
            st.error("⚠️ Please provide both Resume and Job Description")
            return
        
        import tempfile
        temp_dir = Path(tempfile.gettempdir())
        
        try:
            if resume_file:
                resume_path = temp_dir / f"resume_{resume_file.name}"
                with open(resume_path, 'wb') as f:
                    f.write(resume_file.getbuffer())
            else:
                resume_path = temp_dir / "resume.txt"
                with open(resume_path, 'w', encoding='utf-8') as f:
                    f.write(resume_text)
            
            if jd_file:
                jd_path = temp_dir / f"jd_{jd_file.name}"
                with open(jd_path, 'wb') as f:
                    f.write(jd_file.getbuffer())
            else:
                jd_path = temp_dir / "jd.txt"
                with open(jd_path, 'w', encoding='utf-8') as f:
                    f.write(jd_text)
            
            with st.spinner("🔄 Analyzing candidate... Please wait"):
                report = st.session_state.pipeline.analyze(resume_path, jd_path)
                st.session_state.report = report
                
                resume_path.unlink()
                jd_path.unlink()
            
            st.success("✅ Analysis Complete!")
            st.balloons()
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            import traceback
            st.error(f"Details: {traceback.format_exc()}")
            return
    
    if st.session_state.report:
        st.markdown("---")
        display_results(st.session_state.report)


if __name__ == "__main__":
    main()