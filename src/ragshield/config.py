import yaml
import os

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "ragshield.yaml")

class RAGShieldConfig:
    def __init__(self, config_override=None, config_path=DEFAULT_CONFIG_PATH):
        self.config = {}
        
        # Load from YAML if it exists
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
                
        # Merge overrides
        if config_override:
            self._update_nested_dict(self.config, config_override)
            
    def _update_nested_dict(self, d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = self._update_nested_dict(d.get(k, {}), v)
            else:
                d[k] = v
        return d
        
    def get(self, key, default=None):
        keys = key.split('.')
        val = self.config
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                return default
        return val if val is not None else default
