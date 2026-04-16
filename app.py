import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="MA-CityOS Terminal", page_icon="💻", layout="wide", initial_sidebar_state="expanded")

# --- CSS CUSTOMIZADO (Cyberpunk Feel) ---
st.markdown("""
    <style>
    .stMetric {
        background-color: #1A1A1A;
        border-left: 3px solid #00FF41;
        padding: 10px;
        border-radius: 5px;
    }
    .main-header {
        font-family: 'Courier New', Courier, monospace;
        color: #00FF41;
        text-shadow: 0 0 5px #00FF41;
    }
    .radar-card {
        background: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">💻 MA-CityOS: NEURAL TERMINAL V2</h1>', unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS ---
def load_json(filename):
    try:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
    except: pass
    return None

config = load_json("city_config.json") or {"districts": [], "version": "2.0.0"}
global_status = load_json("city_data/global_status.json") or {}
news_feed = load_json("city_data/news_feed.json") or []
radar_data = load_json("city_data/global_radar.json") or []

# --- BARRA LATERAL (Cyber Shield & Status) ---
with st.sidebar:
    st.markdown('<h2 style="color:#00FF41;">🛡️ CYBER SHIELD</h2>', unsafe_allow_html=True)
    alerts = global_status.get("security_alerts", [])
    if alerts:
        st.error(f"⚠️ {len(alerts)} BRECHAS DETECTADAS")
        with st.expander("Ver Relatório de Intrusão"):
            for a in alerts[:5]:
                st.code(f"Repo: {a['repo']}\nAlvo: {a['file']}", language="bash")
    else:
        st.success("✅ INTEGRIDADE DO SISTEMA: 100%")
        
    st.divider()
    st.markdown('### ⚙️ SISTEMA AUTÔNOMO')
    if st.button("🔌 FORÇAR SINCRONIZAÇÃO NEURAL", use_container_width=True):
        st.rerun()
    st.caption(f"Último Pulso: {global_status.get('last_scan', 'Desconhecido')}")

# --- PAINEL DE COMANDO ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Nós (Bairros)", len(config.get("districts", [])))
col2.metric("Aliados Locais", len(global_status.get("allied_projects", [])))
col3.metric("Tecnologias no Radar", len(radar_data))
col4.metric("Status da Memória", "OTIMIZADA", delta="+20% Eficiência")

st.divider()

# --- TABS DE OPERAÇÃO ---
tab1, tab2, tab3 = st.tabs(["🔭 RADAR DE INOVAÇÃO (Global)", "🤝 REDE DE ALIADOS (Local)", "🌍 PULSO MUNDIAL"])

with tab1:
    st.markdown("### Tecnologias Complementares Descobertas no GitHub")
    if radar_data:
        cols = st.columns(3)
        for i, tech in enumerate(radar_data):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="radar-card">
                    <h4 style="color:#00FF41; margin-bottom:5px;">{tech['name']}</h4>
                    <p style="font-size: 0.9em; color:#AAA;">⭐ {tech['stars']} Stars</p>
                    <p style="font-size: 0.8em; height: 60px; overflow: hidden;">{tech['desc'][:100]}...</p>
                    <a href="{tech['url']}" target="_blank" style="color:#00FF41; text-decoration:none; border:1px solid #00FF41; padding:2px 8px; border-radius:3px;">Explorar Repositório</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Varredura do Radar Global em andamento... Aguarde o próximo ciclo do Swarm.")

with tab2:
    st.markdown("### Seus Projetos Integrados à Malha")
    allies = global_status.get("allied_projects", [])
    if allies:
        df_allies = pd.DataFrame(allies)
        st.dataframe(df_allies[['name', 'desc']], use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum aliado processado ainda.")

with tab3:
    st.markdown("### Fluxo de Dados: Inteligência Artificial")
    for item in news_feed:
        with st.container():
            st.markdown(f"**[{item['title']}]({item['link']})**")
            st.caption(f"Capturado em: {item['pubDate']}")
            st.divider()

st.markdown("---")
st.caption("MA-CityOS Neural Mesh // Operando em modo de processamento distribuído.")
