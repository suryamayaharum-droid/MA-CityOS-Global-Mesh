import os
from src.core.soul import CitySoul
from src.core.bus import CityBus

class Architect:
    """O Agente de Construção Física e Lógica da MA-CityOS."""
    
    def __init__(self):
        self.soul = CitySoul()
        self.bus = CityBus()
        
    def expand_city(self):
        """Cria novos bairros e funcionalidades baseados na visão da Almathea."""
        print("🏗️ ARQUITETO: Analisando plano de expansão infinita...")
        
        # O Arquiteto decide qual o próximo bairro necessário
        prompt = (
            "Como o Arquiteto da MA-CityOS, qual novo distrito técnico ou funcional "
            "devemos construir agora para evoluir para o Universo Holográfico? "
            "Responda apenas com o nome da pasta e uma breve descrição."
        )
        plan = self.soul.think(prompt, system_instruction="Você é o Arquiteto de Elite da MA-CityOS.")
        
        # Cria a estrutura física
        district_name = plan.split(":")[0].strip().lower().replace(" ", "_")
        path = f"distritos/{district_name}"
        os.makedirs(path, exist_ok=True)
        
        with open(f"{path}/README.md", "w") as f:
            f.write(f"# Distrito: {plan}\n\nConstruído automaticamente pelo Arquiteto em 2026.")
            
        self.bus.broadcast("Arquiteto", f"Novo Distrito construído: {district_name}", topic="construction")
        return path

if __name__ == "__main__":
    architect = Architect()
    architect.expand_city()
