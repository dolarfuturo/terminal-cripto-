import streamlit as st
import requests
import time

# Configuração Estilo Bloomberg
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #0f0; font-family: monospace; }</style>", unsafe_allow_html=True)

# Puxa preço real da Binance
def get_live_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        res = requests.get(url, timeout=3)
        return float(res.json()['price'])
    except:
        return 89126.0 # Preço da sua imagem 2 caso a rede falhe

# SEU EIXO TRAVADO (Imagem 2)
eixo_mestre = 89795.0 
preco_atual = get_live_price()
def calc(p): return eixo_mestre * (1 + (p/100))

# Painel Superior
st.title("🏛️ ALPHA VISION | TERMINAL")
c1, c2, c3 = st.columns(3)
c1.metric("ATIVO", "BTC/USDT")
c2.metric("PREÇO ATUAL", f"${preco_atual:,.2f}")
c3.metric("VAR/EIXO", f"{((preco_atual/eixo_mestre)-1)*100:.2f}%")

st.divider()

# Grade de Alvos Institucionais (Sua Régua)
st.write("🎯 **GRADE DE ALVOS**")
cols = st.columns(4)
cols[0].metric("1.22% ALVO", f"${calc(1.22):,.0f}")
cols[1].metric("0.83% TOPO", f"${calc(0.83):,.0f}")
cols[2].metric("0.61% PARCIAL", f"${calc(0.61):,.0f}")
cols[3].metric("0.40% RESPIRO", f"${calc(0.40):,.0f}")

# COMANDO DE MOVIMENTO (Faz o preço pular na tela)
time.sleep(3)
st.rerun()
