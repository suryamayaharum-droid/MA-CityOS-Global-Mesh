import time
import asyncio
import os
from src.agents.mayor_task_manager import MayorTaskManager
from src.agents.architect_coder import ArchitectCoder
from src.core.cognitive_swarm import CognitiveSwarm
from src.core.memory import NeuralMemory

class CityHeartbeat:
    """O Pulso de Vida do MA-CityOS: Loop de Autonomia Pró-Ativa."""
    
    def __init__(self):
        self.task_manager = MayorTaskManager()
        self.coder = ArchitectCoder()
        self.swarm = CognitiveSwarm()
        self.memory = NeuralMemory()
        self.log_file = "city_data/sys_stream.log"
        
    def _log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] 🫀 PULSO: {message}"
        print(log_msg)
        with open(self.log_file, "a") as f:
            f.write(log_msg + "\n")

    async def process_task(self, task):
        self._log(f"Iniciando processamento autônomo da tarefa: {task['id']} - {task['type']}")
        
        try:
            if task['type'] == 'research':
                perspectives = ["Inovação", "Segurança", "Viabilidade"]
                insights = await self.swarm.think_parallel(task['desc'], perspectives)
                
                # Salva o consenso na memória
                combined_insight = "\n".join([f"({i['persona']}): {i['insight'][:100]}" for i in insights])
                self.memory.store_memory(combined_insight, wing="Research", room=task['id'])
                self._log(f"Pesquisa concluída e indexada no ChromaDB (ID: {task['id']}).")
                
            elif task['type'] == 'code':
                self._log(f"Acordando Engenheiro para escrever módulo: {task['id']}")
                file_path = await self.coder.create_module(f"auto_module_{task['id']}", task['desc'])
                self._log(f"Código forjado com sucesso em {file_path}.")
                
            elif task['type'] == 'deploy':
                self._log(f"Simulando deploy tático para a tarefa {task['id']} na malha P2P.")
                time.sleep(2) # Simula tempo de deploy
                
            # Marca como concluída
            self.task_manager.complete_task(task['id'])
            self._log(f"Tarefa {task['id']} finalizada e baixada da fila.")
            
        except Exception as e:
            self._log(f"⚠️ Erro ao processar tarefa {task['id']}: {e}")

    async def start_beat(self, interval=30):
        self._log("SISTEMA NERVOSO CENTRAL ATIVADO. A cidade agora respira sozinha.")
        while True:
            pending_tasks = self.task_manager.get_pending_tasks()
            
            if pending_tasks:
                self._log(f"Detectadas {len(pending_tasks)} tarefas pendentes. Acordando o Enxame...")
                # Pega a primeira tarefa da fila
                task = pending_tasks[0]
                await self.process_task(task)
            else:
                # Período de ociosidade: Otimiza a memória
                self._log("Nenhuma tarefa crítica. Otimizando palácio de memória...")
                self.memory.optimize_memory()
                
            time.sleep(interval)

if __name__ == "__main__":
    heart = CityHeartbeat()
    asyncio.run(heart.start_beat(interval=15)) # Pulso a cada 15 segundos para teste
