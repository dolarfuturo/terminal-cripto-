import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-container { text-align: center; padding: 15px; }
    .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; letter-spacing: 2px; }
    .subtitle-white { color: #FFFFFF; font-size: 16px; font-weight: 300; letter-spacing: 5.5px; text-transform: lowercase; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 15px 0; border-bottom: 1px solid #151515; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 18px; font-weight: 800; color: #FFF; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 10px; font-size: 12px; display: flex; justify-content: center; gap: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO (CALIBRAGEM 1.115% EXTRAÍDA DO SEU MESTRE)
config_ativos = {
    "BTC-USD":  {"nome": "BTC/USDT", "gatilho": 1.35, "mov": 0.0122, "ex_t": 1.01115, "topo": 1.0083, "dec": 1.0061, "resp": 1.0040, "pf": 0.9939, "ex_f": 0.98885},
    "ETH-USD":  {"nome": "ETH/USDT", "gatilho": 1.35, "mov": 0.0122, "ex_t": 1.01115, "topo": 1.0083, "dec": 1.0061, "resp": 1.0040, "pf": 0.9939, "ex_f": 0.98885},
    "SOL-USD":  {"nome": "SOL/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1115, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8885},
    "BNB-USD":  {"nome": "BNB/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1115, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8885},
    "XRP-USD":  {"nome": "XRP/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1115, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8885},
    "DOGE-USD": {"nome": "DOGE/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1115, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8885}
}

# 3. MOTOR DE CÁLCULO (RESETVISION 18:00 BR)
def get_reset_vision(ticker):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(br_tz)
        # Se for FDS, pega o fechamento de sexta às 18h
        if now.weekday() >= 5:
            dias_atras = now.weekday() - 4
            target = now - timedelta(days=dias_atras)
        else:
            target = now if now.hour >= 18 else now - timedelta(days=1)
            
        data = yf.download(ticker, start=target.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not data.empty:
            data.index = data.index.tz_convert(br_tz)
            # Pega o preço mais próximo das 18:00 BR
            precos_18h = data.between_time('17:55', '18:05')
            if not precos_18h.empty:
                return float(precos_18h['Close'].iloc[-1])
        return yf.Ticker(ticker).fast_info['last_price']
    except:
        return 0

if 'data_ativos' not in st.session_state:
    st.session_state.data_ativos = {t: {"mp": get_reset_vision(t), "rv": get_reset_vision(t)} for t in config_ativos}

st.markdown("""<div class="title-container"><div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div></div>""", unsafe_allow_html=True)
placeholder = st.empty()

while True:
    try:
        with placeholder.container():
            st.markdown("""<div class="header-container"><div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div><div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div><div class="h-col">DECISÃO</div><div class="h-col">RESPIRO</div><div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div></div>""", unsafe_allow_html=True)
            
            for ticker, cfg in config_ativos.items():
                price = yf.Ticker(ticker).fast_info['last_price']
                mp = st.session_state.data_ativos[ticker]["mp"]
                rv = st.session_state.data_ativos[ticker]["rv"]
                
                # ESCADA ANCORAVISION
                var_mp = ((price / mp) - 1) * 100
                if var_mp >= cfg["gatilho"]: st.session_state.data_ativos[ticker]["mp"] *= (1 + cfg["mov"])
                elif var_mp <= -cfg["gatilho"]: st.session_state.data_ativos[ticker]["mp"] *= (1 - cfg["mov"])

                var_rv = ((price / rv) - 1) * 100
                cor_v = "#00FF00" if var_rv >= 0 else "#FF4444"
                
                # Formatação segura para evitar o erro de sintaxe anterior
                p_f = f"{price:,.2f}" if price > 1 else f"{price:,.4f}"
                rv_f = f"{rv:,.2f}" if rv > 1 else f"{rv:,.4f}"
                mp_f = f"{mp:,.2f}" if mp > 1 else f"{mp:,.4f}"

                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{cfg['nome']}</div>
                        <div class="w-col"><div>{p_f}</div><div style="color:{cor_v}; font-size:11px;">{var_rv:+.2f}%</div></div>
                        <div class="w-col" style="color:#FF4444;">{mp*cfg['ex_t']:,.2f}</div>
                        <div class="w-col" style="color:#FFA500;">{mp*cfg['topo']:,.2f}</div>
                        <div class="w-col" style="color:#FFFF00;">{mp*cfg['dec']:,.2f}</div>
                        <div class="w-col" style="color:#00CED1;">{mp*cfg['resp']:,.2f}</div>
                        <div class="w-col" style="color:#FFA500;">{mp*cfg['pf']:,.2f}</div>
                        <div class="w-col" style="color:#00FF00;">{mp*cfg['ex_f']:,.2f}</div>
                    </div>
                    <div style="display: flex; justify-content: center; gap: 50px; background: #050505; padding: 5px;">
                        <div style="color:#888; font-size:10px;">RESETVISION: <span style="color:#FFF;">{rv_f}</span></div>
                        <div style="color:#888; font-size:10px;">ANCORAVISION: <span style="color:#00e6ff;">{mp_f}</span></div>
                    </div>
                """, unsafe_allow_html=True)
        time.sleep(2)
    except: time.sleep(5)
