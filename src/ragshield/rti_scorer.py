class TrustScorer:
    """
    Module 4: Retrieval Retrieval Trust Index (RTI)r
    Computes a Normalized Weighted Trust Index. Extensible to arbitrary signals.
    """
    def __init__(self, config):
        self.enabled = config.get("modules.enable_rti_scorer", True)
        self.weights = config.get("weights", {})
        self.penalty_weight = config.get("consistency_penalty_weight", 0.0)
        
    def score(self, chunk_signals: dict) -> tuple[float, float]:
        """
        Takes a dictionary of {signal_name: signal_value}.
        Both signal_value and weights are expected to be floats.
        Returns a final Retrieval Trust Index (RTI) clamped to [0,1].
        """
        if not self.enabled:
            return 1.0, 0.0 # Default full trust if disabled
            
        total_score = 0.0
        
        for signal_name, signal_val in chunk_signals.items():
            # Get the weight for this specific signal, defaulting to 0.0 if not found
            weight = self.weights.get(signal_name, 0.0)
            total_score += (weight * signal_val)
            
        # Optimization 3: Consistency Penalty
        # If one chunk strongly disagrees with majority (low consensus) but maintains high retrieval conf.
        consistency_penalty = 0.0
        if self.penalty_weight > 0:
            ret_conf = chunk_signals.get("retrieval_confidence", 0.0)
            cons_score = chunk_signals.get("consensus_score", 0.0)
            if ret_conf > 0.7 and cons_score < 0.4:
                # Apply penalty scaled by how strong the disagreement is
                consistency_penalty = self.penalty_weight * (0.4 - cons_score)
                total_score -= consistency_penalty
            
        # The sum might slightly exceed 1.0 or dip below 0.0 depending on weight calibration
        # We clamp it to [0, 1] mathematically.
        return max(0.0, min(1.0, total_score)), consistency_penalty
