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
        """Busca notícias reais via RSS."""
        print("🌍 GLOBAL MONITOR: Buscando pulso do mundo real...")
        news = []
        try:
            url = "https://news.google.com/rss/search?q=tecnologia+inteligencia+artificial+agentes&hl=pt-BR&gl=BR&ceid=BR:pt-419"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                for item in root.findall('./channel/item')[:5]:
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

    def search_global_github_network(self):
        """Busca tecnologias complementares em TODA A REDE do GitHub."""
        if not self.github:
            return []
            
        print("🔭 RADAR GLOBAL: Varrendo o GitHub mundial por inovações...")
        queries = [
            "topic:swarm-intelligence language:python",
            "topic:multi-agent-system language:python",
            "topic:agentic-os"
        ]
        
        global_radar = []
        try:
            for query in queries:
                # Pega os 3 repositórios mais estrelados para cada query
                repositories = self.github.search_repositories(query=query, sort="stars", order="desc")[:3]
                for repo in repositories:
                    if not any(r['name'] == repo.name for r in global_radar): # Evita duplicatas
                        global_radar.append({
                            "name": repo.full_name,
                            "stars": repo.stargazers_count,
                            "url": repo.html_url,
                            "desc": repo.description or "Sem descrição"
                        })
        except Exception as e:
            print(f"⚠️ Erro no Radar Global: {e}")
            
        # Salva o Radar de Inovação
        with open(f"{self.data_dir}/global_radar.json", "w") as f:
            json.dump(global_radar, f, indent=4)
            
        print(f"🎯 RADAR: {len(global_radar)} tecnologias de ponta mapeadas.")
        return global_radar

    def run_security_scan_and_import(self):
        """Varredura de segurança local e importação de aliados da conta."""
        if not self.github:
            return

        print("🛡️ CYBERSHIELD: Varredura de integridade na conta...")
        user = self.github.get_user()
        alerts = []
        allies = []
        suspicious_files = re.compile(r'(\.env|secret|token|key|credentials)\b', re.IGNORECASE)
        
        try:
            for repo in user.get_repos():
                if repo.name != "MA-CityOS-Global-Mesh":
                    desc = repo.description or ""
                    topics = repo.get_topics()
                    # Identifica Aliados Locais
                    if any(kw in desc.lower() for kw in ['ai', 'agent', 'bot']) or topics:
                        allies.append({"name": repo.name, "url": repo.html_url, "desc": desc})
                        
                # Scan de Segurança
                try:
                    tree = repo.get_git_tree(repo.default_branch, recursive=True)
                    for item in tree.tree:
                        if suspicious_files.search(item.path):
                            alerts.append({
                                "repo": repo.name,
                                "file": item.path,
                                "risk": "CRÍTICO"
                            })
                except: pass
        except Exception as e:
            print(f"⚠️ Erro na varredura: {e}")

        report = {
            "last_scan": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "security_alerts": alerts,
            "allied_projects": allies
        }
        with open(f"{self.data_dir}/global_status.json", "w") as f:
            json.dump(report, f, indent=4)
        return report

if __name__ == "__main__":
    monitor = GlobalMonitor()
    monitor.fetch_real_world_news()
    monitor.search_global_github_network()
    monitor.run_security_scan_and_import()
