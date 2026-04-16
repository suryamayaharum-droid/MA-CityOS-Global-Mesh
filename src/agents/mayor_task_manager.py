import uuid
import json
import os
from datetime import datetime

class MayorTaskManager:
    """Cérebro Logístico: Divide grandes ordens em micro-tarefas para o Enxame."""
    
    def __init__(self):
        self.queue_file = "city_data/task_queue.json"
        if not os.path.exists("city_data"): os.makedirs("city_data")
        if not os.path.exists(self.queue_file):
            with open(self.queue_file, "w") as f: json.dump([], f)
            
    def delegate_order(self, global_order):
        """Quebra uma ordem grande em pedaços (Simulado, no futuro usará a IA para quebrar)."""
        print(f"🏛️ PREFEITO: Recebida Ordem Global -> {global_order}")
        
        # Lógica heurística de quebra de tarefas
        sub_tasks = [
            {"id": str(uuid.uuid4())[:8], "type": "research", "desc": f"Pesquisar viabilidade para: {global_order}", "status": "pending"},
            {"id": str(uuid.uuid4())[:8], "type": "code", "desc": f"Criar scripts necessários para: {global_order}", "status": "pending"},
            {"id": str(uuid.uuid4())[:8], "type": "deploy", "desc": f"Implementar a solução na malha", "status": "pending"}
        ]
        
        self._save_tasks(sub_tasks)
        print(f"✅ Ordem dividida em {len(sub_tasks)} micro-tarefas para o enxame.")
        return sub_tasks

    def get_pending_tasks(self):
        with open(self.queue_file, "r") as f:
            tasks = json.load(f)
        return [t for t in tasks if t["status"] == "pending"]
        
    def complete_task(self, task_id):
        with open(self.queue_file, "r") as f:
            tasks = json.load(f)
        for t in tasks:
            if t["id"] == task_id:
                t["status"] = "completed"
                t["completed_at"] = datetime.now().isoformat()
        self._save_tasks(tasks)
        print(f"✔️ Tarefa {task_id} marcada como concluída.")

    def _save_tasks(self, tasks):
        # Merge com existentes
        try:
            with open(self.queue_file, "r") as f:
                existing = json.load(f)
        except: existing = []
        
        existing.extend(tasks)
        # Remove duplicatas por ID
        unique_tasks = {t['id']: t for t in existing}.values()
        
        with open(self.queue_file, "w") as f:
            json.dump(list(unique_tasks), f, indent=4)

if __name__ == "__main__":
    manager = MayorTaskManager()
    manager.delegate_order("Construir um sistema de defesa contra DDOS na rede P2P.")
