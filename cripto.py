import streamlit as st
import requests
import time

# Configuração Estilo Bloomberg
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #0f0; font-family: monospace; }</style>", unsafe_allow_html=True)

# Puxa preço real usando Mirror (Mais estável que o padrão)
def get_live_price():
    try:
        # Usando api1 para evitar bloqueios de IP
        url = "https://api1.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        res = requests.get(url, timeout=5)
        return float(res.json()['price'])
    except:
        # Se falhar, ele tenta o endpoint secundário em vez de travar no preço fixo
        try:
            url = "https://api3.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            res = requests.get(url, timeout=5)
            return float(res.json()['price'])
        except:
            return None # Retorna None para sabermos que a rede falhou

# SEU EIXO TRAVADO
eixo_mestre = 89795.0 
preco_atual = get_live_price()

# Cálculo de Alvos
def calc(p): return eixo_mestre * (1 + (p/100))

# Painel Superior
st.title("🏛️ ALPHA VISION | TERMINAL")

if preco_atual:
    c1, c2, c3 = st.columns(3)
    c1.metric("ATIVO", "BTC/USDT")
    # Formatação com cor dinâmica
    st.markdown(f"<h1 style='color: #0f0; font-size: 60px;'>${preco_atual:,.2f}</h1>", unsafe_allow_html=True)
    c3.metric("VAR/EIXO", f"{((preco_atual/eixo_mestre)-1)*100:.2f}%")

    st.divider()

    # Grade de Alvos Institucionais (Sua Régua)
    st.write("🎯 **GRADE DE ALVOS**")
    cols = st.columns(4)
    cols[0].metric("1.22% ALVO", f"${calc(1.22):,.0f}")
    cols[1].metric("0.83% TOPO", f"${calc(0.83):,.0f}")
    cols[2].metric("0.61% PARCIAL", f"${calc(0.61):,.0f}")
    cols[3].metric("0.40% RESPIRO", f"${calc(0.40):,.0f}")
else:
    st.error("🔄 Tentando reconectar com a Binance... Verifique o sinal.")

# COMANDO DE MOVIMENTO
time.sleep(2)
st.rerun()
