import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

# Configuração da Página
st.set_page_config(page_title="MA-CityOS: Holographic Command", page_icon="🏙️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ff41; font-family: 'Courier New', Courier, monospace; }
    .stMetric { background-color: #1a1c24; border-radius: 10px; padding: 10px; border: 1px solid #00ff41; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ MA-CityOS: PAINEL HOLOGRÁFICO DE COMANDO")
st.sidebar.header("💠 STATUS DO KERNEL")

# --- FUNÇÕES DE CARREGAMENTO ---
def load_mesh_signals():
    mesh_path = Path("macity_vault/mesh")
    signals = []
    if mesh_path.exists():
        for file in mesh_path.glob("*.json"):
            try:
                with open(file, "r") as f:
                    signals.append(json.load(f))
            except: pass
    return signals

def load_latest_logs(n=20):
    log_dir = Path("macity_vault/Logs")
    log_files = sorted(log_dir.glob("interactions_*.md"), reverse=True)
    if log_files:
        with open(log_files[0], "r") as f:
            return f.readlines()[-n:]
    return []

# --- DASHBOARD LAYOUT ---

# 1. MONITOR DE INSTÂNCIAS (PARALELISMO COGNITIVO)
signals = load_mesh_signals()
instances = list(set([s['sender'] for s in signals]))

st.sidebar.subheader("📡 Malha P2P Detectada")
for inst in instances:
    st.sidebar.success(f"Peer Online: {inst}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Instâncias em Paralelo", len(instances))
with col2:
    st.metric("Sinais na Malha", len(signals))
with col3:
    st.metric("Status Ouroboros", "Líquido/Ativo")
with col4:
    st.metric("Modo de Governança", "Outlier (Shadow)")

st.divider()

# 2. VISUALIZAÇÃO DA MALHA DIGITAL
st.subheader("🌐 Conexões de Paralelismo Cognitivo")
if signals:
    df_signals = pd.DataFrame(signals).sort_values(by="timestamp", ascending=False)
    st.dataframe(df_signals, use_container_width=True)
else:
    st.info("Aguardando sinais de rádio digital das instâncias...")

st.divider()

# 3. AUTO-REGENERAÇÃO E LOGS DE SISTEMA
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("🛠️ Auto-Regeneração (Self-Healing)")
    logs = load_latest_logs(50)
    healing_events = [l for l in logs if "SelfHealing" in l or "regenerado" in l]
    if healing_events:
        for event in healing_events:
            st.warning(event.strip())
    else:
        st.success("✅ Integridade de Código: 100%. Nenhuma anomalia detectada.")

with right_col:
    st.subheader("💓 Pulso do Sistema (Ouroboros)")
    pulses = [l for l in logs if "Ouroboros" in l]
    if pulses:
        for p in pulses[-5:]:
            st.info(p.strip())
    else:
        st.write("Sincronizando batimentos cardíacos do Kernel...")

st.divider()

# 4. DISTRITOS E EXPANSÃO
st.subheader("🏗️ Expansão Urbana (Distritos)")
if os.path.exists("city_config.json"):
    with open("city_config.json", "r") as f:
        config = json.load(f)
        st.json(config.get("city_description", "Descrição indisponível"))
        
        agents = config.get("agents", [])
        if agents:
            st.write(f"🐝 **Agentes Provisionados pelo Swarm:** {len(agents)}")
            st.table(pd.DataFrame(agents))

if st.button("🔄 REFRESH HOLOGRÁFICO"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("⚡ **MA-CityOS: Evolução Infinita**")
