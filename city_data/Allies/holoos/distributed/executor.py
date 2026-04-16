"""HoloOS Distributed Executor"""
import time
from typing import Dict, List, Callable, Any

class Worker:
    def __init__(self, id: str, capabilities: List[str]):
        self.id = id
        self.status = "idle"
        self.capabilities = capabilities
        self.last_seen = time.time()

class DistributedExecutor:
    def __init__(self):
        self.workers: Dict[str, Worker] = {}
        self.tasks: Dict[str, dict] = {}
    
    def register(self, worker_id: str, capabilities: List[str]) -> None:
        self.workers[worker_id] = Worker(worker_id, capabilities)
    
    def submit(self, task_id: str, func: Callable, *args, **kwargs) -> None:
        self.tasks[task_id] = {"func": func, "args": args, "kwargs": kwargs, "status": "pending", "result": None}
    
    def execute(self, task_id: str, worker_id: str) -> Any:
        if task_id in self.tasks and worker_id in self.workers:
            task = self.tasks[task_id]
            worker = self.workers[worker_id]
            worker.status = "busy"
            try:
                task["result"] = task["func"](*task["args"], **task["kwargs"])
                task["status"] = "done"
            except Exception as e:
                task["result"] = str(e)
                task["status"] = "failed"
            worker.status = "idle"
            return task["result"]
        return None
    
    def get_status(self) -> Dict:
        return {"workers": len(self.workers), "tasks": len(self.tasks)}

__all__ = ["DistributedExecutor", "Worker"]