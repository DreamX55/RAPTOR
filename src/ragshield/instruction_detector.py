import re

class InstructionDetector:
    """
    Module 1: Detects prompt-injection style language.
    Outputs a score in [0,1] indicating the presence of malicious instructions.
    """
    def __init__(self, config):
        self.enabled = config.get("modules.enable_instruction_detector", True)
        self.patterns = config.get("instruction_detector.patterns", [])
        
        # Compile patterns for fast matching, case-insensitive
        self.compiled_patterns = [re.compile(re.escape(p), re.IGNORECASE) for p in self.patterns]
        
    def detect(self, text: str) -> float:
        """
        Returns a signal [0,1] based on matches. 
        Currently implemented as a normalized density or simple presence scale.
        """
        if not self.enabled or not text or not self.compiled_patterns:
            return 0.0
            
        match_count = 0
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                match_count += 1
                
        # Simple normalization: if it matches 1 pattern, it's highly suspicious (e.g. 0.8)
        # If it matches multiple, it maxes out at 1.0.
        if match_count == 0:
            return 0.0
        elif match_count == 1:
            return 0.8
        else:
            return 1.0
