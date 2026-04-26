import streamlit as st
import pandas as pd
from core.data_loader import load_candidates, prepare_candidate_text_for_embedding
from core.matcher import CandidateMatcher
from core.conversational_agent import ConversationalAgent

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Talent Scout",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .candidate-card {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .score-badge {
        background-color: #4CAF50;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 14px;
    }
    .dialogue-agent {
        background-color: #2b3a4a;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 3px solid #3498db;
    }
    .dialogue-candidate {
        background-color: #3d3b4a;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        border-left: 3px solid #9b59b6;
        text-align: right;
    }
    .metric-container {
        display: flex;
        gap: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialization ---
@st.cache_resource
def load_models():
    """Load the ML models once and cache them."""
    matcher = CandidateMatcher()
    agent = ConversationalAgent()
    return matcher, agent

@st.cache_data
def load_and_embed_data(_matcher):
    """Load data and compute embeddings once."""
    df = load_candidates()
    texts = prepare_candidate_text_for_embedding(df)
    embeddings = _matcher.generate_embeddings(texts)
    return df, embeddings

matcher, agent = load_models()
candidates_df, candidate_embeddings = load_and_embed_data(matcher)

# --- Sidebar ---
st.sidebar.title("🕵️ AI Talent Scout")
st.sidebar.markdown("Automate talent discovery with semantic matching and simulated conversational outreach.")
st.sidebar.divider()
st.sidebar.markdown("**Database Stats:**")
st.sidebar.info(f"Loaded {len(candidates_df)} candidates in the pool.")

# --- Main Area ---
st.title("Talent Discovery & Engagement Dashboard")
st.markdown("Enter a Job Description below to find and engage the best matching candidates from our database.")

# JD Input
jd_input = st.text_area("Job Description (JD)", height=200, placeholder="Paste the job description here. e.g., 'We are looking for a Senior Python Developer with experience in Django, AWS, and building scalable backend systems...'")

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    match_weight = st.slider("Match Score Weight", 0.0, 1.0, 0.7, 0.1)
with col2:
    interest_weight = st.slider("Interest Score Weight", 0.0, 1.0, 0.3, 0.1)

if st.button("🚀 Run AI Scouting Pipeline", type="primary", use_container_width=True):
    if not jd_input.strip():
        st.error("Please enter a Job Description.")
    else:
        with st.spinner("Analyzing Job Description & finding matches..."):
            # 1. Semantic Matching
            match_scores = matcher.calculate_match_scores(jd_input, candidate_embeddings)
            candidates_df['Match_Score'] = match_scores
            
            # 2. Simulated Outreach (For top candidates to save time, or all for this demo)
            interest_scores = []
            dialogues = []
            explanations = []
            match_explanations = []
            
            # Progress bar for simulated outreach
            progress_text = "Simulating conversational outreach..."
            my_bar = st.progress(0, text=progress_text)
            
            for i, row in candidates_df.iterrows():
                # Simulate Outreach
                outreach_result = agent.simulate_outreach(row.to_dict(), jd_input)
                interest_scores.append(outreach_result['interest_score'])
                dialogues.append(outreach_result['dialogue'])
                explanations.append(outreach_result['explanation'])
                
                # Match Explanation
                match_explanations.append(matcher.get_match_explanation(jd_input, row.to_dict()))
                
                # Update progress
                my_bar.progress((i + 1) / len(candidates_df), text=f"Engaging with {row['name']}...")
                
            candidates_df['Interest_Score'] = interest_scores
            candidates_df['Dialogue'] = dialogues
            candidates_df['Interest_Explanation'] = explanations
            candidates_df['Match_Explanation'] = match_explanations
            
            # 3. Final Ranking
            candidates_df['Final_Score'] = (candidates_df['Match_Score'] * match_weight) + (candidates_df['Interest_Score'] * interest_weight)
            candidates_df['Final_Score'] = candidates_df['Final_Score'].round(1)
            
            # Sort by Final Score
            ranked_df = candidates_df.sort_values(by='Final_Score', ascending=False).reset_index(drop=True)
            
            my_bar.empty()
            st.success("Pipeline complete! Here are your top candidates:")
            
            # --- Display Results ---
            st.divider()
            
            for i, row in ranked_df.iterrows():
                # Only show top 5 matches
                if i >= 5: break 
                
                with st.container():
                    st.markdown(f'<div class="candidate-card">', unsafe_allow_html=True)
                    
                    header_col, score_col = st.columns([3, 1])
                    with header_col:
                        st.subheader(f"#{i+1} {row['name']}")
                        st.markdown(f"**{row['role']}** | {row['experience_years']} years experience")
                        st.markdown(f"*{row['summary']}*")
                        
                    with score_col:
                        st.markdown(f"**Final Score:** <span class='score-badge' style='background-color: #2196F3;'>{row['Final_Score']} / 100</span>", unsafe_allow_html=True)
                        st.markdown(f"**Match:** <span class='score-badge'>{row['Match_Score']}</span> | **Interest:** <span class='score-badge' style='background-color: #FF9800;'>{row['Interest_Score']}</span>", unsafe_allow_html=True)
                        
                    with st.expander("🔍 View AI Explanations & Conversation"):
                        tab1, tab2 = st.tabs(["Match Explainability", "Simulated Conversation"])
                        
                        with tab1:
                            st.markdown("#### Match Reasoning")
                            st.info(row['Match_Explanation'])
                            skills_str = ", ".join(row['skills']) if isinstance(row['skills'], list) else row['skills']
                            st.markdown(f"**Candidate Skills:** {skills_str}")
                            
                        with tab2:
                            st.markdown("#### Engagement Assessment")
                            st.warning(row['Interest_Explanation'])
                            st.markdown("---")
                            st.markdown("##### Simulated Dialogue Transcript")
                            for msg in row['Dialogue']:
                                if msg['speaker'] == 'Agent':
                                    st.markdown(f"<div class='dialogue-agent'><b>🤖 AI Agent:</b> {msg['text']}</div>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<div class='dialogue-candidate'><b>👤 {row['name']}:</b> {msg['text']}</div>", unsafe_allow_html=True)
                                    
                    st.markdown("</div>", unsafe_allow_html=True)
