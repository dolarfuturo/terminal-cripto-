import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP VISUAL
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .title-gold { color: #D4AF37; font-size: 30px; font-weight: 900; text-align: center; padding: 10px; }
    .header-container { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background: #080808; }
    .h-col { font-size: 10px; color: #FFF; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 12px 0; border-bottom: 1px solid #151515; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 16px; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO (FATOR 1.115% EXATO)
config_ativos = {
    "BTC-USD":  {"nome": "BTC/USDT", "gatilho": 1.35, "mov": 0.0122, "ex_t": 1.01115, "topo": 1.0083, "dec": 1.0061, "resp": 1.0040, "pf": 0.9939, "ex_f": 0.98885},
    "ETH-USD":  {"nome": "ETH/USDT", "gatilho": 1.35, "mov": 0.0122, "ex_t": 1.01115, "topo": 1.0083, "dec": 1.0061, "resp": 1.0040, "pf": 0.9939, "ex_f": 0.98885},
    "SOL-USD":  {"nome": "SOL/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1115, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8885},
    "XRP-USD":  {"nome": "XRP/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1115, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8885}
}

# 3. CÁLCULO MESTRE (MAX + MIN / 2) - SEXTA 11:30 ÀS 18:00
def get_mestre_value(ticker):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(br_tz)
        
        # Como hoje é sábado (31/01), recua para sexta (30/01)
        dias_para_sexta = (now.weekday() - 4) % 7
        target = now - timedelta(days=dias_para_sexta)
        
        df = yf.download(ticker, start=target.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not df.empty:
            df.index = df.index.tz_convert(br_tz)
            df_win = df.between_time('11:30', '18:00')
            if not df_win.empty:
                return (float(df_win['High'].max()) + float(df_win['Low'].min())) / 2
        return yf.Ticker(ticker).fast_info['last_price']
    except: return 0

# Inicializa Session State
if 'data_ativos' not in st.session_state:
    st.session_state.data_ativos = {t: {"mp": get_mestre_value(t), "rv": get_mestre_value(t)} for t in config_ativos}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
placeholder = st.empty()

while True:
    try:
        with placeholder.container():
            st.markdown("""<div class="header-container"><div class="h-col">CÓDIGO</div><div class="h-col">PREÇO</div><div class="h-col">EXAUSTÃO T.</div><div class="h-col">TOPO</div><div class="h-col">DECISÃO</div><div class="h-col">RESPIRO</div><div class="h-col">FUNDO</div><div class="h-col">EXAUSTÃO F.</div></div>""", unsafe_allow_html=True)
            
            for ticker, cfg in config_ativos.items():
                price = yf.Ticker(ticker).fast_info['last_price']
                mp, rv = st.session_state.data_ativos[ticker]["mp"], st.session_state.data_ativos[ticker]["rv"]
                
                # ESCADA ANCORAVISION (GATILHO 1.35% / MOV 1.22%)
                var_mp = ((price / mp) - 1) * 100
                if var_mp >= cfg["gatilho"]: st.session_state.data_ativos[ticker]["mp"] *= (1 + cfg["mov"])
                elif var_mp <= -cfg["gatilho"]: st.session_state.data_ativos[ticker]["mp"] *= (1 - cfg["mov"])

                # Formatação de preços
                fmt = ".2f" if price > 1 else ".4f"
                p_s, rv_s, mp_s = f"{price:{fmt}}", f"{rv:{fmt}}", f"{mp:{fmt}}"
                var_rv = ((price / rv) - 1) * 100

                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{cfg['nome']}</div>
                        <div class="w-col"><div>{p_s}</div><div style="font-size:10px; color:{"#0F0" if var_rv>0 else "#F00"}">{var_rv:+.2f}%</div></div>
                        <div class="w-col" style="color:#FF4444;">{mp*cfg['ex_t']:{fmt}}</div>
                        <div class="w-col">{mp*cfg['topo']:{fmt}}</div>
                        <div class="w-col" style="color:#FFFF00;">{mp*cfg['dec']:{fmt}}</div>
                        <div class="w-col">{mp*cfg['resp']:{fmt}}</div>
                        <div class="w-col">{mp*cfg['pf']:{fmt}}</div>
                        <div class="w-col" style="color:#00FF00;">{mp*cfg['ex_f']:{fmt}}</div>
                    </div>
                    <div style="display:flex; justify-content:center; gap:30px; font-size:10px; color:#666; margin-top:-10px;">
                        <span>RESETVISION (18H SEX): {rv_s}</span>
                        <span>ANCORAVISION: {mp_s}</span>
                    </div>
                """, unsafe_allow_html=True)
        time.sleep(2)
    except: time.sleep(5)
