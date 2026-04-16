import os
import json

class ResilienceAgent:
    """O Agente de Resiliência: O Guardião da Malha que aprende com as falhas."""
    
    def __init__(self):
        self.health_log = "macity_vault/system_health.json"
        self.status = "OPERACIONAL"
        
    def log_failure(self, provider, error):
        """Registra a falha e propõe uma rota de fuga (Bypass)."""
        failure_data = {
            "timestamp": os.uname().nodename,
            "provider": provider,
            "error": str(error),
            "action": "Alternando para Bypass Nativo"
        }
        
        with open(self.health_log, "a") as f:
            f.write(json.dumps(failure_data) + "\n")
            
        print(f"🛡️ RESILIENCE: Falha detectada em {provider}. Rota de fuga ativada.")
        return "Bypass de Inteligência Ativado"

    def get_status(self):
        return self.status

if __name__ == "__main__":
    ra = ResilienceAgent()
    print(ra.log_failure("OpenRouter", "Erro 404 - No Endpoints"))
