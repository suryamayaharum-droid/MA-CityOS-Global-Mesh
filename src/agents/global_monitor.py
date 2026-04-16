import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from github import Github, Auth
import re
from datetime import datetime

class GlobalMonitor:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        auth = Auth.Token(self.token) if self.token else None
        self.github = Github(auth=auth) if auth else None
        self.data_dir = "city_data"
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "Allies"), exist_ok=True)

    def fetch_real_world_news(self):
        """Busca notícias reais via RSS do Google News para alimentar a cidade."""
        print("🌍 GLOBAL MONITOR: Buscando notícias do mundo real...")
        news = []
        try:
            url = "https://news.google.com/rss/search?q=tecnologia+inteligencia+artificial&hl=pt-BR&gl=BR&ceid=BR:pt-419"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                for item in root.findall('./channel/item')[:5]: # Pega as 5 principais
                    news.append({
                        "title": item.find('title').text,
                        "link": item.find('link').text,
                        "pubDate": item.find('pubDate').text
                    })
        except Exception as e:
            print(f"⚠️ Erro ao buscar notícias: {e}")
        
        with open(f"{self.data_dir}/news_feed.json", "w") as f:
            json.dump(news, f, indent=4)
        return news

    def run_security_scan_and_import(self):
        """Varre os repositórios da conta em busca de vazamentos e projetos aliados."""
        if not self.github:
            print("⚠️ GLOBAL MONITOR: GITHUB_TOKEN não encontrado. Varredura abortada.")
            return

        print("🛡️ CYBERSHIELD: Iniciando varredura global na conta do GitHub...")
        user = self.github.get_user()
        alerts = []
        allies = []
        
        # Padrões suspeitos em nomes de arquivos (varredura rápida via árvore Git)
        suspicious_files = re.compile(r'(\.env|secret|token|key|credentials)\b', re.IGNORECASE)
        
        try:
            for repo in user.get_repos():
                print(f"🔍 Analisando: {repo.name}...")
                
                # 1. Busca Projetos Complementares
                if repo.name != "MA-CityOS-Global-Mesh":
                    desc = repo.description or ""
                    topics = repo.get_topics()
                    # Se tiver IA, Agent ou Python, consideramos um aliado potencial
                    if any(kw in desc.lower() for kw in ['ai', 'agent', 'bot', 'os']) or 'python' in repo.language or topics:
                        allies.append({"name": repo.name, "url": repo.html_url, "desc": desc})
                        # Clona como aliado (usando git clone superficial e silencioso com auth)
                        ally_path = os.path.join(self.data_dir, "Allies", repo.name)
                        if not os.path.exists(ally_path):
                            print(f"🤝 Aliado encontrado! Importando {repo.name}...")
                            clone_url_auth = f"https://{self.token}@github.com/{repo.full_name}.git"
                            os.system(f"git clone --depth 1 {clone_url_auth} {ally_path} > /dev/null 2>&1")

                # 2. Varredura de Segurança (Olhando a árvore de arquivos)
                try:
                    tree = repo.get_git_tree(repo.default_branch, recursive=True)
                    for item in tree.tree:
                        if suspicious_files.search(item.path):
                            alerts.append({
                                "repo": repo.name,
                                "file": item.path,
                                "risk": "CRÍTICO - Possível vazamento de credencial",
                                "url": f"{repo.html_url}/blob/{repo.default_branch}/{item.path}"
                            })
                except Exception:
                    pass # Repositório pode estar vazio
        except Exception as e:
            print(f"⚠️ Erro na varredura: {e}")

        # Salva o relatório de segurança e aliados
        report = {
            "last_scan": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "security_alerts": alerts,
            "allied_projects": allies
        }
        with open(f"{self.data_dir}/global_status.json", "w") as f:
            json.dump(report, f, indent=4)
            
        print(f"✅ Varredura concluída. {len(alerts)} alertas encontrados. {len(allies)} projetos aliados conectados.")
        return report

if __name__ == "__main__":
    monitor = GlobalMonitor()
    monitor.fetch_real_world_news()
    monitor.run_security_scan_and_import()
