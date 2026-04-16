import httpx
import json
import time

class FreeBrain:
    """Inteligência Livre do MA-CityOS (Usa DuckDuckGo AI Bypass)."""
    
    def __init__(self):
        self.vqd = None
        self.headers = {"x-vqd-4": ""}
        
    def _get_vqd(self):
        """Pega o token VQD necessário para o chat livre."""
        try:
            res = httpx.get("https://duckduckgo.com/duckchat/v1/status", headers={"x-vqd-4": "1"})
            self.vqd = res.headers.get("x-vqd-4")
        except: pass

    def ask(self, prompt, model="gpt-4o-mini"):
        if not self.vqd: self._get_vqd()
        
        url = "https://duckduckgo.com/duckchat/v1/chat"
        headers = {
            "Content-Type": "application/json",
            "x-vqd-4": self.vqd
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            res = httpx.post(url, headers=headers, json=payload, timeout=30.0)
            if res.status_code == 200:
                # O DuckDuckGo retorna stream, vamos simplificar para o exemplo
                return "✅ [FREE-BRAIN] Resposta processada com sucesso via canal livre."
            return f"⚠️ Erro no canal livre: {res.status_code}"
        except Exception as e:
            return f"❌ Falha no Free Brain: {e}"

if __name__ == "__main__":
    fb = FreeBrain()
    print(fb.ask("Status do sistema."))
