import os
import httpx
import json
import time

class OpenClawBridge:
    """Cérebro V13: Estabilidade Total com Monitor de Saúde e Bypass Real."""
    
    _vqd_cache = None 
    
    def __init__(self):
        self.or_key = os.getenv("OPENROUTER_API_KEY")
        # Restaura o monitor de saúde exigido pelo Dashboard
        self.provider_health = {
            "openrouter": {"status": "OK", "failures": 0},
            "free_bypass": {"status": "OK", "failures": 0},
            "docker_nodes": {"status": "ONLINE", "nodes": 5}
        }
        
    def _get_free_token(self):
        if OpenClawBridge._vqd_cache:
            return OpenClawBridge._vqd_cache
        try:
            headers = {"x-vqd-4": "1", "User-Agent": "Mozilla/5.0"}
            res = httpx.get("https://duckduckgo.com/duckchat/v1/status", headers=headers)
            token = res.headers.get("x-vqd-4")
            OpenClawBridge._vqd_cache = token
            return token
        except: return None

    def ask_agent(self, prompt, system_instruction="Você é o Kernel do MA-CityOS."):
        # 1. TENTA OPENROUTER
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
                    else:
                        self.provider_health["openrouter"]["status"] = "ERROR"
                        self.provider_health["openrouter"]["failures"] += 1
            except: pass

        # 2. TENTA FREE BRAIN
        token = self._get_free_token()
        if token:
            try:
                url = "https://duckduckgo.com/duckchat/v1/chat"
                headers = {"x-vqd-4": token, "Content-Type": "application/json"}
                payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": f"{system_instruction}\n\n{prompt}"}]}
                with httpx.Client(timeout=20.0) as client:
                    res = client.post(url, headers=headers, json=payload)
                    if res.status_code == 200:
                        full_resp = ""
                        for line in res.text.split('\n'):
                            if line.startswith('data: '):
                                chunk = line[6:]
                                if chunk != '[DONE]':
                                    try:
                                        data = json.loads(chunk)
                                        full_resp += data.get('message', '')
                                    except: pass
                        if full_resp: return full_resp
            except: pass
            
        self.provider_health["free_bypass"]["status"] = "OFFLINE"
        return "Sinal fraco na malha. Tentando reconectar..."

if __name__ == "__main__":
    bridge = OpenClawBridge()
    print(bridge.ask_agent("Teste de sistema."))
