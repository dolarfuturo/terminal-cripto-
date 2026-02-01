import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - VISUAL TOTALMENTE REPLICADO
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .block-container { padding-top: 1rem; }
    
    .title-container { text-align: center; padding: 10px; }
    .title-gold { color: #D4AF37; font-size: 32px; font-weight: 900; letter-spacing: 2px; }
    .subtitle-white { color: #FFFFFF; font-size: 15px; font-weight: 300; letter-spacing: 5px; text-transform: lowercase; margin-top: -10px; }
    
    /* CABEÇALHO ÚNICO NO TOPO */
    .header-container { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    
    /* LINHA DE PREÇOS */
    .row-container { display: flex; width: 100%; align-items: center; padding: 20px 0 5px 0; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; white-space: nowrap; }
    
    /* PONTOS DE VISÃO CENTRALIZADOS (IGUAL À FOTO) */
    .vision-block { display: flex; justify-content: center; gap: 80px; padding: 10px 0 25px 0; border-bottom: 1px solid #151515; }
    .v-item { text-align: center; }
    .v-lab { color: #888; font-size: 9px; text-transform: uppercase; margin-bottom: 2px; }
    .v-val { color: #ffffff; font-size: 19px; font-weight: bold; font-family: 'monospace'; }
    
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 12px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 30px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO
def get_midpoint_v13(ticker, fallback):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download(ticker, start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not df.empty:
            df.index = df.index.tz_convert(br_tz)
            df_window = df.between_time('11:30', '18:00')
            if not df_window.empty:
                return int((float(df_window['High'].max()) + float(df_window['Low'].min())) / 2)
        return fallback
    except: return fallback

# BTC PRIMEIRO, ETH DEPOIS
CONFIG = {
    "BTC-USD": {"label": "BTC/USDT", "fallback": 82632},
    "ETH-USD": {"label": "ETH/USDT", "fallback": 2900}
}

st.markdown("""<div class="title-container"><div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div></div>""", unsafe_allow_html=True)

# Inicializa Estados
for t in CONFIG:
    if f'mp_{t}' not in st.session_state:
        val = get_midpoint_v13(t, CONFIG[t]['fallback'])
        st.session_state[f'mp_{t}'] = val
        st.session_state[f'rv_{t}'] = val

placeholder = st.empty()

while True:
    try:
        now_utc = datetime.now(pytz.utc)
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        
        # Reset 00:00 UTC
        if now_utc.hour == 0 and now_utc.minute == 0 and now_utc.second < 2:
            for t in CONFIG:
                novo = get_midpoint_v13(t, CONFIG[t]['fallback'])
                st.session_state[f'mp_{t}'] = novo
                st.session_state[f'rv_{t}'] = novo
            st.rerun()

        with placeholder.container():
            # Cabeçalho Único
            st.markdown("""<div class="header-container"><div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div><div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div><div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div><div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div></div>""", unsafe_allow_html=True)
            
            for ticker, info in CONFIG.items():
                price = yf.Ticker(ticker).fast_info['last_price']
                mp = st.session_state[f'mp_{ticker}']
                rv = st.session_state[f'rv_{ticker}']
                
                # Escada (ÂncoraVision)
                var_esc = ((price / mp) - 1) * 100
                if var_esc >= 1.35: st.session_state[f'mp_{ticker}'] = int(mp * 1.0122)
                elif var_esc <= -1.35: st
