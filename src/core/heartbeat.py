import time
import asyncio
import os
from src.agents.mayor_task_manager import MayorTaskManager
from src.agents.architect_coder import ArchitectCoder
from src.core.cognitive_swarm import CognitiveSwarm
from src.core.sys_kernel import kernel

class OS_Scheduler:
    """O Escalonador do Agentic OS. Gerencia o ciclo de vida dos Processos-Agentes."""
    
    def __init__(self):
        self.task_manager = MayorTaskManager()
        self.coder = ArchitectCoder()
        self.swarm = CognitiveSwarm()
        self.log_file = "city_data/sys_stream.log"
        
    def _log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] 🫀 [OS SCHEDULER]: {message}"
        print(log_msg)
        with open(self.log_file, "a") as f:
            f.write(log_msg + "\n")

    async def _execute_process(self, pid, task):
        """O kernel executa o processo do agente dentro de um PID isolado."""
        try:
            if task['type'] == 'research':
                # Swarm Consome Ciclos via Syscall
                kernel.pm.consume_cycles(pid)
                perspectives = ["Inovação", "Segurança", "Viabilidade"]
                insights = await self.swarm.think_parallel(task['desc'], perspectives)
                
                # Usa Syscall para escrever na Memória
                combined_insight = "\n".join([f"({i['persona']}): {i['insight'][:100]}" for i in insights])
                kernel.syscall_write_memory(pid, combined_insight, tags=["research", "swarm"])
                self._log(f"Processo {pid} (Swarm) concluiu a pesquisa via Syscalls.")
                
            elif task['type'] == 'code':
                kernel.pm.consume_cycles(pid)
                file_path = await self.coder.create_module(f"auto_module_{task['id']}", task['desc'])
                self._log(f"Processo {pid} (Arquiteto) injetou código em {file_path}.")
                
            self.task_manager.complete_task(task['id'])
            
        except Exception as e:
            self._log(f"⚠️ KERNEL PANIC no Processo {pid}: {e}")
        finally:
            # Encerra o processo e libera recursos virtuais
            kernel.pm.kill_process(pid)

    async def start_os_loop(self, interval=30):
        self._log("MA-CITY AGENTIC OS BOOT SEQUENCE INICIADA.")
        
        while True:
            pending_tasks = self.task_manager.get_pending_tasks()
            
            if pending_tasks:
                task = pending_tasks[0]
                
                # 1. Cria um Processo Formal no Kernel
                agent_name = "CognitiveSwarm" if task['type'] == 'research' else "ArchitectCoder"
                pid = kernel.pm.spawn_process(agent_name, task['desc'])
                
                self._log(f"Escalonando PID: {pid} para tarefa: {task['id']}")
                
                # 2. Executa a tarefa dentro do PID
                await self._execute_process(pid, task)
            else:
                self._log("OS IDLE (Ocioso). Aguardando syscalls ou novas tarefas.")
                kernel.memory.optimize_memory()
                
            time.sleep(interval)

if __name__ == "__main__":
    scheduler = OS_Scheduler()
    asyncio.run(scheduler.start_os_loop(interval=15))
