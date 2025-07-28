from sentence_transformers import SentenceTransformer
import numpy as np

def get_embedder():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode

# Note: In production, cache or preload model 