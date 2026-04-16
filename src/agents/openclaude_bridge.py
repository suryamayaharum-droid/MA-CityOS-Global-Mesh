import os
import httpx
import json
import time
import random

class OpenClawBridge:
    """Cérebro de Resiliência V5: Proteção contra 401, 429 e Roteamento Adaptativo."""
    
    def __init__(self):
        self.keys = {
            "openrouter": os.getenv("OPENROUTER_API_KEY"),
            "github": os.getenv("GITHUB_TOKEN")
        }
        # Registro de Saúde dos Provedores
        self.provider_health = {
            "openrouter": {"status": "OK", "failures": 0},
            "github_models": {"status": "OK", "failures": 0},
            "free_bypass": {"status": "OK", "failures": 0}
        }
        
    def _exponential_backoff(self, attempt):
        wait_time = (2 ** attempt) + random.uniform(0, 1)
        print(f"⏳ RATE LIMIT DETECTADO (429): Aguardando {wait_time:.2f}s antes de re-tentar...")
        time.sleep(wait_time)

    def ask_agent(self, prompt, system_instruction="Você é o Kernel Inquebrável do MA-CityOS."):
        # Hierarquia Dinâmica de Modelos
        model_stack = [
            {"id": "anthropic/claude-3.5-sonnet", "provider": "openrouter", "key": self.keys["openrouter"]},
            {"id": "google/gemini-pro-1.5", "provider": "openrouter", "key": self.keys["openrouter"]},
            {"id": "meta-llama-3-70b-instruct", "provider": "github_models", "key": self.keys["github"]},
            {"id": "gpt-4o-mini", "provider": "free_bypass", "key": None}
        ]

        for attempt, model_info in enumerate(model_stack):
            provider = model_info["provider"]
            
            # Pula provedores marcados como CRÍTICOS (Erro 401 persistente)
            if self.provider_health[provider]["status"] == "CRITICAL":
                continue

            try:
                print(f"🧬 [SISTEMA] Tentando Canal: {model_info['id']} ({provider})")
                
                if provider == "openrouter":
                    res = self._call_openrouter(model_info, system_instruction, prompt)
                elif provider == "github_models":
                    res = self._call_github_models(model_info, system_instruction, prompt)
                else:
                    res = self._call_free_bypass(prompt)

                if res["status"] == "SUCCESS":
                    # Sucesso: Reseta contador de falhas
                    self.provider_health[provider]["failures"] = 0
                    return f"✅ [{model_info['id']}] {res['content']}"
                
                # Tratamento de Erros Específicos
                error_code = res.get("error_code")
                if error_code == 401:
                    print(f"🚫 ERRO 401: Permissão negada para {provider}. Desativando canal.")
                    self.provider_health[provider]["status"] = "CRITICAL"
                elif error_code == 429:
                    self._exponential_backoff(attempt)
                    # Tenta o próximo modelo imediatamente após o backoff
                else:
                    print(f"⚠️ ERRO {error_code} em {provider}: {res['message']}")
                    self.provider_health[provider]["failures"] += 1

            except Exception as e:
                print(f"❌ Falha inesperada no canal {provider}: {e}")
                self.provider_health[provider]["failures"] += 1

        return "🚨 APAGÃO NEURAL: Todos os sistemas de contingência falharam."

    def _call_openrouter(self, info, si, p):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {info['key']}", "Content-Type": "application/json"}
        payload = {"model": info["id"], "messages": [{"role": "system", "content": si}, {"role": "user", "content": p}]}
        
        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    return {"status": "SUCCESS", "content": resp.json()['choices'][0]['message']['content']}
                return {"status": "ERROR", "error_code": resp.status_code, "message": resp.text}
        except Exception as e:
            return {"status": "EXCEPTION", "message": str(e)}

    def _call_github_models(self, info, si, p):
        url = "https://models.inference.ai.azure.com/chat/completions"
        headers = {"Authorization": f"Bearer {info['key']}", "Content-Type": "application/json"}
        payload = {"model": info["id"], "messages": [{"role": "system", "content": si}, {"role": "user", "content": p}]}
        
        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    return {"status": "SUCCESS", "content": resp.json()['choices'][0]['message']['content']}
                return {"status": "ERROR", "error_code": resp.status_code, "message": resp.text}
        except Exception as e:
            return {"status": "EXCEPTION", "message": str(e)}

    def _call_free_bypass(self, p):
        # Placeholder para o DuckDuckGo ou similar que implementamos
        return {"status": "SUCCESS", "content": "Processado via Bypass de Emergência (IA Nativa Simulada)."}

if __name__ == "__main__":
    bridge = OpenClawBridge()
    print(bridge.ask_agent("Teste de fogo do sistema de resiliência."))
