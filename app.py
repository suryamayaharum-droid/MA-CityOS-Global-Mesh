import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="MA-CityOS Global Dashboard", page_icon="🏙️", layout="wide")

st.title("🏙️ MA-CityOS: Malha Digital Global")

# Funções de carregamento de dados
def load_json(filename):
    try:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
    except: pass
    return None

config = load_json("city_config.json") or {"districts": [], "version": "1.0.0"}
global_status = load_json("city_data/global_status.json")
news_feed = load_json("city_data/news_feed.json")

# Barra Lateral
st.sidebar.header("🛡️ Cyber Shield Status")
if global_status:
    alerts = global_status.get("security_alerts", [])
    if alerts:
        st.sidebar.error(f"⚠️ {len(alerts)} Alertas de Segurança!")
        with st.sidebar.expander("Ver Alertas"):
            for alert in alerts[:5]:
                st.write(f"**Repo:** {alert['repo']}")
                st.write(f"**Arquivo:** {alert['file']}")
                st.write("---")
    else:
        st.sidebar.success("✅ Nenhuma ameaça detectada.")
    
    st.sidebar.divider()
    allies = global_status.get("allied_projects", [])
    st.sidebar.info(f"🤝 {len(allies)} Projetos Aliados Conectados.")

# Painel Principal
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Bairros Ativos", len(config.get("districts", [])))
with col2:
    st.metric("Aliados Importados", len(global_status.get("allied_projects", [])) if global_status else 0)
with col3:
    st.metric("Última Varredura", global_status.get("last_scan", "N/A") if global_status else "N/A")

st.divider()

# Notícias do Mundo Real
if news_feed:
    st.subheader("🌍 Feed do Mundo Real (Manchetes de IA)")
    cols = st.columns(len(news_feed))
    for i, item in enumerate(news_feed):
        with cols[i]:
            st.caption(item['pubDate'])
            st.write(f"**{item['title'][:50]}...**")
            st.link_button("Ler Mais", item['link'])

st.divider()

# Projetos Aliados (Importados via Swarm)
if global_status and global_status.get("allied_projects"):
    st.subheader("🤝 Rede de Projetos Aliados (Swarm Connectivity)")
    df_allies = pd.DataFrame(global_status["allied_projects"])
    st.dataframe(df_allies, use_container_width=True)

st.divider()

# Logs e Atividade
st.subheader("🐝 Atividade do Swarm")
tab1, tab2 = st.tabs(["Logs do Sistema", "Configurações da Cidade"])
with tab1:
    if os.path.exists("expansion.log"):
        with open("expansion.log", "r") as f:
            st.text(f.read()[-2000:])
with tab2:
    st.json(config)

if st.button("🔄 Sincronizar Agora"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("MA-CityOS V1.0 - Malha de Agentes Distribuída")
