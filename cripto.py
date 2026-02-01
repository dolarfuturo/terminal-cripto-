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

# CSS PARA TRAVAMENTO E ALINHAMENTO MILIMÉTRICO
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    header, [data-testid="stHeader"] { display: none; }
    
    /* FORÇA O PRIMEIRO BLOCO A FICAR FIXO NO TOPO */
    [data-testid="stVerticalBlock"] > div:first-child {
        position: fixed;
        top: 0; left: 0; width: 100%;
        z-index: 999999;
        background-color: #000;
        border-bottom: 2px solid #D4AF37;
    }
    
    .top-bar { display: flex; justify-content: space-between; padding: 5px 30px; background: #050505; color: #FFF; font-family: monospace; font-size: 13px; }
    .title-gold { color: #D4AF37; font-size: 52px; font-weight: 900; text-align: center; line-height: 1; margin: 15px 0 5px 0; }
    .subtitle-white { color: #FFF; font-size: 20px; text-align: center; letter-spacing: 10px; text-transform: lowercase; margin-bottom: 15px; }
    
    /* GRID DE ALINHAMENTO UNIFICADO - CABEÇALHO E LINHAS IDENTICOS */
    .grid-layout { 
        display: grid; 
        grid-template-columns: 1.2fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; 
        width: 100%; text-align: center;
    }
    
    .h-col { font-size: 11px; color: #FFF; font-weight: 800; padding: 15px 0; background: #0A0A0A; border-top: 1px solid #222; }
    .w-col { font-family: monospace; font-size: 20px; font-weight: 800; color: #FFF; padding: 10px 0; }
    
    /* COMPENSA O ESPAÇO DO CABEÇALHO FIXO */
    .spacer { margin-top: 260px; }

    .vision-block { display: flex; justify-content: center; gap: 70px; padding: 5px 0 20px 0; border-bottom: 4px solid #333; margin-bottom: 5px; }
    .dot { height:
