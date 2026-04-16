#!/bin/bash
# 🏙️ MA-CityOS: STARTUP SCRIPT V12 (GUARDIAN DAEMON)
# Inicialização do Sistema Operacional Invulnerável

echo "🌌 MA-CityOS: Despertando Kernel V12..."

# 1. Configuração do Ambiente
mkdir -p city_data
touch city_data/sys_stream.log
touch city_data/guardian.log
export PYTHONPATH=$PYTHONPATH:.

# 2. Transição de Poder para o Guardian Daemon
echo "🛡️ Transferindo controle para o Guardian Daemon..."
echo "⚠️ O sistema se tornará auto-sustentável. Para desligar, use Ctrl+C."

# O Guardian inicia e monitora:
# - Heartbeat (O escalonador autônomo)
# - P2P Network (A comunicação de bairro)
# - Streamlit (A interface do usuário)
python3 guardian_daemon.py
