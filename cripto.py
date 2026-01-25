import streamlit as st
import pandas as pd
import time
from datetime import datetime, timezone

# Configuração de Interface Estilo Bloomberg
st.set_page_config(page_title="TERMINAL ALPHA VISION", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FF00; font-family: 'Courier New', Courier, monospace; }
    .stMetric { background-color: #111111; border: 1px solid #333; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("🏛️ ALPHA VISION | INSTITUTIONAL TERMINAL")
st.write(f"Sessão: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# --- LÓGICA DE DADOS (Simulando API Real-Time) ---
# Aqui o sistema busca o preço ao vivo (Exemplo: $89.126 como no seu print)
preco_atual = 89126.0 
# Seu Eixo Travado (Pode ser automatizado via API pegando Max/Min 11:30-18:00)
eixo_mestre = 89795.0 

# Cálculo de Variação com base no Eixo
variacao_eixo = ((preco_atual / eixo_mestre) - 1) * 100

# --- CÁLCULO DOS ALVOS ---
def calc(p): return eixo_mestre * (1 + (p/100))

alvos_up = { "1.22%": calc(1.22), "0.83%": calc(0.83), "0.61%": calc(0.61), "0.40%": calc(0.4) }
alvos_down = { "-0.40%": calc(-0.4), "-0.61%": calc(-0.61), "-0.83%": calc(-0.83), "-1.22%": calc(-1.22) }

# --- PAINEL PRINCIPAL ---
col_stats1, col_stats2, col_stats3 = st.columns(3)

with col_stats1:
    st.metric("TICKER", "BTC/USDT")
with col_stats2:
    color = "inverse" if variacao_eixo < 0 else "normal"
    st.metric("PREÇO ATUAL", f"${preco_atual:,.2f}", f"{variacao_eixo:.2f}% vs Eixo", delta_color=color)
with col_stats3:
    st.metric("EIXO MESTRE (LOCK)", f"${eixo_mestre:,.2f}", "Reset 00:00 UTC")

st.divider()

# --- TABELA DE ALVOS BLOOMBERG STYLE ---
st.subheader("📊 GRADE DE EXECUÇÃO INSTITUCIONAL")

tabela_dados = {
    "NÍVEL (%)": ["1.22% (ALVO)", "0.83% (TOPO)", "0.61% (PARCIAL)", "0.40% (RESPIRO)", "0.00% (EIXO)", "-0.40%", "-0.61%", "-0.83%", "-1.22%"],
    "PREÇO": [
        f"${alvos_up['1.22%']:,.2f}", f"${alvos_up['0.83%']:,.2f}", f"${alvos_up['0.61%']:,.2f}", f"${alvos_up['0.40%']:,.2f}",
        f"${eixo_mestre:,.2f}",
        f"${alvos_down['-0.40%']:,.2f}", f"${alvos_down['-0.61%']:,.2f}", f"${alvos_down['-0.83%']:,.2f}", f"${alvos_down['-1.22%']:,.2f}"
    ],
    "STATUS": [
        "🎯 TARGET", "⚠️ EXAUSTÃO", "🛡️ PROTEÇÃO", "🔄 PULLBACK", "💎 BALANCE", "🔄 PULLBACK", "🛡️ PROTEÇÃO", "⚠️ EXAUSTÃO", "🎯 TARGET"
    ]
}

df_terminal = pd.DataFrame(tabela_dados)
st.table(df_terminal)

# --- AUTO REFRESH ---
time.sleep(2)
# st.rerun() # Descomente para rodar ao vivo
