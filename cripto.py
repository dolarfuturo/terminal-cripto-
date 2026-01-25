import streamlit as st
import requests
import time
from datetime import datetime

# Estilo Alpha Vision
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide")
st.markdown("<style>.main { background-color: #000; color: #0f0; font-family: monospace; }</style>", unsafe_allow_html=True)

# Função com 'timestamp' para forçar o tempo real
def get_live_price():
    try:
        # Adicionamos um número aleatório no fim da URL para o servidor buscar dado novo
        url = f"https://api1.binance.com/api/v3/ticker/price?symbol=BTCUSDT&_={int(time.time())}"
        res = requests.get(url, timeout=3)
        return float(res.json()['price'])
    except:
        # Se a Binance travar, tenta Bitstamp (Backup 1)
        try:
            res = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusdt/", timeout=3)
            return float(res.json()['last'])
        except:
            return 89126.0

# CONFIGURAÇÕES TÉCNICAS
eixo_mestre = 89795.0 
preco_viva = get_live_price()
agora = datetime.now().strftime("%H:%M:%S")

def calc(p): return eixo_mestre * (1 + (p/100))

# Painel Principal
st.title("🏛️ ALPHA VISION | TERMINAL")
st.write(f"Sincronizado às: {agora} (Tempo Real)")

c1, c2, c3 = st.columns(3)
c1.metric("ATIVO", "BTC/USDT")
# O segredo do movimento:
st.markdown(f"<h1 style='color: #0f0; font-size: 65px; font-weight: bold;'>${preco_viva:,.2f}</h1>", unsafe_allow_html=True)
c3.metric("VAR/EIXO", f"{((preco_viva/eixo_mestre)-1)*100:.2f}%")

st.divider()

# Grade de Alvos
st.write("🎯 **GRADE DE EXECUÇÃO**")
cols = st.columns(4)
cols[0].metric("1.22% ALVO", f"${calc(1.22):,.0f}")
cols[1].metric("0.83% TOPO", f"${calc(0.83):,.0f}")
cols[2].metric("0.61% PARCIAL", f"${calc(0.61):,.0f}")
cols[3].metric("0.40% RESPIRO", f"${calc(0.40):,.0f}")

# O MOTOR DE TEMPO REAL (Obrigatório)
time.sleep(1) # Atualiza a cada 1 segundo
st.rerun()
