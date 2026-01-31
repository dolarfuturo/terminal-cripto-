import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA
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

# 3. MOTOR DINÂMICO (JANELA 11:30 ÀS 18:00 BR)
def calcular_mestre_vision(ticker):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(br_tz)
        
        # Define o dia da análise (Se FDS, olha para Sexta-feira)
        if now.weekday() == 5: target_date = now - timedelta(days=1)
        elif now.weekday() == 6: target_date = now - timedelta(days=2)
        else: target_date = now if now.hour >= 18 else now - timedelta(days=1)

        # Baixa dados de 1 minuto para precisão total na janela
        df = yf.download(ticker, start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not df.empty:
            df.index = df.index.tz_convert(br_tz)
            # Janela mestre definida no seu código
            df_window = df.between_time('11:30', '18:00')
            if not df_window.empty:
                # FÓRMULA MESTRE: (MÁXIMA + MÍNIMA) / 2
                return (float(df_window['High'].max()) + float(df_window['Low'].min())) / 2
        
        return yf.Ticker(ticker).fast_info['last_price']
    except:
        return 0

# Inicialização com o cálculo mestre dinâmico
if 'data_ativos' not in st.session_state:
    st.session_state.data_ativos = {t: {"mp": calcular_mestre_vision(t), "rv": calcular_mestre_vision(t)} for t in config_ativos}

# ... (Interface Visual Alpha Vision) ...

while True:
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)

        # EXECUTA O CÁLCULO MESTRE ÀS 18:00 (SEG A SEX)
        if now_br.weekday() < 5 and now_br.hour == 18 and now_br.minute == 0 and now_br.second < 10:
            for t in config_ativos.keys():
                novo_mestre = calcular_mestre_vision(t)
                st.session_state.data_ativos[t] = {"mp": novo_mestre, "rv": novo_mestre}
            st.rerun()

        # Renderização e lógica de escada (AncoraVision) seguem aqui...
        # (Omitido para focar na sua correção de cálculo)
        time.sleep(2)
    except:
        time.sleep(5)
