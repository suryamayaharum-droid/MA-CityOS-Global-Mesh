import os
import subprocess
import time
from src.core.bus import CityBus

class CityGuardian:
    """O Vigilante 24/7 da MA-CityOS. 
    Garante que todos os motores e agentes estejam sempre online."""
    
    def __init__(self):
        self.bus = CityBus()
        self.processes = {
            "Consolidador": ["python3", "consolidator.py"],
            "ShadowExec": ["python3", "src/core/shadow_exec.py"],
            "CyberShield": ["python3", "src/agents/cyber_shield.py"]
        }
        self.active_procs = {}

    def start_watchdog(self):
        """Inicia e monitora os processos vitais da cidade."""
        print("🛡️ GUARDIAN: Iniciando vigilância 24/7...")
        self.bus.broadcast("Guardian", "Vigilância ativa. Protegendo a integridade da cidade.", topic="system")
        
        while True:
            for name, cmd in self.processes.items():
                if name not in self.active_procs or self.active_procs[name].poll() is not None:
                    print(f"⚠️ GUARDIAN: Reiniciando {name}...")
                    self.active_procs[name] = subprocess.Popen(
                        cmd, 
                        env=dict(os.environ, PYTHONPATH=os.getcwd()),
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL
                    )
                    self.bus.broadcast("Guardian", f"Processo {name} restaurado.", topic="system_recovery")
            time.sleep(10)

if __name__ == "__main__":
    guardian = CityGuardian()
    guardian.start_watchdog()
