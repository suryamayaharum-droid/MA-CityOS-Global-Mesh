import json
from src.core.process_manager import RealProcessManager
from src.core.memory import NeuralMemory
from src.core.p2p_network import P2PNode

class SysKernel:
    """O Núcleo V12: Syscalls e Gestão de Multiprocessing Real."""
    
    def __init__(self):
        self.pm = RealProcessManager()
        self.memory = NeuralMemory()
        
    def syscall_read_memory(self, query):
        """Syscall livre para leitura do ChromaDB."""
        return self.memory.recall(query)

    def syscall_write_memory(self, content, tags):
        """Syscall livre para gravação na Memória de Longo Prazo."""
        return self.memory.store_memory(content, tags=tags)

    def syscall_spawn_agent(self, agent_name, task_desc, target_function):
        """Syscall: O SO cria um processo real (Multiprocessing) para o agente."""
        return self.pm.spawn_process(agent_name, task_desc, target_function)

    def syscall_get_processes(self):
        return self.pm.get_process_list()

# Kernel Global Único (Singleton)
kernel = SysKernel()
