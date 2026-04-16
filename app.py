import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from src.agents.openclaude_bridge import OpenClawBridge

st.set_page_config(page_title="MA-CityOS Neural Terminal", page_icon="🏙️", layout="wide")

# --- CSS CUSTOMIZADO (Cyberpunk Resilience Feel) ---
st.markdown("""
    <style>
    .status-ok { color: #00FF41; font-weight: bold; }
    .status-error { color: #FF3131; font-weight: bold; }
    .status-warn { color: #FFD700; font-weight: bold; }
    .resilience-card { background: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="color:#00FF41; font-family:monospace;">🧬 MA-CityOS: RESILIENCE TERMINAL V5</h1>', unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS ---
bridge = OpenClawBridge()
health = bridge.provider_health

# --- MONITOR DE SAÚDE DA MALHA (Top Bar) ---
cols = st.columns(len(health))
for i, (provider, data) in enumerate(health.items()):
    with cols[i]:
        status_class = "status-ok" if data["status"] == "OK" else "status-error"
        st.markdown(f"""
        <div class="resilience-card">
            <p style="margin:0; font-size:0.8em; color:#888;">Provedor: {provider.upper()}</p>
            <p class="{status_class}" style="margin:0; font-size:1.2em;">{data['status']}</p>
            <p style="margin:0; font-size:0.7em; color:#555;">Falhas: {data['failures']}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# --- ÁREA DE OPERAÇÃO ---
tab1, tab2, tab3 = st.tabs(["🤖 TERMINAL DE ELITE", "🛡️ LOGS DE RESILIÊNCIA", "⚙️ CONFIGURAÇÕES DE BYPASS"])

with tab1:
    st.markdown("### 🧬 Pulso Neural Multi-Canal")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Envie um comando para a malha..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Navegando pelos canais de resiliência..."):
                response = bridge.ask_agent(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.markdown("### 🛡️ Histórico de Auto-Cura")
    if os.path.exists("macity_vault/system_health.json"):
        with open("macity_vault/system_health.json", "r") as f:
            logs = [json.loads(line) for line in f.readlines()]
            df_logs = pd.DataFrame(logs)
            st.dataframe(df_logs, use_container_width=True)
    else:
        st.info("Nenhuma falha registrada ainda. Sistema operando em estabilidade nominal.")

with tab3:
    st.markdown("### ⚙️ Lógica de Bypass")
    st.write("O sistema alterna automaticamente entre canais baseados em:")
    st.code("""
    1. Erro 401 -> Bloqueio imediato do provedor (Bypass Crítico).
    2. Erro 429 -> Backoff Exponencial (2^n) + Troca de Canal.
    3. Timeout  -> Próximo modelo na pilha de elite.
    """, language="python")

if st.button("🔄 REINICIALIZAR SENSORES"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("MA-CityOS Resilience Mesh // V5.0.0")
