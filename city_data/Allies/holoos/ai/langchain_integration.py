"""HoloOS LangChain Integration

Integra com LangChain para:
- Chains (sequência de operações)
- Agents (ação autônoma)
- Memory (memória persistente)
- Tools (ferramentas)
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass

@dataclass
class ChainStep:
    name: str
    func: Callable
    input_key: str
    output_key: str

class Chain:
    """Cadeia de operações LangChain-style"""
    
    def __init__(self, name: str):
        self.name = name
        self.steps: List[ChainStep] = []
    
    def add_step(self, name: str, func: Callable, input_key: str, output_key: str) -> None:
        self.steps.append(ChainStep(name, func, input_key, output_key))
    
    def run(self, input_data: Dict) -> Dict:
        """Executa a cadeia"""
        data = input_data.copy()
        for step in self.steps:
            result = step.func(data.get(step.input_key, ""))
            data[step.output_key] = result
        return data

class Agent:
    """Agente estilo LangChain"""
    
    def __init__(self, name: str, tools: List[Callable]):
        self.name = name
        self.tools = tools
        self.history: List[Dict] = []
    
    def run(self, task: str) -> str:
        """Executa tarefa usando tools"""
        self.history.append({"task": task, "action": "processing"})
        
        # Simple tool selection
        for tool in self.tools:
            if callable(tool):
                return f"[{self.name}] Executando: {task[:30]}... → {tool()}"
        
        return f"[{self.name}] Tarefa: {task[:50]}..."

class Memory:
    """Memória estilo LangChain"""
    
    def __init__(self):
        self.buffer: List[str] = []
        self.max_tokens = 2000
    
    def add(self, text: str) -> None:
        self.buffer.append(text)
        # Trim if needed
        while sum(len(t.split()) for t in self.buffer) > self.max_tokens:
            self.buffer.pop(0)
    
    def get_context(self) -> str:
        return "\n".join(self.buffer[-5:])

class LangChainIntegration:
    """Integração principal com LangChain"""
    
    def __init__(self):
        self.chains: Dict[str, Chain] = {}
        self.agents: Dict[str, Agent] = {}
        self.memory = Memory()
    
    def create_chain(self, name: str) -> Chain:
        chain = Chain(name)
        self.chains[name] = chain
        return chain
    
    def create_agent(self, name: str, tools: List[Callable]) -> Agent:
        agent = Agent(name, tools)
        self.agents[name] = agent
        return agent
    
    def add_memory(self, text: str) -> None:
        self.memory.add(text)
    
    def get_context(self) -> str:
        return self.memory.get_context()
    
    def get_status(self) -> Dict:
        return {
            "chains": len(self.chains),
            "agents": len(self.agents),
            "memory_tokens": sum(len(t.split()) for t in self.memory.buffer),
        }

__all__ = ["Chain", "Agent", "Memory", "LangChainIntegration"]
