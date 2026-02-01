import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. CONFIGURAÇÃO DO TERMINAL (TOP 20)
st.set_page_config(page_title="ALPHA VISION PRO", layout="wide", initial_sidebar_state="collapsed")

# Dicionário com as 20 mais líquidas e suas casas decimais
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

# FUNÇÃO DE CÁLCULO MÁX+MÍN/2 (Sexta 11:30 até 18:00 se for FDS)
def get_alpha_midpoint(ticker):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(br_tz)
        # Lógica de Reset: Sexta a Segunda
        if now.weekday() >= 5 or (now.weekday() == 0 and now.hour < 18):
            days_back = (now.weekday() - 4) if now.weekday() >= 5 else 3
            target_date = now - timedelta(days=days_back)
        else:
            target_date = now if now.hour >= 18 else now - timedelta(days=1)
        
        df = yf.download(ticker, start=target_date.strftime('%Y-%m-%d'), interval="5m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_window = df.between_time('11:30', '18:00')
        
        if not df_window.empty:
            return (float(df_window['High'].max()) + float(df_window['Low'].min())) / 2
        return yf.Ticker(ticker).fast_info['last_price']
    except: return 0

# INICIALIZAÇÃO
for t in COINS_CONFIG:
    if f'rv_{t}' not in st.session_state:
        val = get_alpha_midpoint(t)
        st.session_state[f'rv_{t}'] = val
        st.session_state[f'mp_{t}'] = val

# CSS VISUAL PROFISSIONAL
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 32px; font-weight: 900; text-align: center; letter-spacing: 2px; }
    .header-container { display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; position: sticky; top: 0; z-index: 999; }
    .h-col { font-size: 10px; color: #FFF; text-align: center; font-weight: 800; }
    .row-container { display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; width: 100%; align-items: center; padding: 15px 0; border-bottom: 1px solid #151515; }
    .w-col { text-align: center; font-family: 'monospace'; font-size: 18px; font-weight: 800; color: #FFF; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        with placeholder.container():
            st.markdown('<div class="title-gold">ALPHA VISION PRO • TOP 20</div>', unsafe_allow_html=True)
            st.markdown('<div class="header-container"><div class="h-col">CÓDIGO</div><div class="h-col">PREÇO</div><div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">ÂNCORA UP</div><div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div><div class="h-col">ÂNCORA DOWN</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div></div>', unsafe_allow_html=True)

            for t, info in COINS_CONFIG.items():
                price = yf.Ticker(t).fast_info['last_price']
                mp = st.session_state[f'mp_{t}']
                rv = st.session_state[f'rv_{t}']
                
                # REGRA DE RÉGUA: BTC/ETH (1.22%) | OUTRAS (12.2%)
                if t in ["BTC-USD", "ETH-USD"]:
                    g_ex, g_mov, g_dec, g_res = 1.35, 1.0122, 1.0061, 1.0040
                else:
                    g_ex, g_mov, g_dec, g_res = 13.5, 1.122, 1.061, 1.040
                
                var_escada = ((price / mp) - 1) * 100
                if var_escada >= g_ex: st.session_state[f'mp_{t}'] = mp * g_mov
                elif var_escada <= -g_ex: st.session_state[f'mp_{t}'] = mp * (2 - g_mov)
                
                var_reset = ((price / rv) - 1) * 100
                cor_v = "#00FF00" if var_reset >= 0 else "#FF4444"
                
                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{info['label']}</div>
                        <div class="w-col">
                            <div>{f"{price:,.{info['dec']}f}"}</div>
                            <div style="color:{cor_v}; font-size:10px;">{var_reset:+.2f}%</div>
                        </div>
                        <div class="w-col" style="color:#FF4444;">{f"{(mp * (1 + g_ex/100)):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#FFA500;">{f"{(mp * g_mov):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#FFFF00;">{f"{(mp * g_dec):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#00CED1;">{f"{(mp * g_res):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#FFA500;">{f"{(mp * (2 - g_mov)):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#00FF00;">{f"{(mp * (1 - g_ex/100)):,.{info['dec']}f}"}</div>
                    </div>
                """, unsafe_allow_html=True)
        time.sleep(2)
    except: time.sleep(5)
