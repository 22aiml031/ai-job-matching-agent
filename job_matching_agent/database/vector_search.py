import os
import requests
from typing import List

class VectorSearch:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.base_url = supabase_url
        self.headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }

    def search_jobs(self, embedding: List[float], top_k: int = 5):
        payload = {
            "embedding": embedding,
            "top_k": top_k
        }
        url = f"{self.base_url}/rest/v1/rpc/vector_search"
        print(f"[VectorSearch] RPC URL: {url}")
        print(f"[VectorSearch] Payload: {payload}")
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            print(f"[VectorSearch] Status: {response.status_code}")
            print(f"[VectorSearch] Response: {response.text}")
            response.raise_for_status()
            jobs = response.json()
            print(f"[VectorSearch] Jobs returned: {len(jobs)}")
            return jobs
        except Exception as e:
            print(f"[VectorSearch] Error: {e}")
            return []
