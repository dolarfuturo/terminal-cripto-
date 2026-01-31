import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA VISION
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

# 2. CONFIGURAÇÃO (FATOR 1.115% E GATILHOS)
config_ativos = {
    "BTC-USD":  {"nome": "BTC/USDT", "gatilho": 1.35, "mov": 0.0122, "ex_t": 1.01115, "topo": 1.0083, "dec": 1.0061, "resp": 1.0040, "pf": 0.9939, "ex_f": 0.98885},
    "ETH-USD":  {"nome": "ETH/USDT", "gatilho": 1.35, "mov": 0.0122, "ex_t": 1.01115, "topo": 1.0083, "dec": 1.0061, "resp": 1.0040, "pf": 0.9939, "ex_f": 0.98885},
    "SOL-USD":  {"nome": "SOL/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1115, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8885},
    "BNB-USD":  {"nome": "BNB/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1115, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8885},
    "XRP-USD":  {"nome": "XRP/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1115, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8885},
    "DOGE-USD": {"nome": "DOGE/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1115, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8885}
}

# 3. FUNÇÃO MESTRE: MÉDIA (MAX+MIN)/2 DA SEXTA (11:30 - 18:00)
def get_midpoint_mestre(ticker):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(br_tz)
        
        # Como hoje é sábado, recuamos para sexta-feira
        if now.weekday() >= 5: # Sábado ou Domingo
            dias_atras = now.weekday() - 4
            target = now - timedelta(days=dias_atras)
        else:
            # Em dias de semana, se for antes das 18h, pega o dia anterior
            target = now if now.hour >= 18 else now - timedelta(days=1)

        df = yf.download(ticker, start=target.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not df.empty:
            df.index = df.index.tz_convert(br_tz)
            # Filtra rigorosamente entre 11:30 e 18:00
            df_window = df.between_time('11:30', '18:00')
            if not df_window.empty:
                mx = float(df_window['High'].max())
                mn = float(df_window['Low'].min())
                return (mx + mn) / 2 # A fórmula mestre
        return yf.Ticker(ticker).fast_info['last_price']
    except:
        return 0

# Inicializa o estado com o cálculo de sexta-feira
if 'data_ativos' not in st.session_state:
    st.session_state.data_ativos = {t: {"mp": get_midpoint_mestre(t), "rv": get_midpoint_mestre(t)} for t in config_ativos}

# (Interface e Estilos CSS seguem conforme os prints enviados...)
# ... [Omitido para brevidade, mas integrado no loop] ...

while True:
    try:
        with st.empty().container():
            for ticker, cfg in config_ativos.items():
                price = yf.Ticker(ticker).fast_info['last_price']
                mp = st.session_state.data_ativos[ticker]["mp"] # Âncora (Escada)
                rv = st.session_state.data_ativos[ticker]["rv"] # Reset (Fixo)

                # ESCADA ANCORAVISION
                var_mp = ((price / mp) - 1) * 100
                if var_mp >= cfg["gatilho"]: st.session_state.data_ativos[ticker]["mp"] *= (1 + cfg["mov"])
                elif var_mp <= -cfg["gatilho"]: st.session_state.data_ativos[ticker]["mp"] *= (1 - cfg["mov"])

                # VARIAÇÃO FIXA RESETVISION
                var_rv = ((price / rv) - 1) * 100
                
                # Exibição dos dados (Formatado conforme 1000028186.png)
                # ... Lógica de st.markdown aqui ...
        time.sleep(2)
    except:
        time.sleep(5)
