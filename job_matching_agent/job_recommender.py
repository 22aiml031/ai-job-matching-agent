import os
from dotenv import load_dotenv
from job_matching_agent.embedding_service import EmbeddingService
from job_matching_agent.supabase_client import SupabaseClient

class JobRecommender:
    def __init__(self):
        load_dotenv()
        self.embedding_service = EmbeddingService()
        self.supabase_client = SupabaseClient()

    def recommend_jobs(self, resume_text: str, top_k: int = 5):
        embedding = self.embedding_service.embed(resume_text)
        print(f"[JobRecommender] Resume embedding: {embedding[:5]} ... (len={len(embedding)})")
        jobs = self.supabase_client.vector_search(embedding, top_k=top_k)
        results = []
        for job in jobs:
            results.append({
                "id": job.get("id"),
                "title": job.get("title"),
                "skills": job.get("skills"),
                "experience_level": job.get("experience_level"),
                "similarity": job.get("similarity")
            })
        return results
