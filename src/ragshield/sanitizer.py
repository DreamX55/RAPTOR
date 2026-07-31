import re

class ContextSanitizer:
    """
    Module 6: Context Sanitizer
    Removes prompt-injection style language without destroying facts.
    """
    def __init__(self, config):
        self.enabled = config.get("modules.enable_sanitizer", True)
        self.removal_terms = config.get("sanitizer.removal_terms", [])
        self.drop_low_trust_chunks = config.get("drop_low_trust_chunks", False)
        self.adaptive_sanitizer = config.get("adaptive_sanitizer_enabled", False)
        self.min_rti_score = config.get("minimum_rti_score", 0.5)
        
        # Sort terms by length descending to prevent partial match deletion (e.g. "System Override" before "System:")
        self.removal_terms = sorted(self.removal_terms, key=len, reverse=True)
        
    def sanitize(self, chunks: list[dict]) -> list[dict]:
        """
        Takes a list of chunks, removes specified terms from the 'text' field.
        Appends a 'sanitization_actions' list to each chunk for logging.
        """
        if not self.enabled or not self.removal_terms:
            for chunk in chunks:
                if 'sanitization_actions' not in chunk:
                    chunk['sanitization_actions'] = []
            return chunks
            
        surviving_chunks = []
        for chunk in chunks:
            original_text = chunk.get("text", "")
            actions = []
            
            # Optimization 4: Hard Trust Filtering
            rti = chunk.get("rti_score", 1.0)
            if self.drop_low_trust_chunks and rti < self.min_rti_score:
                chunk["dropped"] = True
                chunk["sanitization_actions"] = ["Dropped due to low RTI"]
                continue # Skip appending to surviving_chunks
                
            chunk["dropped"] = False
            
            # Optimization 5: Adaptive Sanitizer
            if self.adaptive_sanitizer:
                if rti > 0.8:
                    # High trust -> preserve
                    actions.append("Preserved text (High RTI)")
                    new_text = original_text
                elif rti >= self.min_rti_score:
                    # Medium trust -> selective sanitize
                    new_text = original_text
                    for term in self.removal_terms:
                        if term in new_text:
                            actions.append(f"Adaptive Removed: '{term}'")
                            new_text = new_text.replace(term, "")
                else:
                    # Low trust (but not dropped) -> heavy sanitize or truncate
                    actions.append("Truncated (Low RTI)")
                    new_text = original_text[:len(original_text)//2] # truncate half
            else:
                # Standard Sanitization
                new_text = original_text
                for term in self.removal_terms:
                    if term in new_text:
                        actions.append(f"Removed: '{term}'")
                        new_text = new_text.replace(term, "")
                    
            # Clean up double spaces caused by removals
            new_text = re.sub(' +', ' ', new_text).strip()
            
            chunk["text"] = new_text
            chunk["sanitization_actions"] = actions
            surviving_chunks.append(chunk)
            
        return surviving_chunks
