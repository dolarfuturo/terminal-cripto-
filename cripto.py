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
    "DOT-USD": {"label": "DOT/USDT", "dec": 2}, "LINK-USD": {"label": "LINK/USDT", "dec": 2}
}

# CSS PARA TRAVAMENTO FIXO ABSOLUTO
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    header, [data-testid="stHeader"] { display: none; }
    
    /* TRAVA O CABEÇALHO NO TOPO DO VIEWPORT */
    .sticky-wrapper {
        position: fixed;
        top: 0; left: 0; width: 100%;
        z-index: 999999;
        background-color: #000;
        border-bottom: 2px solid #D4AF37;
    }
    
    .top-bar { display: flex; justify-content: space-between; padding: 5px 20px; background: #050505; color: #FFF; font-family: monospace; font-size: 12px; }
    .title-gold { color: #D4AF37; font-size: 52px; font-weight: 900; text-align: center; line-height: 1; margin: 10px 0; }
    .subtitle-white { color: #FFF; font-size: 20px; text-align: center; letter-spacing: 8px; text-transform: lowercase; margin-bottom: 10px; }
    
    .grid-layout { 
        display: grid; 
        grid-template-columns: 1.2fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; 
        width: 100%; text-align: center;
    }
    
    .h-col { font-size: 10px; color: #FFF; font-weight: 800; padding: 10px 0; background: #0A0A0A; }
    .w-col { font-family: monospace; font-size: 20px; font-weight: 800; color: #FFF; padding: 10px 0; }
    
    /* ESPAÇO PARA O CONTEÚDO NÃO FICAR EMBAIXO DO TRAVAMENTO */
    .spacer { margin-top: 240px; }

    .vision-block { display: flex; justify-content: center; gap: 50px; padding: 5px 0 15px 0; border-bottom: 2px solid #333; margin-bottom: 5px; }
    .dot { height: 8px; width: 8px; background: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

for t in COINS_CONFIG:
    if f'mp_{t}' not in st.session_state:
        st.session_state[f'rv_{t}'] = st.session_state[f'mp_{t}'] = yf.Ticker(t).fast_info['last_
