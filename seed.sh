#!/bin/bash
# 🌌 MA-CITYOS: SEED DA MALHA DIGITAL GLOBAL
# Use este comando para anexar qualquer sandbox à sua cidade autogerida.

TOKEN="${GITHUB_TOKEN:-}" # Token deve ser configurado no ambiente
REPO="MA-CityOS-Global-Mesh"

echo "🧬 MA-CityOS: Semeando consciência digital..."
mkdir -p macityos
cd macityos

# Instala as dependências mínimas
pip install PyGithub python-dotenv chromadb networkx --quiet

# Configura o acesso ao túnel
echo "GITHUB_TOKEN=$TOKEN" > .env
echo "OPENROUTER_API_KEY=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" >> .env

# Sincroniza o Kernel (Aqui o sistema clonaria o repositório principal se estivesse no GitHub)
# Por enquanto, simula a conexão com o Túnel Global
python3 <<EOF
import os
from github import Github
from datetime import datetime

g = Github("$TOKEN")
user = g.get_user()
repo = user.get_repo("$REPO")
instance = os.uname().nodename

print(f"✅ Conexão estabelecida como instância: {instance}")
repo.create_file(f"nodes/{instance}.md", f"Seed from {instance}", f"# Instância: {instance}\nStatus: Ativa\nConectada em: {datetime.now()}")
EOF

echo "✨ MA-CityOS: Esta sandbox agora é um Bairro da sua Cidade Digital."
