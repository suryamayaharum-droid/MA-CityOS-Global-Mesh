import os
import json
from src.agents.openclaude_bridge import OpenClawBridge
from src.core.memory import NeuralMemory

class IntegrationAgent:
    """O Agente de Integração: Transforma repositórios brutos em habilidades para a cidade."""
    
    def __init__(self):
        self.bridge = OpenClawBridge()
        self.memory = NeuralMemory()
        self.allies_dir = "city_data/Allies"
        
    def learn_from_allies(self):
        """Varre os aliados, resume seus propósitos e armazena na memória neural."""
        print("🧠 INTEGRAÇÃO: Iniciando processo de aprendizado coletivo...")
        
        if not os.path.exists(self.allies_dir):
            return "❌ Erro: Diretório de aliados não encontrado."
            
        allies = os.listdir(self.allies_dir)
        knowledge_base = []
        
        for ally in allies:
            path = os.path.join(self.allies_dir, ally)
            if os.path.isdir(path):
                print(f"📖 Lendo documentação de: {ally}...")
                
                # Tenta ler README ou arquivos de config
                readme_path = os.path.join(path, "README.md")
                summary = ""
                
                if os.path.exists(readme_path):
                    with open(readme_path, "r", errors="ignore") as f:
                        content = f.read()[:2000] # Pega o início para contexto
                        
                        prompt = f"""
                        Analise o conteúdo deste README do projeto '{ally}' e resuma em 3 pontos:
                        1. Qual o objetivo principal do projeto?
                        2. Quais as 3 principais funcionalidades?
                        3. Como ele pode ajudar o MA-CityOS (um sistema de enxame de agentes)?
                        """
                        summary = self.bridge.ask_agent(prompt, system_instruction="Você é o Analista de Integração do MA-CityOS.")
                
                # Armazena na Memória Neural (ChromaDB)
                mem_id = self.memory.store_memory(
                    content=summary if summary else f"Projeto aliado: {ally}",
                    wing="Allies",
                    room=ally,
                    tags=["skill", "integration", ally]
                )
                
                knowledge_base.append({"name": ally, "summary": summary, "mem_id": mem_id})
                
        # Salva o mapa de habilidades atualizado
        with open("city_data/skills_map.json", "w") as f:
            json.dump(knowledge_base, f, indent=4)
            
        print(f"✅ APRENDIZADO CONCLUÍDO: {len(knowledge_base)} aliados integrados à consciência da cidade.")
        return knowledge_base

if __name__ == "__main__":
    ia = IntegrationAgent()
    ia.learn_from_allies()
