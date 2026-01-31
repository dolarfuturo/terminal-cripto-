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
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; margin-top: 20px; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 25px 0; border-bottom: 1px solid #151515; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; white-space: nowrap; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 13px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 35px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO
def get_midpoint_v13(ticker_symbol):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download(ticker_symbol, start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not df.empty:
            return (float(df['High'].max()) + float(df['Low'].min())) / 2
        return 0
    except:
        return 0

# 3. CONFIGURAÇÃO DE ATIVOS
# BTC e ETH usam alvos 0.40, 0.61, 0.83, 1.22
# ALTS usam 4, 6, 12 (convertidos em multiplicadores: 1.04, 1.06, 1.12)
ativos = {
    "BTC-USD": [1.0122, 1.0083, 1.0061, 1.0040, 0.9939, 0.9878],
    "ETH-USD": [1.0122, 1.0083, 1.0061, 1.0040, 0.9939, 0.9878],
    "BNB-USD": [1.12, 1.06, 1.04, 1.02, 0.96, 0.88],
    "SOL-USD": [1.12, 1.06, 1.04, 1.02, 0.96, 0.88],
    "XRP-USD": [1.12, 1.06, 1.04, 1.02, 0.96, 0.88],
    "DOGE-USD": [1.12, 1.06, 1.04, 1.02, 0.96, 0.88]
}

if 'precos_base' not in st.session_state:
    st.session_state.precos_base = {symbol: get_midpoint_v13(symbol) for symbol in ativos}

# INTERFACE
st.markdown('<div class="title-container"><div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div></div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        
        # Reset Binance (18:00 BR)
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
            st.session_state.precos_base = {symbol: get_midpoint_v13(symbol) for symbol in ativos}
            st.rerun()

        with placeholder.container():
            for symbol, alvos in ativos.items():
                ticker = yf.Ticker(symbol)
                price = ticker.fast_info['last_price']
                mp = st.session_state.precos_base[symbol]
                
                # Variação para o ResetVision
                var_reset = ((price / mp) - 1) * 100
                cor_v = "#00FF00" if var_reset >= 0 else "#FF4444"
                seta_v = "▲" if var_reset >= 0 else "▼"
                
                # Lógica de Gatilho (Escada)
                # Para BTC/ETH 1.35% | Para Alts 13%
                gatilho = 1.35 if "BTC" in symbol or "ETH" in symbol else 13.0
                if var_reset >= gatilho:
                    st.session_state.precos_base[symbol] = mp * alvos[0]
                elif var_reset <= -gatilho:
                    st.session_state.precos_base[symbol] = mp * (2 - alvos[0])

                st.markdown(f"""
                    <div class="header-container">
                        <div class="h-col">{symbol.replace('-USD','')}</div><div class="h-col">PREÇO ATUAL</div>
                        <div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                        <div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div>
                        <div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div>
                    </div>
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{symbol.split('-')[0]}</div>
                        <div class="w-col">
                            <div style="line-height: 1.1;">{price:,.2f}</div>
                            <div style="color:{cor_v}; font-size:11px;">{seta_v} {var_reset:+.2f}%</div>
                        </div>
                        <div class="w-col" style="color:#FF4444;">{mp * alvos[0]:,.2f}</div>
                        <div class="w-col" style="color:#FFA500;">{mp * alvos[1]:,.2f}</div>
                        <div class="w-col">{mp * alvos[2]:,.2f}</div>
                        <div class="w-col" style="color:#00CED1;">{mp * alvos[3]:,.2f}</div>
                        <div class="w-col" style="color:#FFA500;">{mp * alvos[4]:,.2f}</div>
                        <div class="w-col" style="color:#00FF00;">{mp * alvos[5]:,.2f}</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""<div style="height:100px;"></div>""", unsafe_allow_html=True) # Espaço para o footer não tampar

        st.markdown(f"""
            <div class="footer">
                <div><span class="dot"></span> LIVESTREAM ATIVO</div>
                <div>BRASÍLIA: {now_br.strftime('%H:%M:%S')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(2)
    except Exception as e:
        time.sleep(5)
