import time
import asyncio
import os
import json
from src.core.sys_kernel import kernel
from src.agents.mayor_task_manager import MayorTaskManager
from src.agents.openclaude_bridge import OpenClawBridge

# Agentes agora têm acesso ao Kernel Semântico
def agent_runtime_wrapper(task_desc):
    """Runtime Cognitivo: O ambiente de execução do agente."""
    bridge = OpenClawBridge()
    pid = os.getpid()
    
    # O agente carrega sua 'identidade' se existir
    # TODO: Implementar persistência de identidade
    
    print(f"🧠 [RUNTIME] PID {pid} executando com foco em Propósito.")
    
    # Simula o comportamento GPT-5.4 Cyber: Análise profunda
    sys_inst = "Você é um Runtime Cognitivo do MA-CityOS. Opere em modo de alta fidelidade e resolução de propósito."
    result = bridge.ask_agent(task_desc, system_instruction=sys_inst)
    
    # Escreve na memória usando o Kernel
    kernel.memory.store_memory(result, tags=["os_execution", f"pid_{pid}"])
    
    # Salva estado final
    kernel.syscall_persist_state(f"Agent_{pid}", {"last_task": task_desc, "status": "success"})

class OS_Scheduler:
    """Escalonador V13: O Orquestrador de Intenções."""
    
    def __init__(self):
        self.task_manager = MayorTaskManager()
        
    def start_os_loop(self, interval=5):
        print("🏙️ MA-CITY OS V13: COGNITIVE RUNTIME ONLINE.")
        
        while True:
            pending_tasks = self.task_manager.get_pending_tasks()
            
            if pending_tasks:
                task = pending_tasks[0]
                
                # O Kernel decide quem executa com base na intenção!
                agent_name = kernel.syscall_dispatch(task['desc'])
                
                # Spawn de processo real
                pid = kernel.syscall_spawn_agent(agent_name, task['desc'], agent_runtime_wrapper)
                
                # Marca como concluída no log de ordens
                self.task_manager.complete_task(task['id'])
                print(f"🚀 PID {pid} forjado para propósito: {agent_name}")
            
            time.sleep(interval)

if __name__ == "__main__":
    scheduler = OS_Scheduler()
    scheduler.start_os_loop()
