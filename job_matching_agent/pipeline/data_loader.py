import json
from typing import List, Dict

class JobDataLoader:
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.jobs = self.load_jobs()

    def load_jobs(self) -> List[Dict]:
        with open(self.json_path, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
        # Filter out incomplete entries
        jobs = [job for job in jobs if job.get('JobID') and job.get('Title')]
        return jobs

    def job_to_document(self, job: Dict) -> str:
        doc = []
        doc.append(f"Title: {job.get('Title', '')}")
        doc.append(f"Experience Level: {job.get('ExperienceLevel', '')}")
        doc.append(f"Years Of Experience: {job.get('YearsOfExperience', '')}")
        doc.append(f"Skills: {', '.join(job.get('Skills', []))}")
        doc.append(f"Responsibilities: {', '.join(job.get('Responsibilities', []))}")
        doc.append(f"Keywords: {', '.join(job.get('Keywords', []))}")
        return '\n'.join(doc)

    def get_documents(self) -> List[Dict]:
        return [
            {
                'id': job['JobID'],
                'title': job['Title'],
                'experience_level': job.get('ExperienceLevel', ''),
                'skills': ', '.join(job.get('Skills', [])),
                'keywords': ', '.join(job.get('Keywords', [])),
                'document': self.job_to_document(job)
            }
            for job in self.jobs
        ]
