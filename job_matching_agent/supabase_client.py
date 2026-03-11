import os
from dotenv import load_dotenv
from supabase import create_client, Client

class SupabaseClient:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL or SUPABASE_KEY not set in environment.")
        self.client: Client = create_client(self.url, self.key)

    def vector_search(self, embedding, top_k=5):
        # embedding must be a list of floats
        response = self.client.rpc(
            "vector_search",
            {"query_embedding": embedding, "top_k": top_k}
        ).execute()
        if hasattr(response, 'data'):
            return response.data
        return response
