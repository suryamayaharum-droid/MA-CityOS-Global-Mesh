"""HoloOS Plugin Manager"""
import time
from typing import Dict, List, Callable

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, dict] = {}
        self.hooks: Dict[str, List[Callable]] = {}
    
    def register(self, name: str, version: str, hooks: List[str]) -> None:
        self.plugins[name] = {"version": version, "hooks": hooks, "enabled": True, "loaded": time.time()}
        for hook in hooks:
            if hook not in self.hooks:
                self.hooks[hook] = []
    
    def enable(self, name: str) -> bool:
        if name in self.plugins:
            self.plugins[name]["enabled"] = True
            return True
        return False
    
    def disable(self, name: str) -> bool:
        if name in self.plugins:
            self.plugins[name]["enabled"] = False
            return True
        return False
    
    def trigger(self, hook: str, *args, **kwargs) -> List:
        results = []
        if hook in self.hooks:
            for cb in self.hooks[hook]:
                try: results.append(cb(*args, **kwargs))
                except: pass
        return results
    
    def list_all(self) -> List[Dict]:
        return [{"name": n, **p} for n, p in self.plugins.items()]
    
    def get_status(self) -> Dict:
        return {"plugins": len(self.plugins), "hooks": len(self.hooks)}

__all__ = ["PluginManager"]