import subprocess
import os
import tempfile
from src.core.factory.brain import DigitalBrain

class RecursiveRefactor:
    """O motor de auto-escrita e refatoração recursiva. 
    Capacidade de testar e melhorar o próprio código em tempo real."""
    
    def __init__(self):
        self.brain = DigitalBrain()
        
    def build_and_validate(self, task_description, max_attempts=5):
        """Tenta construir uma solução e a refatora recursivamente até validar."""
        print(f"🛠️ RECURSIVE: Iniciando construção para: {task_description}")
        
        attempt = 0
        current_code = self.brain.generate_solution(task_description)
        
        while attempt < max_attempts:
            # 1. Verifica Sintaxe
            syntax_ok, syntax_error = self._check_syntax(current_code)
            
            if syntax_ok:
                # 2. Tenta execução real
                success, error_log = self._execute_code(current_code)
                
                if success:
                    print(f"✅ RECURSIVE: Código validado com sucesso na tentativa {attempt+1}.")
                    return current_code
                else:
                    error_to_fix = error_log
            else:
                error_to_fix = syntax_error

            print(f"❌ RECURSIVE: Falha detectada (Attempt {attempt+1}). Erro: {error_to_fix[:50]}...")
            # Refatoração proativa
            refactor_prompt = (
                f"O código falhou: {error_to_fix}. "
                f"Tarefa: {task_description}. "
                "Corrija o código Python. Use apenas bibliotecas padrão (os, sys, json). "
                "Não inclua explicações, apenas o código puro."
            )
            current_code = self.brain.soul.think(refactor_prompt, system_instruction="Você é o Cérebro Capybara de Elite.")
            current_code = self.brain.sanitize_code(current_code)
            attempt += 1
                
        return "Falha na refatoração recursiva: Limite de tentativas atingido."

    def _check_syntax(self, code):
        """Verifica a sintaxe do código antes da execução."""
        try:
            compile(code, "<string>", "exec")
            return True, None
        except SyntaxError as e:
            return False, str(e)

    def _execute_code(self, code):
        """Executa o código em um ambiente temporário e captura erros."""
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(code)
            temp_path = f.name
            
        try:
            # Executa e aguarda o resultado
            result = subprocess.run(
                ["python3", temp_path], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            os.remove(temp_path)
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            if os.path.exists(temp_path): os.remove(temp_path)
            return False, str(e)

if __name__ == "__main__":
    refactor = RecursiveRefactor()
    code = refactor.build_and_validate("Escreva um script que liste todos os arquivos em 'macityos' e conte as linhas de cada um.")
    print(f"💎 Código Final:\n{code}")
