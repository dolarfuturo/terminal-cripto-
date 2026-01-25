import streamlit as st
import requests
import time

# Configuração de Estilo Terminal
st.set_page_config(page_title="ALPHA LINE", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FF00; font-family: 'Courier New', monospace; }
    .stMetric { border: 1px solid #222; padding: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PREÇO AO VIVO ---
def get_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        return float(requests.get(url).json()['price'])
    except:
        return 89126.0 # Fallback caso a API falhe

# --- PARÂMETROS ---
eixo = 89795.0 
atual = get_price()
def c(p): return eixo * (1 + (p/100))

# --- TERMINAL EM LINHA ---
st.write("### 🟢 ALPHA VISION LIVE FEED")

# Primeira Linha: Dados do Ativo
col_main = st.columns([1, 1, 1, 1])
col_main[0].metric("CÓDIGO", "BTC/USDT")
col_main[1].metric("PREÇO ATUAL", f"${atual:,.2f}")
col_main[2].metric("EIXO MESTRE", f"${eixo:,.2f}")
col_main[3].metric("VAR %", f"{((atual/eixo)-1)*100:.2f}%")

st.divider()

# Segunda Linha: Alvos de ALTA (Horizontal)
st.write("⬆️ **ZONA DE ALTA (ALVOS)**")
cols_up = st.columns(4)
cols_up[0].metric("0.40% (R)", f"{c(0.4):,.2f}")
cols_up[1].metric("0.61% (P)", f"{c(0.61):,.2f}")
cols_up[2].metric("0.83% (T)", f"{c(0.83):,.2f}")
cols_up[3].metric("1.22% (GO)", f"{c(1.22):,.2f}")

st.divider()

# Terceira Linha: Alvos de BAIXA (Horizontal)
st.write("⬇️ **ZONA DE BAIXA (ALVOS)**")
cols_down = st.columns(4)
cols_down[0].metric("-0.40% (R)", f"{c(-0.4):,.2f}")
cols_down[1].metric("-0.61% (P)", f"{c(-0.61):,.2f}")
cols_down[2].metric("-0.83% (T)", f"{c(-0.83):,.2f}")
cols_down[3].metric("-1.22% (GO)", f"{c(-1.22):,.2f}")

# Refresh automático para o preço flutuar
time.sleep(5)
st.rerun()
