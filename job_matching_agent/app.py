import streamlit as st
import sys
import os
import re
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.resume_parser import ResumeParser
from agent.job_recommender import JobRecommender

st.title("AI Job Matching Agent")

# -------------------------------
# Simple Skill Extraction
# -------------------------------

def extract_skills(text):

    skills_db = [
        "python","java","c++","sql","machine learning","deep learning",
        "nlp","data science","data analysis","tensorflow","pytorch",
        "scikit-learn","git","docker","aws","azure","react",
        "html","css","javascript","pandas","numpy"
    ]

    text = text.lower()

    found_skills = []
    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


# -------------------------------
# Experience Detection
# -------------------------------

def detect_experience(text):

    match = re.search(r'(\d+)\+?\s*(years|yrs)', text.lower())

    if match:

        years = int(match.group(1))

        if years <= 1:
            return "Entry Level"

        elif years <= 3:
            return "Junior Level"

        elif years <= 5:
            return "Mid Level"

        else:
            return "Senior Level"

    return "Not Found"


# -------------------------------
# Upload Resume
# -------------------------------

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)")


if uploaded_file:

    if uploaded_file.name.endswith(".pdf"):
        resume_text = ResumeParser.parse_pdf(uploaded_file)

    else:
        resume_text = ResumeParser.parse_text(
            uploaded_file.read().decode("utf-8")
        )


    with st.expander("📄 Extracted Resume Text"):
        st.write(resume_text)


    # Extract skills
    skills = extract_skills(resume_text)

    with st.expander("🧠 Extracted Skills"):
        if skills:
            st.write(", ".join(skills))
        else:
            st.write("No skills detected")


    # Detect experience
    experience = detect_experience(resume_text)

    with st.expander("💼 Experience Level"):
        st.write(experience)


    # -------------------------------
    # Job Recommendation
    # -------------------------------

    if st.button("Recommend Jobs"):

        job_recommender = JobRecommender()

        try:

            recommendations = job_recommender.recommend_jobs(
                resume_text,
                top_k=5
            )

            if not recommendations:

                st.warning(
                    "No jobs found. Please check if jobs exist in Supabase."
                )

            else:

                st.subheader("Recommended Jobs")

                for job in recommendations:

                    match_score = (
                        round(job["similarity"] * 100)
                        if job.get("similarity")
                        else 0
                    )

                    st.markdown(f"### {job['title']}")

                    st.write(f"**Skills:** {job['skills']}")

                    st.write(
                        f"**Experience Level:** {job['experience_level']}"
                    )

                    st.write(f"**Match Score:** {match_score}%")

                    st.progress(match_score / 100)

                    st.divider()

        except Exception as e:

            st.error(f"Error during job recommendation: {e}")
