"""HoloOS Config Manager"""
import os

class ConfigManager:
    def __init__(self):
        self.config = {}
        self.secrets = {}
    
    def set(self, key: str, value: str) -> None:
        self.config[key] = value
    
    def get(self, key: str, default: str = None) -> str:
        return self.config.get(key, default)
    
    def set_secret(self, key: str, value: str) -> None:
        self.secrets[key] = value
    
    def get_secret(self, key: str) -> str:
        return self.secrets.get(key)
    
    def load_env(self, prefix: str = "HOLOOS_") -> None:
        for k, v in os.environ.items():
            if k.startswith(prefix):
                self.config[k[len(prefix):].lower()] = v
    
    def get_all(self) -> dict:
        return {"config": self.config, "secrets": len(self.secrets)}

__all__ = ["ConfigManager"]