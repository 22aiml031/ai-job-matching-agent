from openai import OpenAI
from typing import Dict
import os
from dotenv import load_dotenv

class LLMExplainer:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        self.client = OpenAI(api_key=api_key)

    def explain(self, job: Dict, candidate_skills: str, match_score: float) -> str:
        prompt = f"Job Title: {job['title']}\nSkills: {job['skills']}\nMatch Score: {match_score}\nCandidate Skills: {candidate_skills}\nExplain why this job is recommended for the candidate."
        print(f"[LLMExplainer] Prompt: {prompt}")
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a job recommendation AI"},
                {"role": "user", "content": prompt}
            ]
        )
        explanation = response.choices[0].message.content
        print(f"[LLMExplainer] Explanation: {explanation}")
        return explanation
