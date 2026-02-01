import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

COINS_CONFIG = {
    "BTC-USD": {"label": "BTC/USDT", "dec": 0},
    "ETH-USD": {"label": "ETH/USDT", "dec": 0},
    "SOL-USD": {"label": "SOL/USDT", "dec": 2},
    "BNB-USD": {"label": "BNB/USDT", "dec": 2},
    "XRP-USD": {"label": "XRP/USDT", "dec": 4},
    "DOGE-USD": {"label": "DOGE/USDT", "dec": 4},
    "ADA-USD": {"label": "ADA/USDT", "dec": 4},
    "AVAX-USD": {"label": "AVAX/USDT", "dec": 2},
    "DOT-USD": {"label": "DOT/USDT", "dec": 2},
    "LINK-USD": {"label": "LINK/USDT", "dec": 2},
    "MATIC-USD": {"label": "POL/USDT", "dec": 4},
    "TRX-USD": {"label": "TRX/USDT", "dec": 4},
    "LTC-USD": {"label": "LTC/USDT", "dec": 2},
    "BCH-USD": {"label": "BCH/USDT", "dec": 2},
    "SHIB-USD": {"label": "SHIB/USDT", "dec": 6},
    "NEAR-USD": {"label": "NEAR/USDT", "dec": 3},
    "APT-USD": {"label": "APT/USDT", "dec": 2},
    "UNI-USD": {"label": "UNI/USDT", "dec": 2},
    "STX-USD": {"label": "STX/USDT", "dec": 3},
    "ARB-USD": {"label": "ARB/USDT", "dec": 4}
}

def get_calculation_date():
    br_tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(br_tz)
    if now.weekday() == 5: return now - timedelta(days=1)
    if now.weekday() == 6: return now - timedelta(days=2)
    if now.weekday() == 0 and now.hour < 18: return now - timedelta(days=3)
    if now.hour < 18: return now - timedelta(days=1)
    return now

def get_alpha_midpoint(ticker):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        target_date = get_calculation_date()
        start_fetch = target_date.strftime('%Y-%m-%d')
        end_fetch = (target_date + timedelta(days=1)).strftime('%Y-%m-%d')
        df = yf.download(ticker, start=start_fetch, end=end_fetch, interval="1m", progress=False)
        if df.empty: return yf.Ticker(ticker).fast_info['last_price']
        df.index = df.index.tz_convert(br_tz)
        df_window = df.between_time('11:30', '18:00')
        if not df_window.empty:
            return (float(df_window['High'].max()) + float(df_window['Low'].min())) / 2
        return yf.Ticker(ticker).fast_info['last_price']
    except: return 0

# CSS DEFINITIVO - TÍTULOS GIGANTES E TOPO TRAVADO
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    /* Forçar o cabeçalho a ficar fixo no topo da página */
    header, [data-testid="stHeader"] { display: none; }
    
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #000000;
        z-index: 9999;
        border-bottom: 2px solid #D4AF37;
        padding-top: 10px;
    }

    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 5px 40px; background: #050505; }
    .clocks { display: flex; gap: 35px; color: #888; font-family: monospace; font-size: 13px; }
    .clock-item b { color: #FFF; }
    .live-indicator { display: flex; align-items: center; gap: 10px; color: #FFF; font-size: 13px; font-weight: bold; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; animation: pulse 1.5s infinite; }
    @keyframes pulse { 0% { transform: scale(0.9); opacity: 1; box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.7); } 70% { transform: scale(1); opacity: 0.6; box-shadow: 0 0 0 10px rgba(0, 255, 0, 0); } 100% { transform: scale(0.9); opacity: 1; } }
    
    .title-gold { color: #D4AF37; font-size: 52px; font-weight: 900; text-align: center; margin-top: 10px; line-height: 1; text-transform: uppercase; }
    .subtitle-white { color: #FFFFFF; font-size: 22px; text-align: center; letter-spacing: 8px; text-transform: lowercase; margin-bottom: 15px; font-weight: 300; }
    
    .header-grid { display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; width: 100%; padding: 12px 0; background: #080808; border-top: 1px solid #1a1a1a; }
    .h-col { font-size: 11px; color: #FFF; text-align: center; font-weight: 800; }
    
    /* Espaçamento para o conteúdo não ficar escondido atrás do topo fixo */
    .content-spacer { margin-top: 220px; }

    .row-container { display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; width: 100%; align-items: center; padding: 15px 0 5px 0; }
    .w-col { text-align: center; font-family: 'monospace'; font-size: 19px; font-weight: 800; color: #FFF; }
    .vision-block { display: flex; justify-content: center; gap: 70px; padding: 5px 0 15px 0; border-bottom: 4px solid #333; margin-bottom: 5px; } /* DIVISOR FORTE */
    .v-item { text-align: center; }
    
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAR ESTADOS
for t in COINS_CONFIG:
    if f'rv_{t}' not in st.session_state:
        val = get_alpha_midpoint(t)
        st.session_state[f'rv_{t}'] = val
        st.session_state[f'mp_{t}'] = val

placeholder = st.empty()

while True:
    try:
        tz_br, tz_ny, tz_ld = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York'), pytz.timezone('Europe/London')
        now_br, now_ny, now_ld = datetime.now(tz_br), datetime.now(tz_ny), datetime.now(tz_ld)

        with placeholder.container():
            # CABEÇALHO FIXO
            st.markdown(f"""
                <div class="sticky-header">
                    <div class="top-bar">
                        <div class="live-indicator"><span class="dot"></span> LIVESTREAM</div>
                        <div class="clocks">
                            <div class="clock-item">BRASÍLIA: <b>{now_br.strftime('%H:%M:%S')}</b></div>
                            <div class="clock-item">NEW YORK: <b>{now_ny.strftime('%H:%M:%S')}</b></div>
                            <div class="clock-item">LONDON: <b>{now_ld.strftime('%H:%M:%S')}</b></div>
                        </div>
                    </div>
                    <div class="title-gold">ALPHA VISION CRYPTO</div>
                    <div class="subtitle-white">visão de tubarão</div>
                    
