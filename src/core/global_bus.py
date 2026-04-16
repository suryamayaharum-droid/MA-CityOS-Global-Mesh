import os
import json
import base64
from github import Github
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(".env")

class GlobalBus:
    """O Túnel Nativo da MA-CityOS. 
    Sincroniza todas as instâncias do ecossistema via GitHub."""
    
    def __init__(self, repo_name="MA-CityOS-Global-Mesh"):
        self.token = os.getenv("GITHUB_TOKEN")
        self.g = Github(self.token)
        self.repo_name = repo_name
        self._initialize_mesh_repo()
        
    def _initialize_mesh_repo(self):
        """Cria ou conecta ao repositório de sincronização global."""
        user = self.g.get_user()
        try:
            self.repo = user.get_repo(self.repo_name)
        except:
            print(f"🌐 MESH: Criando Malha Digital Global: {self.repo_name}")
            self.repo = user.create_repo(self.repo_name, private=True, auto_init=True)

    def send_global_signal(self, sender, message, topic="mesh"):
        """Envia um sinal para todas as instâncias da malha."""
        timestamp = datetime.now().isoformat()
        payload = {
            "timestamp": timestamp,
            "sender": sender,
            "message": message,
            "instance_id": os.uname().nodename
        }
        
        path = f"signals/{timestamp}_{sender}.json"
        content = json.dumps(payload, indent=2)
        
        # Cria o sinal no GitHub (o Túnel)
        self.repo.create_file(path, f"Signal from {sender}", content)
        print(f"📡 [GLOBAL-MESH] Sinal enviado de {payload['instance_id']}")

    def sync_memory(self):
        """Sincroniza o estado da memória entre as instâncias."""
        # Aqui o sistema baixa os últimos sinais e atualiza o ChromaDB local
        pass

if __name__ == "__main__":
    gbus = GlobalBus()
    gbus.send_global_signal("CloudShell_Origin", "Malha Digital Ativada. Aguardando outras instâncias.")
