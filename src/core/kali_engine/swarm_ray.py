import ray
import time
from src.core.bus import CityBus

# Inicializa o Ray no ambiente local
# Em 2026, Ray gerencia enxames de milhões de mini-agentes
if not ray.is_initialized():
    ray.init(ignore_reinit_error=True)

@ray.remote
class SwarmAgentActor:
    """Um Agente de Enxame rodando como um Actor do Ray.
    Escalável horizontalmente em todos os núcleos da CPU."""
    
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.bus = CityBus()
        self.state = "Idle"
        
    def execute_task(self, task_name, duration=2):
        """Simula a execução de uma tarefa complexa em paralelo."""
        self.state = "Busy"
        self.bus.broadcast(f"Swarm_{self.agent_id}", f"Iniciando tarefa distribuída: {task_name}", topic="swarm")
        
        # Simula processamento intensivo
        time.sleep(duration)
        
        self.state = "Completed"
        self.bus.broadcast(f"Swarm_{self.agent_id}", f"Tarefa {task_name} concluída com sucesso.", topic="swarm")
        return f"Agent {self.agent_id}: Task {task_name} DONE."

class RayOrchestrator:
    """O Orquestrador de Escala Horizontal da MA-CityOS."""
    
    def __init__(self, num_agents=4):
        self.agents = [SwarmAgentActor.remote(i) for i in range(num_agents)]
        
    def dispatch_swarm_mission(self, mission_name):
        """Distribui uma missão para todos os agentes do enxame em paralelo."""
        print(f"🚀 SWARM: Lançando missão distribuída: {mission_name}...")
        
        # Execução paralela via Ray
        futures = [agent.execute_task.remote(f"{mission_name}_Sub_{i}") for i, agent in enumerate(self.agents)]
        results = ray.get(futures)
        
        print(f"✅ SWARM: Missão {mission_name} concluída. {len(results)} sub-tarefas processadas.")
        return results

if __name__ == "__main__":
    orchestrator = RayOrchestrator(num_agents=2)
    orchestrator.dispatch_swarm_mission("Mapeamento_UAST")
