#!/bin/bash
# 🏙️ MA-CityOS: STARTUP SCRIPT V10
# Este script liga o Coração da Cidade e o Dashboard simultaneamente.

echo "🌌 MA-CityOS: Inicializando a Malha..."

# 1. Cria arquivos de log se não existirem
mkdir -p city_data
touch city_data/sys_stream.log
touch city_data/task_queue.json

# 2. Liga o Coração da Cidade (Heartbeat) em Background
echo "🫀 Ligando o Pulso Autônomo (Background)..."
export PYTHONPATH=$PYTHONPATH:.
python3 src/core/heartbeat.py &
HEARTBEAT_PID=$!

# 3. Liga o Servidor P2P em Background
echo "🌐 Abrindo portas da Malha P2P..."
python3 src/core/p2p_network.py &
P2P_PID=$!

# 4. Liga o Dashboard (Foreground)
echo "💻 Iniciando Neural Terminal..."
streamlit run app.py

# Se o Streamlit for fechado, mata os processos em background
kill $HEARTBEAT_PID
kill $P2P_PID
echo "🛑 MA-CityOS Desativado."
