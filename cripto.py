import streamlit as st
import requests
import time

# Estilo Bloomberg
st.set_page_config(page_title="ALPHA TERMINAL", layout="wide")
st.markdown("""<style>.main { background-color: #000; color: #0f0; font-family: monospace; }</style>""", unsafe_allow_html=True)

# Pegar preço real da Binance
def get_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        return float(requests.get(url).json()['price'])
    except: return 89070.0

# Seu Eixo da Foto 2
eixo = 89795.0 
preco = get_price()
def calc(p): return eixo * (1 + (p/100))

# Visual em Linha
st.title("🏛️ ALPHA VISION LIVE")
c1, c2, c3 = st.columns(3)
c1.metric("ATIVO", "BTC/USDT")
c2.metric("PREÇO ATUAL", f"${preco:,.2f}")
c3.metric("VAR/EIXO", f"{((preco/eixo)-1)*100:.2f}%")

st.divider()
st.write("🎯 **ALVOS EM LINHA**")
# Exibindo os alvos que você marcou no gráfico
cols = st.columns(4)
cols[0].metric("1.22% (ALVO)", f"${calc(1.22):,.2f}")
cols[1].metric("0.83% (TOPO)", f"${calc(0.83):,.2f}")
cols[2].metric("0.61% (PARCIAL)", f"${calc(0.61):,.2f}")
cols[3].metric("0.40% (RESPIRO)", f"${calc(0.40):,.2f}")

time.sleep(5)
st.rerun()
