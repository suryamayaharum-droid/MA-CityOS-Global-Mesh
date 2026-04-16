from src.core.soul import CitySoul
from src.core.kernel import CognitiveKernel
import json

class DigitalBrain:
    """O cérebro híbrido da fábrica de agentes. 
    Inspirado na lógica Capybara (Anthropic Mythos)."""
    
    def __init__(self):
        self.soul = CitySoul()
        self.kernel = CognitiveKernel()
        
    def evaluate_task(self, task_description):
        """Avalia a tarefa e decide o recurso cognitivo ideal."""
        # Se a tarefa envolver 'codificação', 'criação' ou 'estratégia', usa a Alma (LLM)
        if any(word in task_description.lower() for word in ["criar", "codificar", "refatorar", "estratégia"]):
            return "Soul"
        # Para lógica de fluxo simples ou decisões axiomáticas, usa o Kernel Nativo
        return "Kernel"

    def generate_solution(self, task_description):
        """Gera uma solução baseada na avaliação cognitiva."""
        engine = self.evaluate_task(task_description)
        
        if engine == "Soul":
            prompt = (
                f"Tarefa Capybara: {task_description}. "
                "Gere uma solução técnica inovadora em Python puro que possa ser executada nativamente. "
                "Não inclua nenhuma explicação, apenas o código Python puro."
            )
            raw_code = self.soul.think(prompt, system_instruction="Você é o Cérebro Digital Capybara da MA-CityOS.")
            return self.sanitize_code(raw_code)
        else:
            return self.kernel.reason(task_description)

    def sanitize_code(self, raw_code):
        """Remove blocos de markdown e outros ruídos do código gerado."""
        lines = raw_code.split("\n")
        clean_lines = []
        in_code_block = False
        for line in lines:
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if not in_code_block and not line.strip():
                continue
            clean_lines.append(line)
        return "\n".join(clean_lines)

if __name__ == "__main__":
    brain = DigitalBrain()
    print(f"🧠 Cérebro Digital: {brain.generate_solution('Codificar um agente de segurança')}")
