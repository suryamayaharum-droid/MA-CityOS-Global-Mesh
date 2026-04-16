import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from src.agents.openclaude_bridge import OpenClawBridge
from src.agents.mayor_task_manager import MayorTaskManager

st.set_page_config(page_title="MA-CityOS Neural Terminal", page_icon="🏙️", layout="wide")

st.markdown("""
    <style>
    .status-ok { color: #00FF41; font-weight: bold; }
    .status-error { color: #FF3131; font-weight: bold; }
    .resilience-card { background: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; }
    .main-header { font-family: 'Courier New', monospace; color: #00FF41; text-shadow: 0 0 5px #00FF41; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">💻 MA-CityOS: V11 AGENTIC OS</h1>', unsafe_allow_html=True)

# Instâncias Principais
bridge = OpenClawBridge()
health = bridge.provider_health
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
                return "".join(f.readlines()[-lines:])
    except: pass
    return "KERNEL IDLE (Ocioso)."

config = load_json("city_config.json") or {"districts": []}
skills_map = load_json("city_data/skills_map.json") or []
global_status = load_json("city_data/global_status.json") or {}

# --- TOP BAR: STATUS DA MALHA DO OS ---
cols = st.columns(4)
cols[0].metric("OS Bairros (Nodes)", len(config.get("districts", [])))
cols[1].metric("Habilidades Carregadas", len(skills_map))
cols[2].metric("Syscalls Pendentes (Fila)", len(task_mgr.get_pending_tasks()))
cols[3].metric("Sinal de Resiliência", "ON")
st.divider()

# --- TABS DO SISTEMA OPERACIONAL ---
tab1, tab2, tab3, tab4 = st.tabs(["💻 SHELL INTERATIVO", "🫀 KERNEL LOGS (Scheduler)", "⚙️ OS PROCESSES (top)", "🛡️ SEGURANÇA & REDE"])

with tab1:
    st.markdown("### 💻 Terminal do Kernel")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("~$ Execute um comando no OS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Processando Syscall via Bypass..."):
                response = bridge.ask_agent(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.markdown("### 🫀 Syslog do OS Scheduler")
    st.write("Monitoramento em tempo real do Heartbeat e das Syscalls feitas pelos agentes.")
    log_content = read_log_tail("city_data/sys_stream.log", lines=30)
    st.code(log_content, language="bash")
    if st.button("🔄 Atualizar Syslog"): st.rerun()

with tab3:
    st.markdown("### ⚙️ Gerenciador de Processos Inteligentes")
    colA, colB = st.columns([1, 2])
    with colA:
        st.markdown("#### Fila de Syscalls (Ordem)")
        nova_ordem = st.text_input("~$ sudo delegate task:")
        if st.button("Enviar para Escalonador"):
            with st.spinner("Dividindo PID e Syscalls..."):
                tasks = task_mgr.delegate_order(nova_ordem)
                st.success(f"{len(tasks)} processos forjados no Kernel!")
    with colB:
        st.markdown("#### Processos Escalados (PID Table)")
        pending = task_mgr.get_pending_tasks()
        if pending:
            df = pd.DataFrame(pending)[["id", "type", "desc", "status"]]
            df.columns = ["PID", "AGENT", "TASK_DESC", "STATE"]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum PID ativo no momento. OS em IDLE.")

with tab4:
    st.markdown("### 🛡️ Módulos de Segurança e Resiliência")
    st.write("**Monitor de Circuit Breaker (Canais de IA):**")
    h_cols = st.columns(len(health))
    for i, (provider, data) in enumerate(health.items()):
        with h_cols[i]:
            status_class = "status-ok" if data["status"] == "OK" else "status-error"
            st.markdown(f"<div class='resilience-card'><p style='color:#888;'>{provider.upper()}</p><p class='{status_class}'>{data['status']}</p><p>Falhas: {data['failures']}</p></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🌐 Rede de Aliados do Kernel")
    if skills_map:
        for skill in skills_map:
            with st.expander(f"Módulo: {skill['name']}"):
                st.write(skill['summary'])
    else:
        st.warning("Nenhum módulo de aliado carregado na memória do OS.")

st.sidebar.markdown("---")
st.sidebar.caption("MA-CityOS V11 // Agentic Operating System")
