import streamlit as st
from job_matching_agent.api.main import upload_resume, recommend_jobs

st.title("AI Job Matching Agent")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)")
if uploaded_file:
    result = upload_resume(uploaded_file)
    st.write("Resume Text:", result["resume_text"])
    embedding = result["embedding"]
    candidate_skills = st.text_input("Enter your skills (comma separated)")
    candidate_experience = st.text_input("Enter your experience level")
    if st.button("Recommend Jobs"):
        recs = recommend_jobs(embedding, candidate_skills, candidate_experience)
        for rec in recs["recommendations"]:
            st.subheader(rec["job"]["title"])
            st.write("Skills:", rec["job"]["skills"])
            st.write("Match Score:", rec["match_score"])
            st.write("Explanation:", rec["explanation"])
