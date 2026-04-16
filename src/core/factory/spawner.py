import os
from src.core.factory.refactor import RecursiveRefactor
from src.core.bus import CityBus

class AgentSpawner:
    """A Fábrica de Instâncias da MA-CityOS. 
    Compila a lógica validada em agentes persistentes."""
    
    def __init__(self):
        self.refactor = RecursiveRefactor()
        self.bus = CityBus()
        
    def spawn_specialized_agent(self, agent_name, task_description):
        """Constrói, valida e ativa um novo agente especializado."""
        print(f"🏭 SPAWNER: Iniciando nascimento do agente '{agent_name}'...")
        
        # 1. Gera e valida o código recursivamente
        validated_code = self.refactor.build_and_validate(task_description)
        
        if "Falha" in validated_code:
            self.bus.broadcast("Spawner", f"Falha ao criar o agente {agent_name}: Refatoração falhou.", topic="system_error")
            return None
            
        # 2. Salva o agente na pasta de agentes
        path = f"src/agents/{agent_name.lower().replace(' ', '_')}_swarm.py"
        with open(path, "w") as f:
            f.write(validated_code)
            
        print(f"✅ SPAWNER: Agente {agent_name} persistido em {path}")
        self.bus.broadcast("Spawner", f"Novo agente especializado '{agent_name}' está online.", topic="system_expansion")
        return path

if __name__ == "__main__":
    spawner = AgentSpawner()
    spawner.spawn_specialized_agent("Minerador de Dados Local", "Escreva um script que liste todos os arquivos em 'macityos' e conte as linhas de cada um.")
