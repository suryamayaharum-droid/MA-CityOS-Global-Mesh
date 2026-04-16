import os
from src.core.bus import CityBus
from src.core.memory import NeuralMemory
from src.core.soul import CitySoul

class MayorAgent:
    """O Prefeito da MA-CityOS: Orquestrador Central."""
    
    def __init__(self, project_id=None):
        self.bus = CityBus()
        self.memory = NeuralMemory()
        self.soul = CitySoul()
        
    def process_order(self, user_input):
        self.bus.broadcast("Usuário", user_input, topic="ordens_diretas")
        
        # O Prefeito 'pensa' usando a alma do sistema
        response = self.soul.think(user_input, system_instruction="Você é o Prefeito da MA-CityOS. Governe com sabedoria e rapidez.")
        
        self.memory.store_memory(response, wing="Governance", room="Decisions", Hall="Mayor")
        self.bus.broadcast("Prefeito", response, topic="governanca")
        return response

if __name__ == "__main__":
    mayor = MayorAgent()
    print("🏙️ MA-CityOS: Prefeito assumiu o gabinete na Prefeitura.")
