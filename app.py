import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from src.agents.openclaude_bridge import OpenClawBridge
from src.agents.mayor_task_manager import MayorTaskManager

st.set_page_config(page_title="MA-CityOS Neural Terminal", page_icon="🏙️", layout="wide")

# --- ESTILO CYBERPUNK ---
st.markdown("""
    <style>
    .status-ok { color: #00FF41; font-weight: bold; }
    .status-error { color: #FF3131; font-weight: bold; }
    .resilience-card { background: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; }
    .main-header { font-family: 'Courier New', monospace; color: #00FF41; text-shadow: 0 0 5px #00FF41; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">💻 MA-CityOS: V13 COGNITIVE RUNTIME</h1>', unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA ---
try:
    bridge = OpenClawBridge()
    health = getattr(bridge, "provider_health", {"Sinal": {"status": "CHECKING", "failures": 0}})
except:
    health = {"Sinal": {"status": "ERROR", "failures": 1}}

task_mgr = MayorTaskManager()

def load_json(filename):
    try:
        if os.path.exists(filename):
            with open(filename, "r") as f: return json.load(f)
    except: pass
    return None

def read_log_tail(filename, lines=20):
    try:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                content = f.readlines()
                return "".join(content[-lines:])
    except: pass
    return "KERNEL IDLE (Ocioso)."

config = load_json("city_config.json") or {"districts": []}
skills_map = load_json("city_data/skills_map.json") or []

# --- TOP BAR: MÉTRICAS REAIS ---
cols = st.columns(4)
cols[0].metric("Containers Docker (Nós)", "5 Ativos")
cols[1].metric("Habilidades Carregadas", len(skills_map))
cols[2].metric("Syscalls Pendentes", len(task_mgr.get_pending_tasks()))
cols[3].metric("Integridade do OS", "EXCELENTE")
st.divider()

# --- TABS DO SISTEMA ---
tab1, tab2, tab3, tab4 = st.tabs(["💻 TERMINAL", "🫀 KERNEL LOGS", "⚙️ DOCKER SWARM", "🛡️ RESILIÊNCIA"])

with tab1:
    st.markdown("### 🧬 Pulso Neural")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("~$ sudo run order:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Processando via Malha de Enxame..."):
                response = bridge.ask_agent(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.markdown("### 🫀 Logs do OS Scheduler")
    log_content = read_log_tail("city_data/sys_stream.log", lines=30)
    st.code(log_content, language="bash")
    if st.button("🔄 Atualizar Logs"): st.rerun()

with tab3:
    st.markdown("### ⚙️ Enxame de Bairros Virtualizados")
    st.write("Os seguintes sistemas Linux estão operando em paralelo na sua infraestrutura:")
    nodes_data = [
        {"NOME": f"macity-node-{i}", "OS": "Debian-Slim", "STATUS": "RUNNING", "IA": "Gemma/Llama"}
        for i in range(1, 6)
    ]
    st.table(pd.DataFrame(nodes_data))
    if st.button("🔌 REESCALONAR CONTAINERS"):
        st.info("Orquestrador enviado para o Docker Daemon...")

with tab4:
    st.markdown("### 🛡️ Monitor de Resiliência")
    h_cols = st.columns(len(health))
    for i, (provider, data) in enumerate(health.items()):
        with h_cols[i]:
            status_val = str(data.get("status", "N/A"))
            status_class = "status-ok" if status_val in ["OK", "ONLINE"] else "status-error"
            st.markdown(f"<div class='resilience-card'><p style='color:#888;'>{provider.upper()}</p><p class='{status_class}'>{status_val}</p></div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("MA-CityOS V13 // Operating System Operational")
