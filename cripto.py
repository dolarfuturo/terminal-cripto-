import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP
st.set_page_config(page_title="ALPHA VISION MULTI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 15px 0; border-bottom: 1px solid #151515; }
    .h-col, .w-col { flex: 1; text-align: center; color: #FFF; font-family: 'monospace'; }
    .h-col { font-size: 10px; text-transform: uppercase; font-weight: 800; }
    .w-col { font-size: 18px; font-weight: 800; }
    .title-gold { color: #D4AF37; font-size: 28px; font-weight: 900; text-align: center; }
    .footer { position: fixed; bottom: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 10px; font-size: 12px; border-top: 1px solid #333; display: flex; justify-content: space-around; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

def get_midpoint(ticker):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download(ticker, start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not df.empty:
            df.index = df.index.tz_convert(br_tz)
            df_window = df.between_time('11:30', '18:00')
            if not df_window.empty:
                return int((df_window['High'].max() + df_window['Low'].min()) / 2)
        return 82632 if "BTC" in ticker else 2350
    except:
        return 82632 if "BTC" in ticker else 2350

# 2. INICIALIZAÇÃO DE ESTADO PARA MÚLTIPLOS ATIVOS
tickers = ["BTC-USD", "ETH-USD"]
if 'data' not in st.session_state:
    st.session_state.data = {}
    for t in tickers:
