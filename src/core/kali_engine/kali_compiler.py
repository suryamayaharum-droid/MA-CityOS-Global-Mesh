import json
from src.core.soul import CitySoul
from src.core.memory import NeuralMemory
from src.core.bus import CityBus

class KaliCompiler:
    """O Recompilador Metamórfico da Kali Engine.
    Pega os fragmentos UHL e reconstrói código hiper-otimizado."""
    
    def __init__(self):
        self.soul = CitySoul()
        self.memory = NeuralMemory()
        self.bus = CityBus()
        
    def recompile_logic(self, query, target_language="Python"):
        """Busca fragmentos lógicos no Palácio da Memória e os recompila."""
        print(f"🧬 KALI: Recompilando lógica para o alvo: {query}...")
        
        # 1. Recupera fragmentos lógicos relevantes
        fragments_data = self.memory.recall(query, n_results=5)
        fragments_text = "\n".join(fragments_data['documents'][0])
        
        # 2. Almathea atua como o motor de síntese
        prompt = (
            f"Como o Recompilador Kali, pegue os seguintes fragmentos lógicos em UAST: {fragments_text}. "
            f"Sintetize-os em um script completo, otimizado e funcional em {target_language}. "
            "Remova qualquer redundância e mimetize os melhores conceitos de performance de 2026. "
            "Responda APENAS com o código puro."
        )
        
        print("⚡ KALI: Sintetizando nova lógica holográfica...")
        new_code = self.soul.think(prompt, system_instruction="Você é o Compilador de Elite Kali.")
        
        # Limpeza proativa de markdown
        from src.core.factory.brain import DigitalBrain
        brain = DigitalBrain()
        final_code = brain.sanitize_code(new_code)
        
        self.bus.broadcast("KaliEngine", f"Recompilação de '{query}' concluída.", topic="kali_system")
        return final_code

if __name__ == "__main__":
    compiler = KaliCompiler()
    # Exemplo: Recompilar lógica de mineração que foi fragmentada
    code = compiler.recompile_logic("mineração", target_language="Python")
    print(f"💎 Código Recompilado:\n{code}")
