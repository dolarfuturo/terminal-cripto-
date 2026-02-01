import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA VISION
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

COINS_CONFIG = {
    "BTC-USD": {"label": "BTC/USDT", "dec": 0},
    "ETH-USD": {"label": "ETH/USDT", "dec": 0},
    "SOL-USD": {"label": "SOL/USDT", "dec": 2},
    "BNB-USD": {"label": "BNB/USDT", "dec": 2},
    "XRP-USD": {"label": "XRP/USDT", "dec": 4},
    "DOGE-USD": {"label": "DOGE/USDT", "dec": 4},
    "ADA-USD": {"label": "ADA/USDT", "dec": 4},
    "AVAX-USD": {"label": "AVAX/USDT", "dec": 2}
}

# CSS MOBILE FIRST (Adaptável)
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    /* Espaçamento para o cabeçalho não cobrir os cards */
    [data-testid="stVerticalBlock"] { padding-top: 140px !important; }

    .top-header-fixed {
        position: fixed; top: 0; left: 0; right: 0;
        height: 130px; background: #000; z-index: 9999;
        border-bottom: 2px solid #D4AF37; display: flex;
        flex-direction: column; align-items: center; justify-content: center;
    }

    .title-gold { color: #D4AF37; font-size: 22px; font-weight: 900; letter-spacing: 2px; }
    .live-tag { background: #FF0000; color: #FFF; font-size: 10px; padding: 2px 8px; border-radius: 4px; margin-top: 5px; animation: blink 1s infinite; }
    
    /* Estilo do Card Mobile */
    .mobile-card {
        background: #080808; border: 1px solid #1A1A1A;
        border-radius: 12px; padding: 12px; margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .coin-name { color: #D4AF37; font-size: 18px; font-weight: 800; }
    .coin-price { color: #FFF; font-size: 18px; font-weight: 800; font-family: monospace; }
    
    .data-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .data-item { 
        background: #111; padding: 8px; border-radius: 6px; 
        text-align: center; border: 1px solid #222;
    }
    .val-label { font-size: 9px; color: #666; text-transform: uppercase; margin-bottom: 3px; }
    .val-price { font-size: 14px; font-weight: bold; font-family: monospace; }

    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# Lógica de Reset 00:00 UTC
utc_now = datetime.now(pytz.utc)
if 'last_reset_utc' not in st.session_state:
    st.session_state['last_reset_utc'] = utc_now.day

if 'mp_state' not in st.session_state: st.session_state['mp_state'] = {}
if 'rv_state' not in st.session_state: st.session_state['rv_state'] = {}

placeholder = st.empty()

while True:
    try:
        with placeholder.container():
            # TOPO FIXO
            st.markdown(f"""
                <div class="top-header-fixed">
                    <div class="title-gold">ALPHA VISION CRYPTO</div>
                    <div style="color:#888; font-size:11px; font-family:monospace;">{datetime.now().strftime('%H:%M:%S')}</div>
                    <div class="live-tag">LIVE MOBILE</div>
                </div>
            """, unsafe_allow_html=True)

            for t, info in COINS_CONFIG.items():
                price = yf.Ticker(t).fast_info['last_price']
                
                # Cálculo de bandas (Exemplo baseado na sua lógica Alpha)
                ex_t = price * 1.0135
                ex_f = price * 0.9865
                dec = price * 1.0061
                anc = price * 0.995

                st.markdown(f"""
                    <div class="mobile-card">
                        <div class="card-header">
                            <span class="coin-name">{info['label']}</span>
                            <span class="coin-price">{f"{price:,.{info['dec']}f}"}</span>
                        </div>
                        <div class="data-grid">
                            <div class="data-item">
                                <div class="val-label" style="color:#FF4444;">Exaustão T.</div>
                                <div class="val-price" style="color:#FF4444;">{f"{ex_t:,.{info['dec']}f}"}</div>
                            </div>
                            <div class="data-item">
                                <div class="val-label" style="color:#00FF00;">Exaustão F.</div>
                                <div class="val-price" style="color:#00FF00;">{f"{ex_f:,.{info['dec']}f}"}</div>
                            </div>
                            <div class="data-item">
                                <div class="val-label" style="color:#FFFF00;">Decisão</div>
                                <div class="val-price" style="color:#FFFF00;">{f"{dec:,.{info['dec']}f}"}</div>
                            </div>
                            <div class="data-item">
                                <div class="val-label" style="color:#00e6ff;">Âncora</div>
                                <div class="val-price" style="color:#00e6ff;">{f"{anc:,.{info['dec']}f}"}</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        time.sleep(1)
    except: time.sleep(5)
