import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - VISUAL REFINADO
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-container { text-align: center; padding: 15px; }
    .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; }
    .subtitle-white { color: #FFFFFF; font-size: 16px; font-weight: 300; letter-spacing: 5.5px; margin-top: 2px; text-transform: lowercase; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 15px 0; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 18px; font-weight: 800; color: #FFF; white-space: nowrap; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 13px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 35px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA HIERARQUIA
config_ativos = {
    "BTC-USD":  {"nome": "BTC/USDT", "gatilho": 1.35, "mov": 0.0122, "ex_t": 1.0122, "topo": 1.0083, "dec": 1.0061, "resp": 1.0040, "pf": 0.9939, "ex_f": 0.9878},
    "ETH-USD":  {"nome": "ETH/USDT", "gatilho": 1.35, "mov": 0.0122, "ex_t": 1.0122, "topo": 1.0083, "dec": 1.0061, "resp": 1.0040, "pf": 0.9939, "ex_f": 0.9878},
    "SOL-USD":  {"nome": "SOL/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1200, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8800},
    "BNB-USD":  {"nome": "BNB/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1200, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8800},
    "XRP-USD":  {"nome": "XRP/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1200, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8800},
    "DOGE-USD": {"nome": "DOGE/USDT", "gatilho": 6.50, "mov": 0.0600, "ex_t": 1.1200, "topo": 1.0600, "dec": 1.0400, "resp": 1.0200, "pf": 0.9600, "ex_f": 0.8800}
}

# 3. MOTOR DE CÁLCULO
def get_midpoint_multi(ticker_symbol):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        if now_br.weekday() >= 5 or (now_br.weekday() == 0 and now_br.hour < 18):
            return None 
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download(ticker_symbol, start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_window = df.between_time('11:30', '18:00')
        if not df_window.empty:
            return (float(df_window['High'].max()) + float(df_window['Low'].min())) / 2
        return None
    except: return None

if 'data_ativos' not in st.session_state:
    st.session_state.data_ativos = {}
    for ticker in config_ativos.keys():
        val = get_midpoint_multi(ticker)
        if val is None:
            if "BTC" in ticker: val = 103000.00
            elif "ETH" in ticker: val = 2400.00
            elif "SOL" in ticker: val = 100.00
            elif "BNB" in ticker: val = 300.00
            elif "XRP" in ticker: val = 1.50
            else: val = 0.20
        st.session_state.data_ativos[ticker] = {"mp": val, "rv": val}

st.markdown("""<div class="title-container"><div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div></div>""", unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        br_tz, ny_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York')
        now_br, now_ny = datetime.now(br_tz), datetime.now(ny_tz)

        precos_atuais = {}
        for ticker in config_ativos.keys():
            t = yf.Ticker(ticker)
            precos_atuais[ticker] = t.fast_info['last_price']

        with placeholder.container():
            st.markdown("""<div class="header-container"><div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div><div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div><div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div><div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div></div>""", unsafe_allow_html=True)
            
            for ticker, cfg in config_ativos.items():
                price = precos_atuais[ticker]
                mp = st.session_state.data_ativos[ticker]["mp"]
                rv = st.session_state.data_ativos[ticker]["rv"]
                
                var_mp = ((price / mp) - 1) * 100
                var_rv = ((price / rv) - 1) * 100

                if var_mp >= cfg["gatilho"]:
                    st.session_state.data_ativos[ticker]["mp"] = mp * (1 + cfg["mov"])
                elif var_mp <= -cfg["gatilho"]:
                    st.session_state.data_ativos[ticker]["mp"] = mp * (1 - cfg["mov"])

                cor_v = "#00FF00" if var_rv >= 0 else "#FF4444"
                seta_v = "▲" if var_rv >= 0 else "▼"
                
                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37; font-weight:bold;">{cfg['nome']}</div>
                        <div class="w-col">
                            <div style="font-weight: bold;">{price:,.2f}</div>
                            <div style="color:{cor_v}; font-size:11px;">{seta_v} {var_rv:+.2f}%</div>
                        </div>
                        <div class="w-col" style="color:#FF4444;">{mp*cfg['ex_t']:,.2f}</div>
                        <div class="w-col" style="color:#FFA500;">{mp*cfg['topo']:,.2f}</div>
                        <div class="w-col" style="color:#FFFF00;">{mp*cfg['dec']:,.2f}</div>
                        <div class="w-col" style="color:#00CED1;">{mp*cfg['resp']:,.2f}</div>
                        <div class="w-col" style="color:#FFA500;">{mp*cfg['pf']:,.2f}</div>
                        <div class="w-col" style="color:#00FF00;">{mp*cfg['ex_f']:,.2f}</div>
                    </div>
                    <div style="display: flex; justify-content: center; gap: 40px; margin-top: -12px; padding-bottom: 12px; border-bottom: 1px solid #151515;">
                        <div style="text-align: center;">
                            <span style="color: #666; font-size: 9px; text-transform: uppercase;">ResetVision:</span>
                            <span style="color: #bbb; font-size: 11px; font-family: monospace;">{rv:,.2f}</span>
                        </div>
                        <div style="text-align: center;">
                            <span style="color: #666; font-size: 9px; text-transform: uppercase;">AncoraVision:</span>
                            <span style="color: #00e6ff; font-size: 11px; font-family: monospace;">{mp:,.2f}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="footer">
                    <div><span class="dot"></span>LIVESTREAM ATIVO</div>
                    <div>BRASÍLIA: {now_br.strftime('%H:%M:%S')}</div>
                    <div>NEW YORK: {now_ny.strftime('%H:%M:%S')}</div>
                </div>
            """, unsafe_allow_html=True)
            
        time.sleep(2)
    except Exception as e:
        time.sleep(5)
