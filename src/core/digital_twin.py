import json
import time
from src.core.bus import CityBus

class DigitalTwinEngine:
    """O Motor de Réplica Digital do Mundo Físico da MA-CityOS."""
    
    def __init__(self, state_file="city_data/digital_twin.json"):
        self.bus = CityBus()
        self.state_file = state_file
        self.entities = self._load_state()
        
    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except: return {}
        return {}

    def _save_state(self):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(self.entities, f, indent=2)

    def sync_physical_to_digital(self, object_id, data):
        """Cria ou atualiza a réplica digital de um objeto físico."""
        self.entities[object_id] = {
            "timestamp": time.time(),
            "data": data,
            "holographic_render": True
        }
        self._save_state()
        self.bus.broadcast("DigitalTwin", f"Objeto {object_id} sincronizado com a Réplica Digital.", topic="world_replica")
        return f"Replicação Concluída: {object_id}"

    def generate_global_map(self):
        """Projeta o mapa holográfico da cidade e do mundo minerado."""
        # Aqui o sistema integraria com APIs de mapas ou dados minerados
        print("🌍 DIGITAL TWIN: Projetando Réplica Digital do Mundo Físico...")
        return self.entities

if __name__ == "__main__":
    twin = DigitalTwinEngine()
    twin.sync_physical_to_digital("Main_Server_Terminal", {"temp": "30C", "load": "low"})
    twin.generate_global_map()
