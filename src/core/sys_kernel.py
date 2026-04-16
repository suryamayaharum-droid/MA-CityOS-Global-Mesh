import json
import os
import time
from src.core.process_manager import RealProcessManager
from src.core.memory import NeuralMemory

class SemanticBus:
    """O Barramento Semântico: Roteia intenções, não apenas dados."""
    
    def __init__(self, memory):
        self.memory = memory
        self.routes = {} # Mapeia palavras-chave para agentes especializados

    def register_route(self, keywords, agent_name):
        for kw in keywords:
            self.routes[kw.lower()] = agent_name

    def route_intent(self, intent_desc):
        """Analisa a intenção e sugere o melhor agente."""
        intent_lower = intent_desc.lower()
        for kw, agent in self.routes.items():
            if kw in intent_lower:
                return agent
        return "GeneralSwarm"

class SysKernelV13:
    """O Kernel Cognitivo: Onde o propósito é a base da execução."""
    
    def __init__(self):
        self.pm = RealProcessManager()
        self.memory = NeuralMemory()
        self.bus = SemanticBus(self.memory)
        self._initialize_default_routes()
        
    def _initialize_default_routes(self):
        self.bus.register_route(["código", "python", "script", "programar"], "ArchitectCoder")
        self.bus.register_route(["pesquisar", "analisar", "descobrir", "notícias"], "CyberSwarm")
        self.bus.register_route(["segurança", "ataque", "defesa", "proteção"], "CyberShield")

    def syscall_dispatch(self, order_desc):
        """Encaminha uma ordem para o processo correto via Barramento Semântico."""
        target_agent = self.bus.route_intent(order_desc)
        print(f"📡 KERNEL DISPATCH: Ordem '{order_desc[:30]}...' roteada para {target_agent}")
        return target_agent

    def syscall_persist_state(self, agent_name, state_data):
        """Salva o 'estado de consciência' de um agente."""
        path = f"macity_vault/identities/{agent_name}.json"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({"timestamp": time.time(), "state": state_data}, f)
        return True

# Singleton Kernel V13
kernel = SysKernelV13()
