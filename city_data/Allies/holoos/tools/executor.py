"""HoloOS Tool Executor"""
from typing import Dict, Callable

class ToolExecutor:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self._register()
    
    def _register(self):
        self.tools = {
            "code_writer": lambda **k: f"Code written: {k.get('language', 'unknown')}",
            "code_reader": lambda **k: f"Reading: {k.get('path', '')}",
            "search": lambda **k: f"Search: {k.get('query', '')}",
            "shell": lambda **k: f"Shell: {k.get('command', '')}",
            "github": lambda **k: f"GitHub: {k.get('action', '')}",
            "browser": lambda **k: f"Browser: {k.get('url', '')}",
            "memory": lambda **k: f"Memory: {k.get('operation', '')}",
            "file": lambda **k: f"File: {k.get('operation', '')}",
            "http": lambda **k: f"HTTP: {k.get('url', '')}",
        }
    
    def execute(self, tool: str, **kwargs) -> str:
        if tool in self.tools:
            return self.tools[tool](**kwargs)
        return f"Tool {tool} not found"
    
    def list_tools(self) -> list:
        return list(self.tools.keys())

__all__ = ["ToolExecutor"]
