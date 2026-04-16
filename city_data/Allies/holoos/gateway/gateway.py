"""HoloOS API Gateway - Rate Limiting, Auth, Caching"""
from typing import Dict, Optional, Callable
import time
import hashlib

class RateLimiter:
    def __init__(self, capacity: int = 60):
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.time()
    
    def allow(self) -> bool:
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

class APIGateway:
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.cache = {}
        self.routes = {}
        self.auth_keys = {}
    
    def add_route(self, path: str, handler: Callable) -> None:
        self.routes[path] = handler
    
    def create_key(self, owner: str) -> str:
        key = hashlib.sha256(f"{owner}{time.time()}".encode()).hexdigest()[:32]
        self.auth_keys[key] = owner
        return key
    
    def get_status(self) -> Dict:
        return {"routes": len(self.routes), "keys": len(self.auth_keys)}

__all__ = ["APIGateway", "RateLimiter"]