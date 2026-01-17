import streamlit as st
import ccxt
import pandas as pd

# Configuração de Página
st.set_page_config(page_title="Mister Tesouraria", layout="wide")

# CSS para visual Dark Profissional
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} .stApp {background-color: #0e1117; color: white;}</style>", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def buscar_dados():
    exchange = ccxt.binance()
    moedas = ["BTC", "ETH", "SOL", "BNB", "LINK"]
    res = []
    for s in moedas:
        try:
            bars = exchange.fetch_ohlcv(f"{s}/USDT", timeframe='1h', limit=100)
            df = pd.DataFrame(bars, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
            df['tp'] = (df['h'] + df['l'] + df['c']) / 3
            vwap = (df['tp'] * df['v']).sum() / df['v'].sum()
            atual = df['c'].iloc[-1]
            desvio = ((atual / vwap) - 1) * 100
            
            status, cor = "NORMAL", "#00FF00"
            if abs(desvio) >= 10: status, cor = "EXAUSTÃO", "#FF0000"
            elif abs(desvio) >= 8: status, cor = "STRESS", "#FF8C00"
            elif abs(desvio) >= 4: status, cor = "ATENÇÃO", "#FFFF00"
            
            res.append({"Ativo": s, "Preço": f"$ {atual:,.2f}", "Var": f"{desvio:+.2f}%", "Status": status, "cor": cor})
        except: continue
    return res

st.title("🏛️ Mister Tesouraria: Terminal Cripto")

if st.button('🔄 Atualizar Dados'):
    st.cache_data.clear()
    st.rerun()

dados = buscar_dados()
btc = dados[0]

# Destaque BTC
st.metric(label=f"ANCORA: {btc['Ativo']}", value=btc['Preço'], delta=btc['Var'])
st.markdown(f"<h2 style='color:{btc['cor']};'>STATUS: {btc['Status']}</h2>", unsafe_allow_html=True)

st.divider()

# Grid Altcoins
cols = st.columns(len(dados)-1)
for i, alt in enumerate(dados[1:]):
    with cols[i]:
        st.write(f"**{alt['Ativo']}**")
        st.markdown(f"<p style='color:{alt['cor']}; font-weight:bold;'>{alt['Status']}<br>{alt['Var']}</p>", unsafe_allow_html=True)
