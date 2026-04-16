import os
import httpx
import json
import time

class OpenClawBridge:
    """Cérebro V7: Resiliência Total com Inteligência Livre Real (Independente de APIs Pagas)."""
    
    def __init__(self):
        self.or_key = os.getenv("OPENROUTER_API_KEY")
        self.vqd = None
        
    def _get_free_token(self):
        """Obtém o token VQD para o canal de inteligência livre (DuckChat)."""
        try:
            headers = {"x-vqd-4": "1"}
            res = httpx.get("https://duckduckgo.com/duckchat/v1/status", headers=headers)
            return res.headers.get("x-vqd-4")
        except: return None

    def ask_agent(self, prompt, system_instruction="Você é o Kernel do MA-CityOS."):
        print(f"🧬 PULSO DE RESILIÊNCIA ATIVADO...")
        
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
                        return f"✅ [ELITE-CLOUD] " + resp.json()['choices'][0]['message']['content']
            except: pass

        # 2. TENTATIVA: FREE BRAIN (Bypass Real e Gratuito)
        print("🛡️ ACIONANDO BYPASS DE EMERGÊNCIA (IA Livre)...")
        try:
            if not self.vqd: self.vqd = self._get_free_token()
            url = "https://duckduckgo.com/duckchat/v1/chat"
            headers = {"x-vqd-4": self.vqd, "Content-Type": "application/json"}
            # Usando gpt-4o-mini via canal livre
            payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": f"{system_instruction}\n\n{prompt}"}]}
            
            with httpx.Client(timeout=15.0) as client:
                res = client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    # O DuckChat retorna texto puro com prefixo 'data: ', vamos limpar
                    lines = res.text.split('\n')
                    full_resp = ""
                    for line in lines:
                        if line.startswith('data: '):
                            chunk = line[6:]
                            if chunk != '[DONE]':
                                try:
                                    data = json.loads(chunk)
                                    full_resp += data.get('message', '')
                                except: pass
                    if full_resp:
                        return f"🔓 [FREE-BYPASS] {full_resp}"
        except Exception as e:
            print(f"❌ Falha no canal livre: {e}")

        return "🚨 ISOLAMENTO NEURAL: Tentando reconectar à malha global..."

if __name__ == "__main__":
    bridge = OpenClawBridge()
    print(bridge.ask_agent("Olá, quem é você?"))
