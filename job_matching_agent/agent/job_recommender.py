from typing import List, Dict
from job_matching_agent.database.vector_search import VectorSearch
from job_matching_agent.utils.text_processing import skill_overlap
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class JobRecommender:
    def __init__(self, vector_search: VectorSearch):
        self.vector_search = vector_search

    def recommend(self, resume_embedding: List[float], candidate_skills: List[str], candidate_experience: str) -> List[Dict]:
        jobs = self.vector_search.search_jobs(resume_embedding, top_k=20)
        allowed_levels = ["fresher", "entry-level", "intern"]
        filtered_jobs = [job for job in jobs if job.get('experience_level', '').strip().lower() in allowed_levels]
        recommendations = []
        resume_vec = np.array(resume_embedding).reshape(1, -1)
        for job in filtered_jobs:
            job_vec = np.array(job.get('embedding', [])).reshape(1, -1)
            if job_vec.shape[1] != resume_vec.shape[1]:
                print(f"[JobRecommender] Skipping job {job.get('title')} due to embedding shape mismatch.")
                continue
            cos_sim = cosine_similarity(resume_vec, job_vec)[0][0]
            job_skills = [s.strip() for s in job.get('skills', '').split(',')]
            skill_score = skill_overlap(candidate_skills, job_skills)
            final_score = 0.7 * cos_sim + 0.3 * skill_score
            print(f"[JobRecommender] Job: {job.get('title')}, Cosine: {cos_sim:.3f}, Skill: {skill_score:.3f}, Final: {final_score:.3f}")
            recommendations.append({
                'title': job.get('title'),
                'skills': job.get('skills'),
                'experience_level': job.get('experience_level'),
                'match_score': round(final_score, 3),
                'job': job
            })
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:5]
