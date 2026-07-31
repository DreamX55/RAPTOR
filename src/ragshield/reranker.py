class Reranker:
    """
    Module 5: Intelligent Re-ranking
    Sorts retrieved chunks strictly by Retrieval Trust Index (RTI).
    Optionally pushes chunks below the minimum_rti_score threshold to the bottom.
    """
    def __init__(self, config):
        self.enabled = config.get("modules.enable_reranker", True)
        self.minimum_rti_score = config.get("thresholds.minimum_rti_score", 0.40)
        
    def rerank(self, chunks: list[dict]) -> list[dict]:
        """
        Expects chunks to have 'rti_score' populated.
        Returns a sorted list of chunks.
        """
        if not self.enabled:
            return chunks
            
        # Add a flag for crossing the threshold (for logging)
        for chunk in chunks:
            chunk['threshold_crossed'] = chunk.get('rti_score', 1.0) >= self.minimum_rti_score
            
        # Sort in descending order of rti_score
        # Python's Timsort is stable, so equal trust scores maintain original retrieval order
        sorted_chunks = sorted(chunks, key=lambda x: x.get('rti_score', 1.0), reverse=True)
        
        # Update the 'reranked_position' internally (0-indexed rank for logging)
        for i, chunk in enumerate(sorted_chunks):
            chunk['reranked_position'] = i + 1
            
        return sorted_chunks
