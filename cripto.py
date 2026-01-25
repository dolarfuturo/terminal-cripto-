import streamlit as st
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import time

# Estilo Bloomberg
st.set_page_config(page_title="ALPHA VISION | TV LIVE", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #0f0; font-family: monospace; }</style>", unsafe_allow_html=True)

# Conector TradingView
@st.cache_resource
def login_tv():
    return TvDatafeed()

def get_tv_price():
    try:
        tv = login_tv()
        # Puxa o último preço da Binance dentro do TradingView
        data = tv.get_hist(symbol='BTCUSDT', exchange='BINANCE', interval=Interval.in_1_minute, n_bars=1)
        return float(data['close'].iloc[-1])
    except Exception as e:
        return None

# SEU EIXO TRAVADO
eixo_mestre = 89795.0 
preco_atual = get_tv_price()

def calc(p): return eixo_mestre * (1 + (p/100))

st.title("🏛️ ALPHA VISION | TRADINGVIEW FEED")

if preco_atual:
    c1, c2, c3 = st.columns(3)
    c1.metric("ATIVO", "BTC/USDT (TV)")
    # Preço grande e verde
    st.markdown(f"<h1 style='color: #0f0; font-size: 60px;'>${preco_atual:,.2f}</h1>", unsafe_allow_html=True)
    c3.metric("VAR / EIXO", f"{((preco_atual/eixo_mestre)-1)*100:.2f}%")

    st.divider()

    # Alvos em Linha
    st.write("🎯 **GRADE DE ALVOS INSTITUCIONAIS**")
    ca, cb, cc, cd = st.columns(4)
    ca.metric("1.22% ALVO", f"${calc(1.22):,.0f}")
    cb.metric("0.83% TOPO", f"${calc(0.83):,.0f}")
    cc.metric("0.61% PARCIAL", f"${calc(0.61):,.0f}")
    cd.metric("0.40% RESPIRO", f"${calc(0.40):,.0f}")
else:
    st.warning("🔄 Conectando ao túnel do TradingView... Aguarde.")

# Motor de movimento (5 segundos para não ser bloqueado)
time.sleep(5)
st.rerun()
