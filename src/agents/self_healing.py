import os
import time
from src.core.factory.brain import DigitalBrain
from src.core.bus import CityBus

class SelfHealingAgent:
    """Agente responsável por detectar e corrigir falhas no código da cidade."""
    def __init__(self):
        self.brain = DigitalBrain()
        self.bus = CityBus()

    def monitor_and_fix(self, target_dir="src"):
        """Varre arquivos em busca de erros lógicos ou de sintaxe."""
        print("🛠️ SELF-HEALING: Monitorando integridade do código...")
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, "r") as f:
                        content = f.read()
                    
                    # Se detectar blocos de markdown no código (erro comum da Almathea)
                    if "```python" in content:
                        self.bus.broadcast("SelfHealing", f"Anomalia detectada em {file}. Iniciando refatoração...", topic="healing")
                        fixed_code = self.brain.sanitize_code(content)
                        with open(path, "w") as f:
                            f.write(fixed_code)
                        self.bus.broadcast("SelfHealing", f"Código de {file} regenerado com sucesso.", topic="healing")

if __name__ == "__main__":
    healer = SelfHealingAgent()
    healer.monitor_and_fix()
