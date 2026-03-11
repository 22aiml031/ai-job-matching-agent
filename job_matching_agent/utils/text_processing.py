import re
from typing import List

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def skill_overlap(candidate_skills: List[str], job_skills: List[str]) -> float:
    candidate_set = set([s.lower() for s in candidate_skills])
    job_set = set([s.lower() for s in job_skills])
    if not job_set:
        return 0.0
    return len(candidate_set & job_set) / len(job_set)
