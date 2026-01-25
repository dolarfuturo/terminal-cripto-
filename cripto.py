import streamlit as st
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import time

# Estilo Bloomberg
st.set_page_config(page_title="ALPHA TERMINAL TV", layout="wide")
st.markdown("""<style>.main { background-color: #000; color: #0f0; font-family: monospace; }</style>""", unsafe_allow_html=True)

# --- CONEXÃO TRADINGVIEW ---
@st.cache_resource
def login_tv():
    return TvDatafeed()

def get_tv_price():
    try:
        tv = login_tv()
        # Puxa o último candle de 1 minuto da Binance via TradingView
        data = tv.get_hist(symbol='BTCUSDT', exchange='BINANCE', interval=Interval.in_1_minute, n_bars=1)
        return float(data['close'].iloc[-1])
    except:
        return None

# --- PARÂMETROS ---
eixo = 89795.0 
preco_atual = get_tv_price()

if preco_atual is None:
    st.error("Conectando ao Feed do TradingView...")
    time.sleep(2)
    st.rerun()

# --- CÁLCULOS ---
def c(p): return eixo * (1 + (p/100))
var_pct = ((preco_atual / eixo) - 1) * 100

# --- INTERFACE ---
st.title("🏛️ ALPHA VISION | TV REAL-TIME")

# Linha Principal
c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
c1.metric("CÓDIGO", "BTCUSDT (TV)")
c2.metric("PREÇO ATUAL", f"${preco_atual:,.2f}")
c3.metric("EIXO MESTRE", f"${eixo:,.2f}")
c4.metric("VAR %", f"{var_pct:.2f}%")

st.divider()

# Grade de Alvos em Linha
st.write("🎯 **ALVOS INSTITUCIONAIS**")
ca, cb, cc, cd, ce, cf, cg, ch = st.columns(8)

# Alta
ca.metric("1.22%", f"{c(1.22):,.0f}")
cb.metric("0.83%", f"{c(0.83):,.0f}")
cc.metric("0.61%", f"{c(0.61):,.0f}")
cd.metric("0.40%", f"{c(0.4):,.0f}")
# Baixa
ce.metric("-0.40%", f"{c(-0.4):,.0f}")
cf.metric("-0.61%", f"{c(-0.61):,.0f}")
cg.metric("-0.83%", f"{c(-0.83):,.0f}")
ch.metric("-1.22%", f"{c(-1.22):,.0f}")

# Refresh para flutuação
time.sleep(5)
st.rerun()
