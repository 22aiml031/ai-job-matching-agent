from fastapi import FastAPI, UploadFile, File, Form
from job_matching_agent.pipeline.resume_parser import ResumeParser
from job_matching_agent.embeddings.embedding_model import EmbeddingGenerator
from job_matching_agent.agent.job_recommender import JobRecommender
from job_matching_agent.agent.explanation_agent import ExplanationAgent
from job_matching_agent.database.vector_search import VectorSearch
from job_matching_agent.utils.text_processing import preprocess_text
import os

app = FastAPI()

vector_search = VectorSearch(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
embedding_generator = EmbeddingGenerator()
explanation_agent = ExplanationAgent(os.getenv("OPENAI_API_KEY"))
job_recommender = JobRecommender(vector_search)

@app.post("/upload_resume")
def upload_resume(file: UploadFile = File(...)):
    if file.filename.endswith('.pdf'):
        text = ResumeParser.parse_pdf(file.file)
    else:
        text = ResumeParser.parse_text(file.file.read().decode('utf-8'))
    processed = preprocess_text(text)
    embedding = embedding_generator.generate_single(processed)
    return {"resume_text": processed, "embedding": embedding}

@app.get("/recommend_jobs")
def recommend_jobs(resume_embedding: list, candidate_skills: str = Form(...), candidate_experience: str = Form(...)):
    skills = [s.strip() for s in candidate_skills.split(',')]
    recommendations = job_recommender.recommend(resume_embedding, skills, candidate_experience)
    for rec in recommendations:
        rec['explanation'] = explanation_agent.explain(rec['job'], candidate_skills, rec['match_score'])
    return {"recommendations": recommendations}
