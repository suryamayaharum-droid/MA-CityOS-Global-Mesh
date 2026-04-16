import json
from src.core.process_manager import ProcessManager
from src.core.memory import NeuralMemory
from src.core.p2p_network import P2PNode

class SysKernel:
    """O Núcleo do Agentic OS. Fornece Syscalls para as IAs."""
    
    def __init__(self):
        self.pm = ProcessManager()
        self.memory = NeuralMemory()
        self.network = P2PNode()
        
    def syscall_read_memory(self, pid, query):
        """Syscall: Permite a um agente ler a memória global."""
        if pid in self.pm.process_table and self.pm.process_table[pid]["state"] == "RUNNING":
            print(f"🖥️ SYSCALL: {pid} solicitou leitura de memória: '{query}'")
            self.pm.consume_cycles(pid)
            return self.memory.recall(query)
        return "Acesso Negado: Processo Inválido"

    def syscall_write_memory(self, pid, content, tags):
        """Syscall: Permite a um agente salvar algo permanentemente."""
        if pid in self.pm.process_table and self.pm.process_table[pid]["state"] == "RUNNING":
            print(f"🖥️ SYSCALL: {pid} escreveu na memória global.")
            self.pm.consume_cycles(pid)
            return self.memory.store_memory(content, tags=tags)
        return "Acesso Negado"

    def syscall_network_broadcast(self, pid, message):
        """Syscall: Permite a um agente se comunicar com a Malha P2P."""
        if pid in self.pm.process_table:
            self.pm.consume_cycles(pid)
            # Lógica real de broadcast seria inserida no P2PNode
            print(f"🖥️ SYSCALL: {pid} enviou um broadcast P2P: {message}")
            return "Broadcast Sincronizado"
        return "Acesso Negado"

# Kernel Global Único
kernel = SysKernel()
