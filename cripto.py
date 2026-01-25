import streamlit as st
import requests
import time

# Estética Bloomberg
st.set_page_config(page_title="ALPHA TERMINAL LIVE", layout="wide")
st.markdown("""<style>.main { background-color: #000; color: #0f0; font-family: monospace; }</style>""", unsafe_allow_html=True)

# --- FUNÇÃO DE DADOS EM TEMPO REAL ---
def get_binance_price():
    try:
        # Puxando direto da fonte oficial da Binance
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=2)
        return float(response.json()['price'])
    except:
        return None

# --- PARÂMETROS OPERACIONAIS ---
eixo = 89795.0 # Seu eixo travado conforme as imagens
preco_atual = get_binance_price()

# Se a API falhar, tenta novamente
if preco_atual is None:
    st.warning("Aguardando conexão com a Binance...")
    time.sleep(1)
    st.rerun()

# --- CÁLCULO DE ALVOS (Sua Régua) ---
def c(p): return eixo * (1 + (p/100))
var_pct = ((preco_atual / eixo) - 1) * 100

# --- TERMINAL EM LINHA ---
st.write(f"### 🖥️ TERMINAL ALPHA | BTC/USDT | {time.strftime('%H:%M:%S')}")

# CABEÇALHO EM LINHA
c1, c2, c3, c4 = st.columns([1.5, 2, 2, 1.5])
c1.metric("ATIVO", "BTC/USDT")
c2.metric("PREÇO ATUAL", f"${preco_atual:,.2f}", f"{preco_atual - 89070:.2f} diff") # Comparativo
c3.metric("EIXO MESTRE", f"${eixo:,.2f}")
c4.metric("VAR / EIXO", f"{var_pct:.2f}%")

st.divider()

# LINHA DE ALVOS (HORIZONTAL)
st.write("🎯 **GRADE DE ALVOS (PERCENTUAL SOBRE EIXO)**")
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

# --- LOOP DE MOVIMENTO ---
# Faz o script rodar de novo em 2 segundos para o preço flutuar
time.sleep(2)
st.rerun()
