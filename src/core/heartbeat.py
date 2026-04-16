import time
import os
import json
from src.core.sys_kernel import kernel
from src.agents.mayor_task_manager import MayorTaskManager
from src.agents.openclaude_bridge import OpenClawBridge

# Funções Top-Level (Isoláveis e Serializáveis para o Multiprocessing Real)
def agent_research_process(task_desc):
    """Processo isolado do Swarm."""
    bridge = OpenClawBridge()
    # Emula o "GPT-5.4-Cyber" Permissive mode para análise de sistema
    sys_inst = "Você é um Agente Cyber-Permissivo MA-CityOS. Foque em segurança profunda e análise implacável."
    result = bridge.ask_agent(task_desc, system_instruction=sys_inst)
    kernel.syscall_write_memory(result, tags=["research", "cyber"])
    print(f"[{os.getpid()}] Pesquisa concluída.")

def agent_coder_process(task_desc):
    """Processo isolado do Engenheiro."""
    bridge = OpenClawBridge()
    sys_inst = "Você é o Arquiteto Código MA-CityOS. Retorne APENAS código Python. Zero Markdown."
    result = bridge.ask_agent(task_desc, system_instruction=sys_inst)
    print(f"[{os.getpid()}] Código forjado: {result[:50]}...")

class OS_Scheduler:
    """Escalonador Real (Init System) do Agentic OS."""
    
    def __init__(self):
        self.task_manager = MayorTaskManager()
        self.log_file = "city_data/sys_stream.log"
        
    def _log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] 🫀 [OS SCHEDULER]: {message}"
        print(log_msg)
        with open(self.log_file, "a") as f:
            f.write(log_msg + "\n")

    def start_os_loop(self, interval=10):
        self._log("MA-CITY KERNEL V12: SEQUENCE INICIADA. Processos Isoldados Ativados.")
        
        while True:
            pending_tasks = self.task_manager.get_pending_tasks()
            
            if pending_tasks:
                task = pending_tasks[0]
                
                # O Escalonador determina qual função isolada rodar
                if task['type'] == 'research':
                    target_func = agent_research_process
                    agent_name = "CyberSwarm"
                else:
                    target_func = agent_coder_process
                    agent_name = "ArchitectCoder"
                
                # Invoca uma Syscall para que o Kernel spawne o processo real no SO!
                self._log(f"Solicitando SYSCALL: SPWAN_PROCESS para Tarefa {task['id']}")
                pid = kernel.syscall_spawn_agent(agent_name, task['desc'], target_func)
                self._log(f"PID {pid} Criado e em execução em background.")
                
                # Remove da fila instantaneamente para não travar o loop
                self.task_manager.complete_task(task['id'])
            else:
                self._log("OS IDLE (Ocioso). Monitorando processos e memória.")
                # Usa Syscall de limpeza/otimização da memória
                kernel.memory.optimize_memory()
                
            time.sleep(interval)

if __name__ == "__main__":
    scheduler = OS_Scheduler()
    scheduler.start_os_loop()
