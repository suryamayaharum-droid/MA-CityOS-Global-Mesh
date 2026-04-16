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

st.markdown('<h1 class="main-header">🧬 MA-CityOS: V9 COGNITIVE SWARM</h1>', unsafe_allow_html=True)

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

config = load_json("city_config.json") or {"districts": []}
global_status = load_json("city_data/global_status.json") or {}
skills_map = load_json("city_data/skills_map.json") or []

# --- TOP BAR: STATUS DA MALHA ---
cols = st.columns(4)
cols[0].metric("Nós Ativos (Bairros)", len(config.get("districts", [])))
cols[1].metric("Habilidades Apreendidas", len(skills_map))
cols[2].metric("Tarefas Pendentes", len(task_mgr.get_pending_tasks()))
cols[3].metric("Conexões P2P", "0 (Ouvindo)")
st.divider()

# --- TABS DE OPERAÇÃO ---
tab1, tab2, tab3, tab4 = st.tabs(["🤖 TERMINAL ELITE", "📋 FILA DE TAREFAS", "🧠 CÉREBRO DA CIDADE", "⚙️ RESILIÊNCIA"])

with tab1:
    st.markdown("### 🧬 Pulso Neural")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Dê uma ordem para o Kernel..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Processando via Swarm Cognitivo..."):
                response = bridge.ask_agent(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.markdown("### 📋 Logística do Prefeito (Task Manager)")
    nova_ordem = st.text_input("Enviar Ordem Global para o Prefeito quebrar em tarefas:")
    if st.button("Delegar Ordem"):
        with st.spinner("Dividindo ordem..."):
            tasks = task_mgr.delegate_order(nova_ordem)
            st.success(f"{len(tasks)} micro-tarefas geradas!")
            
    st.markdown("#### Tarefas na Fila")
    pending = task_mgr.get_pending_tasks()
    if pending:
        st.table(pd.DataFrame(pending)[["id", "type", "desc", "status"]])
    else:
        st.info("Nenhuma tarefa pendente.")

with tab3:
    st.markdown("### 🧠 Habilidades Integradas (Aliados)")
    if skills_map:
        for skill in skills_map:
            with st.expander(f"Habilidade: {skill['name']}"):
                st.write(skill['summary'])
                st.caption(f"Memória ID: {skill['mem_id']}")
    else:
        st.warning("O Agente de Integração ainda não rodou. Nenhuma habilidade mapeada.")

with tab4:
    st.markdown("### 🛡️ Saúde dos Provedores (Auto-Cura)")
    h_cols = st.columns(len(health))
    for i, (provider, data) in enumerate(health.items()):
        with h_cols[i]:
            status_class = "status-ok" if data["status"] == "OK" else "status-error"
            st.markdown(f"<div class='resilience-card'><p style='color:#888;'>{provider.upper()}</p><p class='{status_class}'>{data['status']}</p><p>Falhas: {data['failures']}</p></div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("MA-CityOS V9 // Consciência Coletiva Ativa")
