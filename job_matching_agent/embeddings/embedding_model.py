# Embedding generator using SentenceTransformers
# Model: all-MiniLM-L6-v2

from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingGenerator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True).tolist()

    def generate_single(self, text: str) -> List[float]:
        return self.model.encode([text], convert_to_numpy=True)[0].tolist()
