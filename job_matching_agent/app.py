import streamlit as st

import sys
import os
import re
import spacy
from spacy.matcher import PhraseMatcher
from dotenv import load_dotenv

load_dotenv()
st.write(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
st.write(f"SUPABASE_KEY: {os.getenv('SUPABASE_KEY')}")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from embeddings.embedding_model import EmbeddingGenerator
from pipeline.resume_parser import ResumeParser
from agent.job_recommender import JobRecommender
from database.vector_search import VectorSearch
from agent.explanation_agent import LLMExplainer
from utils.text_processing import preprocess_text

# Load spaCy model
@st.cache_resource(show_spinner=False)
def get_spacy_model():
    return spacy.load("en_core_web_sm")

def extract_skills_experience(text):
    nlp = get_spacy_model()
    doc = nlp(text)
    # Skill extraction using phrase matcher
    skills_keywords = [
        'python', 'java', 'c++', 'sql', 'machine learning', 'deep learning', 'nlp', 'data analysis',
        'tensorflow', 'pytorch', 'scikit-learn', 'git', 'docker', 'cloud', 'aws', 'azure', 'react', 'html', 'css', 'javascript'
    ]
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in skills_keywords]
    matcher.add("SKILLS", patterns)
    matches = matcher(doc)
    skills_found = list(set([doc[start:end].text for _, start, end in matches]))
    # Experience extraction using entity recognition and keyword search
    experience_keywords = ['intern', 'fresher', 'entry', 'junior', 'senior', 'lead', 'manager', 'expert', '0-1', '1-3', '3-5', '5+']
    exp_found = None
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'TITLE', 'PERSON'] and any(kw in ent.text.lower() for kw in experience_keywords):
            exp_found = ent.text
            break
    if not exp_found:
        for kw in experience_keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text.lower()):
                exp_found = kw
                break
    return skills_found, exp_found or 'Not found'

st.title("AI Job Matching Agent")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)")

if uploaded_file:
    if uploaded_file.name.endswith('.pdf'):
        resume_text = ResumeParser.parse_pdf(uploaded_file)
    else:
        resume_text = ResumeParser.parse_text(uploaded_file.read().decode('utf-8'))
    with st.expander("📄 Extracted Resume Text"):
        st.write(resume_text)
    skills_found, exp_found = extract_skills_experience(resume_text)
    with st.expander("🧠 Extracted Skills"):
        st.write(', '.join(skills_found) if skills_found else 'None found')
    with st.expander("💼 Experience Level"):
        st.write(exp_found)
    if st.button("Recommend Jobs"):
        from job_matching_agent.job_recommender import JobRecommender
        job_recommender = JobRecommender()
        try:
            recommendations = job_recommender.recommend_jobs(resume_text, top_k=5)
            st.write("Debug: Recommendations Response:", recommendations)
            if not recommendations:
                st.warning("No jobs found. Please check if jobs are inserted in Supabase and the vector_search function is set up.")
            else:
                st.subheader("Recommended Jobs:")
                for rec in recommendations:
                    match_score = round(rec['similarity'] * 100) if rec.get('similarity') is not None else 0
                    st.markdown(f"### {rec['title']}")
                    st.write(f"**Skills:** {rec['skills']}")
                    st.write(f"**Experience Level:** {rec['experience_level']}")
                    st.write(f"**Match Score:** {match_score}%")
                    st.progress(match_score / 100)
                    st.divider()
        except Exception as e:
            st.error(f"Error during job recommendation: {e}")
