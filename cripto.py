import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP E CONFIGURAÇÃO
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

COINS_CONFIG = {
    "BTC-USD": {"label": "BTC/USDT", "dec": 0}, "ETH-USD": {"label": "ETH/USDT", "dec": 0},
    "SOL-USD": {"label": "SOL/USDT", "dec": 2}, "BNB-USD": {"label": "BNB/USDT", "dec": 2},
    "XRP-USD": {"label": "XRP/USDT", "dec": 4}, "DOGE-USD": {"label": "DOGE/USDT", "dec": 4},
    "ADA-USD": {"label": "ADA/USDT", "dec": 4}, "AVAX-USD": {"label": "AVAX/USDT", "dec": 2},
    "DOT-USD": {"label": "DOT/USDT", "dec": 2}, "LINK-USD": {"label": "LINK/USDT", "dec": 2}
}

def get_calculation_date():
    br_tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(br_tz)
    if now.weekday() == 5: return now - timedelta(days=1)
    if now.weekday() == 6: return now - timedelta(days=2)
    return now - timedelta(days=3) if (now.weekday() == 0 and now.hour < 18) else (now - timedelta(days=1) if now.hour < 18 else now)

def get_alpha_midpoint(ticker):
    try:
        target = get_calculation_date()
        df = yf.download(ticker, start=target.strftime('%Y-%m-%d'), end=(target + timedelta(days=1)).strftime('%Y-%m-%d'), interval="1m", progress=False)
        if df.empty: return yf.Ticker(ticker).fast_info['last_price']
        df_w = df.between_time('11:30', '18:00')
        return (float(df_w['High'].max()) + float(df_w['Low'].min())) / 2 if not df_w.empty else yf.Ticker(ticker).fast_info['last_price']
    except: return 0

# 2. CSS DE TRAVAMENTO ABSOLUTO (FIXED)
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    header, [data-testid="stHeader"] { display: none; }
    
    /* BLOCO FIXO QUE NÃO SAI DA TELA */
    .fixed-header {
        position: fixed;
        top: 0; left: 0; width: 100%;
        background: #000;
        z-index: 999999;
        border-bottom: 2px solid #D4AF37;
    }
    
    .top-bar { display: flex; justify-content: space-between; padding: 5px 30px; background: #050505; color: #FFF; font-family: monospace; font-size: 12px; }
    .title-gold { color: #D4AF37; font-size: 52px; font-weight: 900; text-align: center; line-height: 1; margin: 10px 0; }
    .subtitle-white { color: #FFF; font-size: 22px; text-align: center; letter-spacing: 8px; text-transform: lowercase; margin-bottom: 10px; }
    
    .header-grid { 
        display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; 
        padding: 12px 0; background: #080808; border-top: 1px solid #222;
    }
    .h-col { font-size: 10px; color: #FFF; text-align: center; font-weight: bold; }
    
    /* ESPAÇADOR PARA O CONTEÚDO ROLAR POR BAIXO */
    .spacer { margin-top: 230px; }

    .row-container { display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; align-items: center; padding: 15px 0; }
    .w-col { text-align: center; font-family: monospace; font-size: 19px; font-weight: 800; color: #FFF; }
    .vision-block { display: flex; justify-content: center; gap: 50px; padding-bottom: 15px; border-bottom: 2px solid #333; }
    .dot { height: 8px; width: 8px; background: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAR ESTADOS
for t in COINS_CONFIG:
    if f'rv_{t}' not in st.session_state:
        val = get_alpha_midpoint(t)
        st.session_state[f'rv_{t}'] = st.session_state[f'mp_{t}'] = val

placeholder = st.empty()

while True:
    try:
        now = datetime.now(pytz.timezone('America/Sao_Paulo'))
        with placeholder.container():
            st.markdown(f"""
                <div class="fixed-header">
                    <div class="top-bar">
                        <div><span class="dot"></span> LIVESTREAM</div>
                        <div>SÃO PAULO: {now.strftime('%H:%M:%S')}</div>
                    </div>
                    <div class="title-gold">ALPHA VISION CRYPTO</div>
                    <div class="subtitle-white">visão de tubarão</div>
                    <div class="header-grid">
                        <div class="h-col">CÓDIGO</div><div class="h-col">PREÇO</div>
                        <div class="h-col" style="color:#F44;">EXAUSTÃO T.</div><div class="h-col">TOPO</div>
                        <div class="h-col" style="color:#FF0;">DECISÃO</div><div class="h-col">RESPIRO</div>
                        <div class="h-col">FUNDO</div><div class="h-col" style="color:#0F0;">EXAUSTÃO F.</div>
                    </div>
                </div>
                <div class="spacer"></div>
            """, unsafe_allow_html=True)

            for t, info in COINS_CONFIG.items():
                price = yf.Ticker(t).fast_info['last_price']
                mp, rv = st.session_state[f'mp_{t}'], st.session_state[f'rv_{t}']
                g_ex, g_mov, g_dec, g_res = (1.35, 1.0122, 1.0061, 1.0040) if "BTC" in t or "ETH" in t else (13.5, 1.122, 1.061, 1.040)
                
                var_escada = ((price / mp) - 1) * 100
                if var_escada >= g_ex
