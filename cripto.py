import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

COINS_CONFIG = {
    "BTC-USD": {"label": "BTC/USDT", "dec": 0}, "ETH-USD": {"label": "ETH/USDT", "dec": 0},
    "SOL-USD": {"label": "SOL/USDT", "dec": 2}, "BNB-USD": {"label": "BNB/USDT", "dec": 2},
    "XRP-USD": {"label": "XRP/USDT", "dec": 4}, "DOGE-USD": {"label": "DOGE/USDT", "dec": 4},
    "ADA-USD": {"label": "ADA/USDT", "dec": 4}, "AVAX-USD": {"label": "AVAX/USDT", "dec": 2},
    "DOT-USD": {"label": "DOT/USDT", "dec": 2}, "LINK-USD": {"label": "LINK/USDT", "dec": 2},
    "MATIC-USD": {"label": "POL/USDT", "dec": 4}, "TRX-USD": {"label": "TRX/USDT", "dec": 4}
}

# 2. CSS REVISADO: TRAVAMENTO E ALINHAMENTO
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }

    /* CABEÇALHO FIXO NO TOPO */
    .fixed-header {
        position: fixed;
        top: 0; left: 0; width: 100%;
        background: #000000;
        z-index: 999999;
        border-bottom: 2px solid #D4AF37;
    }

    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 5px 25px; background: #050505; border-bottom: 1px solid #1a1a1a; }
    .clocks { display: flex; gap: 30px; color: #888; font-family: monospace; font-size: 13px; }
    .title-gold { color: #D4AF37; font-size: 42px; font-weight: 900; text-align: center; margin: 10px 0; line-height: 1; }
    .subtitle-white { color: #FFF; font-size: 18px; text-align: center; letter-spacing: 6px; text-transform: lowercase; margin-bottom: 10px; }

    /* GRID UNIFICADA PARA CABEÇALHO E DADOS */
    .grid-layout {
        display: grid;
        grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr;
        width: 100%;
        text-align: center;
        background: #080808;
    }

    .h-col { font-size: 11px; color: #FFF; font-weight: 800; padding: 12px 0; border-top: 1px solid #1a1a1a; }
    .w-col { font-family: 'monospace'; font-size: 18px; font-weight: 800; color: #FFF; padding: 15px 0; }
    
    /* COMPENSAÇÃO DE ESPAÇO */
    .spacer { margin-top: 220px; }

    .vision-block { display: flex; justify-content: center; gap: 60px; padding: 5px 0 15px 0; border-bottom: 3px solid #333; margin-bottom: 5px; }
    .dot { height: 9px; width: 9px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

def get_alpha_midpoint(ticker):
    try:
        df = yf.download(ticker, period="2d", interval="1m", progress=False)
        return yf.Ticker(ticker).fast_info['last_price'] if df.empty else (float(df['High'].max()) + float(df['Low'].min())) / 2
    except: return 0

for t in COINS_CONFIG:
    if f'mp_{t}' not in st.session_state:
        val = get_alpha_midpoint(t)
        st.session_state[f'rv_{t}'] = st.session_state[f'mp_{t}'] = val

placeholder = st.empty()

while True:
    try:
        now = datetime.now(pytz.timezone('America/Sao_Paulo'))
        with placeholder.container():
            # BLOCO QUE FICA TRAVADO
            st.markdown(f"""
                <div class="fixed-header">
                    <div class="top-bar">
                        <div style="color:#FFF; font-weight:bold;"><span class="dot"></span> LIVESTREAM</div>
                        <div class="clocks">BR: <b>{now.strftime('%H:%M:%S')}</b></div>
                    </div>
                    <div class="title-gold">ALPHA VISION CRYPTO</div>
                    <div class="subtitle-white">visão de tubarão</div>
                    <div class="grid-layout">
                        <div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div>
                        <div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                        <div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div>
                        <div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div>
                    </div>
                </div>
                <div class="spacer"></div>
            """, unsafe_allow_html=True)

            # LISTAGEM QUE ROLA
            for t, info in COINS_CONFIG.items():
                price = yf.Ticker(t).fast_info['last_price']
                mp, rv = st.session_state[f'mp_{t}'],
