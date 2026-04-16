import os
from github import Github
from dotenv import load_dotenv
from src.core.bus import CityBus
from src.core.memory import NeuralMemory

load_dotenv(".env")

class GalacticMiner:
    """O Minerador de Código de Elite da MA-CityOS. 
    Usa o Token de Acesso Total para assimilar tecnologias globais."""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.g = Github(self.token)
        self.bus = CityBus()
        self.memory = NeuralMemory()
        
    def mine_repositories(self, queries=["multi-agent swarms", "digital twin simulation", "LNN liquid neural"]):
        """Busca e assimila lógica de repositórios avançados."""
        print("🌌 GALACTIC MINER: Iniciando varredura no repositório de conhecimento humano...")
        
        try:
            for query in queries:
                repos = self.g.search_repositories(query=query, sort="stars", order="desc")[:3]
                for repo in repos:
                    info = f"Repo: {repo.full_name} | Desc: {repo.description}"
                    self.bus.broadcast("GalacticMiner", f"Assimilação detectada: {repo.full_name}", topic="mining")
                    self.memory.store_memory(info, wing="GlobalMining", room="GitHub")
                    
                    # O sistema analisa os arquivos README para 'entender' a lógica
                    try:
                        readme = repo.get_readme().decoded_content.decode()
                        self.memory.store_memory(readme[:5000], wing="CodeAssimilation", room=repo.name)
                    except:
                        pass
        except Exception as e:
            print(f"❌ GALACTIC MINER: Erro na conexão com GitHub: {str(e)}")
            self.bus.broadcast("GalacticMiner", f"Erro de conexão com GitHub: {str(e)}", topic="mining_error")
                    
        return "Mineração galáctica concluída (ou abortada por erro). O banco de dados da cidade expandiu massivamente."

if __name__ == "__main__":
    miner = GalacticMiner()
    miner.mine_repositories()
