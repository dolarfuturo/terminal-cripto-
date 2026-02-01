import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA VISION MOBILE FULL
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
    "LINK-USD": {"label": "LINK/USDT", "dec": 2}
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

# CSS MOBILE FULL RESPONSIVE
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    [data-testid="stVerticalBlock"] { padding-top: 140px !important; }

    .top-header-fixed {
        position: fixed; top: 0; left: 0; right: 0;
        height: 130px; background: #000; z-index: 9999;
        border-bottom: 2px solid #D4AF37; text-align: center;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }

    .title-gold { color: #D4AF37; font-size: 24px; font-weight: 900; letter-spacing: 2px; margin: 0; }
    .clock-mobile { color: #FFF; font-size: 14px; font-family: monospace; margin-top: 5px; }
    .live-tag { background: #FF0000; color: #FFF; font-size: 10px; padding: 2px 10px; border-radius: 4px; margin-top: 8px; animation: blink 1s infinite; font-weight: bold; }
    
    .mobile-card {
        background: #0A0A0A; border: 1px solid #1A1A1A;
        border-radius: 15px; padding: 15px; margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6);
    }
    
    .card-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 12px; }
    .coin-name { color: #D4AF37; font-size: 22px; font-weight: 800; }
    .coin-price { color: #FFF; font-size: 22px; font-weight: 800; font-family: monospace; }
    
    .data-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .data-item { background: #111; padding: 12px; border-radius: 10px; text-align: center; border: 1px solid #222; }
    .val-label { font-size: 10px; color: #777; text-transform: uppercase; margin-bottom: 4px; font-weight: bold; }
    .val-price { font-size: 16px; font-weight: bold; font-family: monospace; }
    
    .vision-footer { display: flex; justify-content: space-around; margin-top: 12px; padding-top: 10px; border-top: 1px dashed #333; }
    .footer-label { font-size: 9px; color: #555; text-transform: uppercase; }
    .footer-val { font-size: 13px; color: #888; font-weight: bold; font-family: monospace; }

    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# Lógica de Inicialização e Reset Automático Binance (00:00 UTC)
utc_now = datetime.now(pytz.utc)
if 'last_reset_utc' not in st.session_state:
    st.session_state['last_reset_utc'] = utc_now.day

if utc_now.day != st.session_state['last_reset_utc']:
    for t in COINS_CONFIG:
        val = yf.Ticker(t).fast_info['last_price']
        st.session_state[f'rv_{t}'] = val
        st.session_state[f'mp_{t}'] = val
    st.session_state['last_reset_utc'] = 
