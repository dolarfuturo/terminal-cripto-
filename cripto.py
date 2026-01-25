import streamlit as st
import requests
import time

# Estilo Alpha Vision
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #0f0; font-family: monospace; }</style>", unsafe_allow_html=True)

def get_price():
    # Tenta 3 fontes diferentes para nunca ficar travado
    urls = [
        "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
        "https://api1.binance.com/api/v3/ticker/price?symbol=BTCUSDT",
        "https://www.bitstamp.net/api/v2/ticker/btcusdt/"
    ]
    for url in urls:
        try:
            res = requests.get(url, timeout=3).json()
            return float(res['price']) if 'price' in res else float(res['last'])
        except:
            continue
    return 89126.0

# CONFIGURAÇÕES DO DIRETOR
eixo_mestre = 89795.0 
preco_viva = get_price()
def calc(p): return eixo_mestre * (1 + (p/100))

# Painel Principal
st.title("🏛️ ALPHA VISION | TERMINAL")

c1, c2, c3 = st.columns(3)
c1.metric("ATIVO", "BTC/USDT")
# Mostra o preço em destaque
st.markdown(f"<h1 style='color: #0f0; font-size: 50px;'>${preco_viva:,.2f}</h1>", unsafe_allow_html=True)
c3.metric("VAR/EIXO", f"{((preco_viva/eixo_mestre)-1)*100:.2f}%")

st.divider()

# Grade de Alvos
st.write("🎯 **GRADE DE EXECUÇÃO**")
cols = st.columns(4)
cols[0].metric("1.22% ALVO", f"${calc(1.22):,.0f}")
cols[1].metric("0.83% TOPO", f"${calc(0.83):,.0f}")
cols[2].metric("0.61% PARCIAL", f"${calc(0.61):,.0f}")
cols[3].metric("0.40% RESPIRO", f"${calc(0.40):,.0f}")

# MOTOR DE ATUALIZAÇÃO
time.sleep(2)
st.rerun()
