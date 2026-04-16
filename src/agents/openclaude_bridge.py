import os
import httpx
import json

class OpenClawBridge:
    """Ponte de Integração MA-CityOS + OpenClaude (via OpenRouter)."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "anthropic/claude-3.5-sonnet" # Modelo de elite padrão
        
    def ask_agent(self, prompt, system_instruction="Você é o Agente de Elite OpenClaude, integrado ao MA-CityOS."):
        """Envia uma tarefa para o cérebro OpenClaude via OpenRouter."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://macityos.mesh", # Opcional para OpenRouter
            "X-Title": "MA-CityOS Global Mesh",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = httpx.post(self.base_url, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"❌ Erro na ponte OpenClaude: {e}"

if __name__ == "__main__":
    bridge = OpenClawBridge()
    print("🧠 Testando ponte OpenClaude...")
    res = bridge.ask_agent("Analise o estado atual da malha digital do MA-CityOS.")
    print(f"🤖 OpenClaude Responde: {res[:200]}...")
