import time
import uuid

class ProcessManager:
    """Gerenciador de Processos do MA-CityOS (Equivalente ao 'top' no Linux)."""
    
    def __init__(self):
        self.process_table = {}
        
    def spawn_process(self, agent_name, task_desc, priority=1):
        pid = f"PID-{str(uuid.uuid4())[:6]}"
        self.process_table[pid] = {
            "agent": agent_name,
            "task": task_desc,
            "state": "RUNNING",
            "priority": priority,
            "started_at": time.time(),
            "cpu_cycles": 0
        }
        print(f"⚙️ [OS MANAGER] Processo Criado: {pid} [{agent_name}]")
        return pid
        
    def kill_process(self, pid):
        if pid in self.process_table:
            self.process_table[pid]["state"] = "TERMINATED"
            print(f"🛑 [OS MANAGER] Processo Encerrado: {pid}")
            return True
        return False
        
    def get_process_list(self):
        return self.process_table

    def consume_cycles(self, pid):
        if pid in self.process_table:
            self.process_table[pid]["cpu_cycles"] += 1
