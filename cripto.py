import streamlit as st
import requests
import time

# Configuração de Estilo
st.set_page_config(page_title="ALPHA TERMINAL", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #0f0; font-family: monospace; }</style>", unsafe_allow_html=True)

# Função para pegar o preço ao vivo da Binance
def get_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        res = requests.get(url, timeout=3)
        return float(res.json()['price'])
    except:
        return 89126.0

# Dados do seu Setup (Foto 2)
eixo = 89795.0 
preco_atual = get_price()
def calc(p): return eixo * (1 + (p/100))

# Título e Preço Vivo
st.title("🏛️ ALPHA VISION | TERMINAL LIVE")
c1, c2, c3 = st.columns(3)
c1.metric("ATIVO", "BTC/USDT")
c2.metric("PREÇO ATUAL", f"${preco_atual:,.2f}")
c3.metric("VAR / EIXO", f"{((preco_atual/eixo)-1)*100:.2f}%")

st.divider()

# Alvos em Linha
st.write("🎯 **GRADE DE ALVOS (BASEADO NO EIXO)**")
ca, cb, cc, cd = st.columns(4)
ca.metric("1.22% ALVO", f"${calc(1.22):,.0f}")
cb.metric("0.83% TOPO", f"${calc(0.83):,.0f}")
cc.metric("0.61% PARCIAL", f"${calc(0.61):,.0f}")
cd.metric("0.40% RESPIRO", f"${calc(0.40):,.0f}")

# Comando de movimento: atualiza a cada 3 segundos
time.sleep(3)
st.rerun()
