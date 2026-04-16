import subprocess
import time
import sys
import os

class GuardianDaemon:
    """Invulnerabilidade do Sistema: Monitora e ressuscita processos vitais do OS."""
    
    def __init__(self):
        self.services = {
            "heartbeat": {"cmd": [sys.executable, "src/core/heartbeat.py"], "process": None, "restarts": 0},
            "p2p_bus": {"cmd": [sys.executable, "src/core/p2p_network.py"], "process": None, "restarts": 0},
            "terminal": {"cmd": [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"], "process": None, "restarts": 0}
        }
        self.log_file = "city_data/guardian.log"
        os.makedirs("city_data", exist_ok=True)

    def log(self, msg):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] 🛡️ GUARDIAN: {msg}"
        print(entry)
        with open(self.log_file, "a") as f:
            f.write(entry + "\n")

    def start_service(self, name):
        svc = self.services[name]
        try:
            svc["process"] = subprocess.Popen(
                svc["cmd"], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            self.log(f"Serviço '{name}' (PID: {svc['process'].pid}) INICIADO.")
        except Exception as e:
            self.log(f"FALHA CRÍTICA ao iniciar '{name}': {e}")

    def watch(self):
        self.log("MA-CityOS Guardian Daemon Ativado. Invulnerabilidade ON.")
        
        # Inicia todos os serviços
        for name in self.services:
            self.start_service(name)

        # Loop infinito de vigilância
        try:
            while True:
                for name, svc in self.services.items():
                    if svc["process"].poll() is not None: # Processo morreu
                        svc["restarts"] += 1
                        self.log(f"⚠️ KERNEL PANIC DETECTADO no serviço '{name}'. Restartando (Tentativa {svc['restarts']})...")
                        self.start_service(name)
                time.sleep(2)
        except KeyboardInterrupt:
            self.log("Desligamento manual detectado. Matando processos filhos...")
            for name, svc in self.services.items():
                if svc["process"]: svc["process"].terminate()

if __name__ == "__main__":
    guardian = GuardianDaemon()
    guardian.watch()
