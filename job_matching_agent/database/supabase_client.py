# Supabase client for pgvector operations
# Requires SUPABASE_URL and SUPABASE_KEY in environment variables

import os
import requests
from typing import List, Dict

class SupabaseClient:
    def __init__(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        self.base_url = os.getenv("SUPABASE_URL")
        self.headers = {
            "apikey": os.getenv("SUPABASE_KEY"),
            "Authorization": f"Bearer {os.getenv('SUPABASE_KEY')}",
            "Content-Type": "application/json"
        }

    def insert_jobs(self, jobs: List[Dict], return_raw: bool = False):
        url = f"{self.base_url}/rest/v1/jobs"
        data = [
            {
                "id": job["id"],
                "title": job["title"],
                "experience_level": job["experience_level"],
                "skills": job["skills"],
                "keywords": job["keywords"],
                "embedding": job["embedding"]
            }
            for job in jobs
        ]
        params = {"on_conflict": "id"}
        headers = self.headers.copy()
        headers["Prefer"] = "resolution=merge-duplicates"
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        if return_raw:
            return response
        print('Supabase response:', response.text)
        return response.json()

    def search_jobs(self, embedding: List[float], top_k: int = 5):
        # This is a placeholder. Actual vector search should be done via RPC or SQL endpoint.
        pass
