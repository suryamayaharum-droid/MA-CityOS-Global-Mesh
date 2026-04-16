"""HoloOS Memory System"""
import time
from typing import List, Dict

class MemorySystem:
    def __init__(self):
        self.semantic = []
        self.episodic = []
        self.working = []
        self.procedural = {}
    
    def store(self, content: str, mtype: str = "semantic") -> str:
        item = {"content": content[:200], "time": time.time()}
        if mtype == "semantic": self.semantic.append(item)
        elif mtype == "episodic": self.episodic.append(item)
        elif mtype == "working": 
            self.working.append(item)
            if len(self.working) > 7: self.working = self.working[-7:]
        return f"stored_{len(self.semantic)}"
    
    def recall(self, query: str) -> List[str]:
        return [s["content"] for s in self.semantic[-5:]]
    
    def get_status(self) -> dict:
        return {"semantic": len(self.semantic), "episodic": len(self.episodic), "working": len(self.working), "procedural": len(self.procedural)}

__all__ = ["MemorySystem"]
