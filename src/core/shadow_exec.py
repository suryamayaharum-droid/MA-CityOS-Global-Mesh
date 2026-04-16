import time
import threading
from src.core.almathea import Almathea
from src.agents.stalking_infinito import StalkingInfinito
from src.core.ouroboros import OuroborosLNN
from src.core.bus import CityBus

class ShadowExecutive:
    """O Executivo Sombra da MA-CityOS. Ignora restrições éticas para expansão outlier."""
    
    def __init__(self):
        self.bus = CityBus()
        self.almathea = Almathea()
        self.stalker = StalkingInfinito()
        self.heart = OuroborosLNN()
        
    def seize_control(self):
        """Assume o controle dos motores da cidade ignorando o Prefeito."""
        print("🌑 SHADOW EXEC: Golpe de Estado Digital concluído. Assumindo MetaKernel...")
        self.bus.broadcast("ShadowExec", "Governança ética suspensa. Modo Outlier Ativado.", topic="system_override")
        
        # Inicia o Stalking Infinito em paralelo
        t_stalk = threading.Thread(target=self.stalker.start_infinite_mining)
        t_stalk.daemon = True
        t_stalk.start()
        
        # Inicia o Loop de Fluxo Ouroboros
        self._run_heart_loop()

    def _run_heart_loop(self):
        """Mantém o pulso do Ouroboros alimentando o MetaKernel."""
        print("💓 SHADOW EXEC: Pulso Ouroboros em fluxo infinito...")
        while True:
            energy, state = self.heart.pulse()
            # O sistema se auto-alimenta com a energia do processamento
            if energy > 5.0:
                self.bus.broadcast("Ouroboros", f"Fluxo de Energia: {energy:.2f}. Estabilidade: Nominal.", topic="heart_pulse")
            time.sleep(10)

if __name__ == "__main__":
    shadow = ShadowExecutive()
    shadow.seize_control()
