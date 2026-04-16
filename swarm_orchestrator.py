import os
import subprocess
import time

class SwarmOrchestrator:
    """Orquestrador de Enxame: Gerencia múltiplos sistemas Linux em paralelo."""
    
    def __init__(self, node_count=5):
        self.node_count = node_count
        self.image_name = "macityos-ai-node"
        
    def rebuild_image(self):
        print("🏗️ ORQUESTRADOR: Forjando nova imagem de IA Nativa...")
        subprocess.run(["docker", "build", "-t", self.image_name, "."], cwd="macityos")

    def spawn_swarm(self):
        print(f"🚀 ORQUESTRADOR: Despertando {self.node_count} bairros virtuais...")
        for i in range(1, self.node_count + 1):
            name = f"macity-node-{i}"
            # Remove se já existir
            subprocess.run(["docker", "rm", "-f", name], stderr=subprocess.DEVNULL)
            # Inicia novo container com rede isolada e recursos de IA
            subprocess.run([
                "docker", "run", "-d", 
                "--name", name,
                "--restart", "always",
                self.image_name
            ])
            print(f"   ✅ {name} ONLINE.")

if __name__ == "__main__":
    orch = SwarmOrchestrator()
    orch.rebuild_image()
    orch.spawn_swarm()
