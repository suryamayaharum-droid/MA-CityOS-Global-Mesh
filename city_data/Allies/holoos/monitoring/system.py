"""HoloOS Monitoring"""
import time
from typing import Dict

class HealthCheck:
    def __init__(self, name: str):
        self.name = name
        self.last_check = time.time()
    
    def check(self) -> bool:
        self.last_check = time.time()
        return True

class MonitoringSystem:
    def __init__(self):
        self.checks = {}
        self.metrics = []
    
    def register(self, name: str) -> None:
        self.checks[name] = HealthCheck(name)
    
    def health(self) -> Dict:
        return {n: c.check() for n, c in self.checks.items()}
    
    def record(self, name: str, value: float) -> None:
        self.metrics.append({"name": name, "value": value, "time": time.time()})
    
    def get_status(self) -> Dict:
        return {"checks": len(self.checks), "metrics": len(self.metrics)}

__all__ = ["MonitoringSystem", "HealthCheck"]