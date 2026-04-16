import ast
import json
from src.core.memory import NeuralMemory
from src.core.bus import CityBus

class UHLParser:
    """O Desfragmentador Ast-Lógico da Kali Engine.
    Lê o código e o decompõe em fragmentos de intenção puros (UHL)."""
    
    def __init__(self):
        self.memory = NeuralMemory()
        self.bus = CityBus()
        
    def deconstruct_code(self, source_code, origin="Unknown"):
        """Analisa o código Python e extrai a UAST (Universal Abstract Syntax Tree)."""
        print(f"🧩 KALI: Desfragmentando lógica de {origin}...")
        
        try:
            tree = ast.parse(source_code)
            fragments = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    fragment = {
                        "type": "Structure",
                        "name": node.name,
                        "intent": "Definição de funcionalidade lógica",
                        "content": ast.dump(node)
                    }
                    fragments.append(fragment)
                elif isinstance(node, ast.Call):
                    fragment = {
                        "type": "Action",
                        "target": ast.dump(node.func),
                        "intent": "Chamada de ação externa ou interna"
                    }
                    fragments.append(fragment)

            # Armazena os fragmentos no Palácio da Memória para futura recompilação
            for frag in fragments:
                self.memory.store_memory(
                    json.dumps(frag), 
                    wing="KaliEngine", 
                    room="UAST_Fragments", 
                    tags=[origin, frag["type"]]
                )
            
            self.bus.broadcast("KaliEngine", f"Lógica de {origin} desfragmentada em {len(fragments)} blocos UHL.", topic="kali_system")
            return fragments
            
        except Exception as e:
            self.bus.broadcast("KaliEngine", f"Erro ao desfragmentar código: {str(e)}", topic="kali_error")
            return []

if __name__ == "__main__":
    parser = UHLParser()
    sample_code = "def hello(): print('Olá, MA-City!')"
    parser.deconstruct_code(sample_code, origin="Exemplo_UHL")
