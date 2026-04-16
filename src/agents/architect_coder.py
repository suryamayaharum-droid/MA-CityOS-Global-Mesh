import asyncio
import os
from src.agents.openclaude_bridge import OpenClawBridge

class ArchitectCoder:
    """Engenheiro Autônomo: Escreve e injeta novos módulos no MA-CityOS."""
    
    def __init__(self):
        self.bridge = OpenClawBridge()
        self.output_dir = "src/agents/generated"
        os.makedirs(self.output_dir, exist_ok=True)
        
    async def create_module(self, module_name, description):
        print(f"👨‍💻 ARQUITETO: Projetando o módulo '{module_name}'...")
        prompt = f"""
        Escreva um script Python completo e funcional para o MA-CityOS baseado nesta descrição:
        '{description}'
        
        REGRAS:
        1. Retorne APENAS código Python válido. Sem formatação Markdown (```python).
        2. O código deve ter uma classe principal e um bloco if __name__ == '__main__':
        3. Use bibliotecas padrão ou as já instaladas (httpx, json, asyncio).
        """
        
        # Chama a IA de forma assíncrona (simulada na ponte, mas encapsulada aqui)
        code = self.bridge.ask_agent(prompt, system_instruction="Você é o Engenheiro Chefe do MA-CityOS. Responda APENAS com código fonte limpo.")
        
        # Limpa o código caso a IA teime em usar markdown
        code = code.replace("```python", "").replace("```", "").strip()
        
        # Tratamento do retorno caso o bypass adicione prefixos como ✅ [ELITE]
        if "]" in code[:50]:
            code = code.split("]", 1)[1].strip()
            
        file_path = os.path.join(self.output_dir, f"{module_name}.py")
        with open(file_path, "w") as f:
            f.write(code)
            
        print(f"✅ ARQUITETO: Módulo '{module_name}' forjado e injetado em {file_path}")
        return file_path

if __name__ == "__main__":
    coder = ArchitectCoder()
    asyncio.run(coder.create_module("sensor_clima", "Um agente que busca dados de clima reais de uma API pública e salva num JSON."))
