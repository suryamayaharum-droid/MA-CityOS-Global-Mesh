import os
import httpx
import json
import time

class OpenClawBridge:
    """Cérebro V8: Resiliência Total com Token Persistente e Bypass Inteligente."""
    
    _vqd_cache = None # Cache de classe para o token VQD
    
    def __init__(self):
        self.or_key = os.getenv("OPENROUTER_API_KEY")
        
    def _get_free_token(self):
        """Obtém o token VQD para o canal de inteligência livre de forma robusta."""
        if OpenClawBridge._vqd_cache:
            return OpenClawBridge._vqd_cache
            
        try:
            # O DuckDuckGo agora exige um User-Agent real
            headers = {"x-vqd-4": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            res = httpx.get("https://duckduckgo.com/duckchat/v1/status", headers=headers)
            token = res.headers.get("x-vqd-4")
            if token:
                OpenClawBridge._vqd_cache = token
                return token
        except Exception as e:
            print(f"⚠️ Erro ao capturar token de bypass: {e}")
        return None

    def ask_agent(self, prompt, system_instruction="Você é o Kernel do MA-CityOS."):
        # 1. TENTATIVA: OPENROUTER (Elite)
        if self.or_key and "sk-or" in self.or_key:
            try:
                headers = {"Authorization": f"Bearer {self.or_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "google/gemini-2.0-flash-exp:free",
                    "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": prompt}]
                }
                with httpx.Client(timeout=10.0) as client:
                    resp = client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                    if resp.status_code == 200:
                        return resp.json()['choices'][0]['message']['content']
            except: pass

        # 2. TENTATIVA: FREE BRAIN (Bypass Real)
        token = self._get_free_token()
        if token:
            try:
                url = "https://duckduckgo.com/duckchat/v1/chat"
                headers = {
                    "x-vqd-4": token, 
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }
                payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": f"{system_instruction}\n\n{prompt}"}]}
                
                with httpx.Client(timeout=20.0) as client:
                    res = client.post(url, headers=headers, json=payload)
                    if res.status_code == 200:
                        # Extrai a resposta do stream
                        full_resp = ""
                        for line in res.text.split('\n'):
                            if line.startswith('data: '):
                                chunk = line[6:]
                                if chunk != '[DONE]':
                                    try:
                                        data = json.loads(chunk)
                                        full_resp += data.get('message', '')
                                    except: pass
                        if full_resp:
                            return full_resp
            except: pass

        return f"Sincronização manual necessária para o aliado: {prompt[:50]}..."

if __name__ == "__main__":
    bridge = OpenClawBridge()
    print(bridge.ask_agent("Olá, teste de pulso."))
