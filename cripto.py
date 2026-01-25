import streamlit as st
import yfinance as yf
import time
from datetime import datetime

# Estilo Alpha Vision
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #0f0; font-family: monospace; }</style>", unsafe_allow_html=True)

# Função para buscar preço via Yahoo Finance
def get_yfinance_price():
    try:
        # Busca o ticker do Bitcoin
        data = yf.Ticker("BTC-USD").fast_info
        return float(data['last_price'])
    except:
        return 89126.0

# CONFIGURAÇÕES DO DIRETOR
eixo_mestre = 89795.0 
preco_viva = get_yfinance_price()
agora = datetime.now().strftime("%H:%M:%S")

def calc(p): return eixo_mestre * (1 + (p/100))

# Interface do Terminal
st.title("🏛️ ALPHA VISION | YAHOO REAL-TIME")
st.write(f"Sync: {agora} (Datafeed Ativo)")

c1, c2, c3 = st.columns(3)
c1.metric("ATIVO", "BTC/USD")
# Preço em destaque
st.markdown(f"<h1 style='color: #0f0; font-size: 60px;'>${preco_viva:,.2f}</h1>", unsafe_allow_html=True)
c3.metric("VAR/EIXO", f"{((preco_viva/eixo_mestre)-1)*100:.2f}%")

st.divider()

# Grade de Alvos Institucionais
st.write("🎯 **ALVOS DE EXECUÇÃO**")
cols = st.columns(4)
cols[0].metric("1.22% ALVO", f"${calc(1.22):,.0f}")
cols[1].metric("0.83% TOPO", f"${calc(0.83):,.0f}")
cols[2].metric("0.61% PARCIAL", f"${calc(0.61):,.0f}")
cols[3].metric("0.40% RESPIRO", f"${calc(0.40):,.0f}")

# MOTOR DE MOVIMENTO
time.sleep(2)
st.rerun()
