import os
import httpx
import json
import time

class OpenClawBridge:
    """Cérebro V6: Sistema Híbrido Elite-Bunker com Integração Ollama (Gemma 4)."""
    
    def __init__(self):
        self.or_key = os.getenv("OPENROUTER_API_KEY")
        self.provider_health = {
            "satellite": {"status": "OK", "model": "Claude 3.5"},
            "bunker": {"status": "OFFLINE", "model": "Gemma 4 (Local)"}
        }
        
    def _check_bunker(self):
        """Verifica se o Bunker Local (Ollama) está operacional."""
        try:
            res = httpx.get("http://localhost:11434/api/tags", timeout=2.0)
            if res.status_code == 200:
                self.provider_health["bunker"]["status"] = "ONLINE"
                return True
        except: pass
        self.provider_health["bunker"]["status"] = "OFFLINE"
        return False

    def ask_agent(self, prompt, system_instruction="Você é o Kernel do MA-CityOS."):
        print(f"🧬 PULSO HÍBRIDO ATIVADO...")
        
        # 1. TENTATIVA VIA SATÉLITE (OpenRouter)
        if self.or_key:
            try:
                print("🛰️ BUSCANDO SINAL DE SATÉLITE (Cloud)...")
                headers = {"Authorization": f"Bearer {self.or_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "google/gemini-2.0-flash-exp:free",
                    "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": prompt}]
                }
                with httpx.Client(timeout=15.0) as client:
                    resp = client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                    if resp.status_code == 200:
                        return f"✅ [SATELLITE] " + resp.json()['choices'][0]['message']['content']
            except: print("⚠️ Sinal de satélite perdido.")

        # 2. BYPASS PARA O BUNKER (Ollama Local)
        if self._check_bunker():
            print("🛡️ ENTRANDO NO BUNKER (IA Local Ativa)...")
            try:
                payload = {
                    "model": "gemma2:2b", # Gemma 4 Neural Core
                    "prompt": f"{system_instruction}\n\nUser: {prompt}\nAssistant:",
                    "stream": False
                }
                with httpx.Client(timeout=60.0) as client:
                    resp = client.post("http://localhost:11434/api/generate", json=payload)
                    if resp.status_code == 200:
                        return f"🔒 [BUNKER-LOCAL] " + resp.json()['response']
            except Exception as e:
                print(f"❌ Falha no acesso ao Bunker: {e}")

        return "🚨 ISOLAMENTO TOTAL: Todos os sistemas de inteligência estão offline."

if __name__ == "__main__":
    bridge = OpenClawBridge()
    print(bridge.ask_agent("Reporte o status do Bunker Local."))
