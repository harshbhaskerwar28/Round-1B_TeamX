from scipy.spatial.distance import cdist
import numpy as np
from typing import List, Dict

def rank_sections(sections: List[Dict], embeddings: np.ndarray, query_emb: np.ndarray, top_n: int = 5) -> List[Dict]:
    # Compute cosine similarities
    similarities = 1 - cdist(embeddings, query_emb.reshape(1, -1), metric='cosine').flatten()
    # Add scores to sections
    for i, section in enumerate(sections):
        section['score'] = similarities[i]
    # Sort by score descending
    sorted_sections = sorted(sections, key=lambda s: s['score'], reverse=True)
    # Select top N unique by document and title (simple dedup)
    unique_sections = []
    seen = set()
    for s in sorted_sections:
        key = (s['document'], s['section_title'])
        if key not in seen:
            seen.add(key)
            unique_sections.append(s)
            if len(unique_sections) == top_n:
                break
    # Assign ranks
    for rank, s in enumerate(unique_sections, start=1):
        s['importance_rank'] = rank
    return unique_sections 