import multiprocessing
import time
import uuid

class RealProcessManager:
    """Gerenciador de Processos Real usando Multiprocessing do Python."""
    
    def __init__(self):
        self.active_processes = {}

    def _agent_wrapper(self, pid, task_desc, target_function):
        """Isola a execução do agente para não crachar o Kernel."""
        print(f"⚙️ [KERNEL] PID {pid} INICIADO -> Tarefa: {task_desc}")
        try:
            target_function(task_desc)
            print(f"✅ [KERNEL] PID {pid} CONCLUÍDO COM SUCESSO.")
        except Exception as e:
            print(f"❌ [KERNEL] FATAL ERROR no PID {pid}: {e}")

    def spawn_process(self, agent_name, task_desc, target_function):
        pid = f"PID-{str(uuid.uuid4())[:6]}"
        
        # Cria um processo REAL no SO
        process = multiprocessing.Process(
            target=self._agent_wrapper, 
            args=(pid, task_desc, target_function),
            name=f"MA-City_{agent_name}_{pid}"
        )
        
        self.active_processes[pid] = {
            "agent": agent_name,
            "task": task_desc,
            "process_obj": process,
            "start_time": time.time()
        }
        
        process.start()
        return pid

    def cleanup_zombies(self):
        """Remove processos que já terminaram da tabela."""
        dead_pids = []
        for pid, info in self.active_processes.items():
            if not info["process_obj"].is_alive():
                dead_pids.append(pid)
        for pid in dead_pids:
            del self.active_processes[pid]
        return len(dead_pids)

    def get_process_list(self):
        self.cleanup_zombies()
        # Retorna info segura para serialização
        return {
            pid: {"agent": info["agent"], "task": info["task"], "alive": info["process_obj"].is_alive()}
            for pid, info in self.active_processes.items()
        }
