import numpy as np

class RetrievalConfidence:
    """
    Module 3: Retrieval Confidence
    Normalizes the raw FAISS L2 distance or inner product to [0,1].
    """
    def __init__(self):
        # Depending on how FAISS is configured (IndexFlatL2 vs IndexFlatIP),
        # distances may be arbitrarily large L2 squared distances or bounded.
        # For simplicity in this implementation, we assume L2 distance where lower = better,
        # or we dynamically normalize based on the retrieved set.
        pass
        
    def calculate(self, raw_scores: list[float]) -> list[float]:
        """
        Normalizes a list of raw FAISS scores to [0,1] confidence values.
        Higher output = higher confidence.
        """
        if not raw_scores:
            return []
            
        scores = np.array(raw_scores)
        
        # Determine min and max to normalize
        s_min = np.min(scores)
        s_max = np.max(scores)
        
        if s_min == s_max:
            return [1.0] * len(raw_scores)
            
        # Assuming L2 distance (lower is better):
        # We invert it: (s_max - score) / (s_max - s_min)
        # So the minimum distance (best match) gets 1.0, maximum gets 0.0
        normalized = (s_max - scores) / (s_max - s_min)
        
        # To avoid the worst chunk in the top_k getting strictly 0.0 (since it was still retrieved),
        # we can scale it to a range like [0.2, 1.0].
        # But for strict mathematical alignment to [0,1], we leave it.
        return normalized.tolist()
