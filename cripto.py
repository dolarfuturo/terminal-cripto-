import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime
import pytz

# 1. CONFIGURAÇÃO ALPHA VISION
st.set_page_config(page_title="ALPHA VISION BTC", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; padding-top: 10px; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 16px; text-align: center; margin-top: -5px; letter-spacing: 7px; margin-bottom: 25px; font-weight: 700; }
    
    .header-container { display: flex; width: 100%; padding: 15px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 13px; color: #FFFFFF; text-transform: uppercase; text-align: center; font-weight: 800; letter-spacing: 1px; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 10px 0; border-bottom: 1px solid #151515; }
    .w-ativo { width: 14%; text-align: left; padding-left: 10px; color: #D4AF37; font-size: 18px; font-weight: 700; }
    .w-price { width: 15%; text-align: center; color: #FFFFFF; font-size: 20px; font-weight: 900; }
    .w-target { width: 9%; text-align: center; font-size: 15px; font-weight: 800; }
    
    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 10px; width: 100%; text-align: center; text-transform: uppercase; }
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-decisao { background-color: #FFFF00 !important; color: #000 !important; }
    .bg-atencao { background-color: #FFA500 !important; color: #000 !important; }
    .target-blink-red { background-color: #FF0000 !important; color: #FFF !important; animation: blinker 0.6s linear infinite; }
    .target-blink-green { background-color: #00FF00 !important; color: #000 !important; animation: blinker 0.6s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    
    .footer-live { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #000; color: #00FF00; text-align: center; padding: 10px; font-size: 13px; font-weight: bold; border-top: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO DO EIXO (MÉDIA 11:30 - 18:00 BR)
def get_institutional_axis():
    try:
        ticker = yf.Ticker("BTC-USD")
        hist = ticker.history(period="2d", interval="1m")
        # Converte para horário de Brasília
        hist.index = hist.index.tz_convert('America/Sao_Paulo')
        # Filtra a janela institucional
        df_janela = hist.between_time('11:30', '18:00')
        
        if not df_janela.empty:
            max_p = df_janela['High'].max()
            min_p = df_janela['Low'].min()
            return (max_p + min_p) / 2
        return 89795.0 # Fallback
    except:
        return 89795.0

# 3. MONITORAMENTO REAL-TIME
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

EIXO = get_institutional_axis()
placeholder = st.empty()

while True:
    try:
        btc = yf.Ticker("BTC-USD").fast_info
        price = btc['last_price']
        change_pct = ((price / EIXO) - 1) * 100
        
        with placeholder.container():
            st.markdown(f"""<div class="header-container">
                <div class="h-col" style="width:14%; text-align:left; padding-left:10px;">BTC/USDT</div>
                <div class="h-
