# 🏙️ MA-CityOS AI-DEVELOPMENT IMAGE
FROM python:3.10-slim

# 1. Instala ferramentas de sistema e desenvolvimento
RUN apt-get update && apt-get install -y \
    git curl build-essential libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Configura diretório de trabalho
WORKDIR /app

# 3. Instala Bibliotecas de Memória e IA Nativa (Pesadas)
RUN pip install --no-cache-dir \
    streamlit pandas httpx chromadb \
    transformers faiss-cpu langchain \
    pydantic python-dotenv networkx

# 4. Copia o Kernel e Scripts de Operação
COPY . .

# 5. Terminal Agêntico: Serviço para eu (IA) agir nativamente dentro do sistema
RUN echo "import os, sys; print('🧠 AGENT SHELL ONLINE')" > src/core/agent_internal_shell.py

# 6. Boot do Sistema com Guardian Daemon
ENV PYTHONPATH=/app
CMD ["python3", "guardian_daemon.py"]
