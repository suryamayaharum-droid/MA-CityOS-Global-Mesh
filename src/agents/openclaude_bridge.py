import os
import httpx
import json

class OpenClawBridge:
    """Ponte de Independência MA-CityOS via GitHub Models (Gratuito e Nativo)."""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://models.inference.ai.azure.com" # Endpoint do GitHub Models
        
    def ask_agent(self, prompt, system_instruction="Você é o Cérebro Inquebrável do MA-CityOS."):
        print(f"🧬 PULSO GITHUB MODELS ATIVADO (Bypass Total)...")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Modelo Gratuito do GitHub (Llama 3 ou Mistral)
        payload = {
            "model": "meta-llama-3-70b-instruct",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1024
        }
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
                
                if response.status_code == 200:
                    res_json = response.json()
                    return f"✅ [GITHUB-MODELS] " + res_json['choices'][0]['message']['content']
                else:
                    return f"⚠️ Github Models Indisponível (Erro {response.status_code})."
        except Exception as e:
            return f"❌ FALHA NO BYPASS GITHUB: {e}"

if __name__ == "__main__":
    bridge = OpenClawBridge()
    print(bridge.ask_agent("Reporte o status do sistema de resiliência."))
