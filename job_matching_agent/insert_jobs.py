import os
import json
from dotenv import load_dotenv
from job_matching_agent.embeddings.embedding_model import EmbeddingGenerator
from job_matching_agent.pipeline.data_loader import JobDataLoader
from job_matching_agent.database.supabase_client import SupabaseClient

load_dotenv()
print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))

# Paths
DATASET_PATH = os.path.join(os.path.dirname(__file__), '..', 'job_dataset.json')

# Load jobs
loader = JobDataLoader(DATASET_PATH)
jobs = loader.get_documents()

# Generate embeddings
embedder = EmbeddingGenerator()
texts = [job['document'] for job in jobs]
embeddings = embedder.generate(texts)

# Prepare jobs for Supabase
jobs_for_db = []
for job, embedding in zip(jobs, embeddings):
    if len(embedding) == 384:
        jobs_for_db.append({
            'id': job['id'],
            'title': job['title'],
            'experience_level': job['experience_level'],
            'skills': job['skills'],
            'keywords': job['keywords'],
            'embedding': embedding  # send as list
        })
    else:
        print(f"Skipping job {job['id']} due to invalid embedding length: {len(embedding)}")

# Insert into Supabase
client = SupabaseClient()
print(f'Inserting {len(jobs_for_db)} jobs into Supabase in batches of 50...')
batch_size = 50
for i in range(0, len(jobs_for_db), batch_size):
    batch = jobs_for_db[i:i+batch_size]
    try:
        response = client.insert_jobs(batch, return_raw=True)
        print(f'Batch {i//batch_size+1} HTTP status:', response.status_code)
        print(f'Batch {i//batch_size+1} response text:', response.text)
    except Exception as e:
        print(f'Error inserting batch {i//batch_size+1}: {e}')
