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
    .h-col { font-size: 13px; color: #FFFFFF; text-transform: uppercase; text-align: center; font-weight: 800; letter-spacing: 1px; flex: 1; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 12px 0; border-bottom: 1px solid #151515; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 16px; font-weight: 800; }
    
    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 11px; width: 90%; margin: 0 auto; text-transform: uppercase; }
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-decisao { background-color: #FFFF00 !important; color: #000 !important; }
    .bg-atencao { background-color: #FFA500 !important; color: #000 !important; }
    .target-blink-red { background-color: #FF0000 !important; color: #FFF !important; animation: blinker 0.6s linear infinite; }
    .target-blink-green { background-color: #00FF00 !important; color: #000 !important; animation: blinker 0.6s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DO EIXO (MAX+MIN/2 | 11:30 - 18:00 BR)
def get_eixo():
    try:
        ticker = yf.Ticker("BTC-USD")
        hist = ticker.history(period="2d", interval="1m")
        hist.index = hist.index.tz_convert('America/Sao_Paulo')
        # Filtra horário institucional
        df_range = hist.between_time('11:30', '18:00')
        if not df_range.empty:
            return (df_range['High'].max() + df_range['Low'].min()) / 2
        return 89795.0
    except:
        return 89795.0

# 3. MONITORAMENTO
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

eixo_institucional = get_eixo()
placeholder = st.empty()

while True:
    try:
        btc_data = yf.Ticker("BTC-USD").fast_info
        price = btc_data['last_price']
        change_pct = ((price / eixo_institucional) - 1) * 100
        
        with placeholder.container():
            # Cabeçalho Fixo
            st.markdown(f"""
                <div class="header-container">
                    <div class="h-col">ATIVO</div>
                    <div class="h-col">PREÇO (EIXO: {eixo_institucional:,.0f})</div>
                    <div class="h-col">EXAUSTÃO (1.22)</div>
                    <div class="h-col">TOPO (0.83)</div>
                    <div class="h-col">DECISÃO (0.61)</div>
                    <div class="h-col">RESPIRO (0.40)</div>
                    <div class="h-col">DECISÃO F. (-0.61)</div>
                    <div class="h-col">EXAUSTÃO F. (-1.22)</div>
                    <div class="h-col">SINALIZADOR</div>
                </div>
            """, unsafe_allow_html=True)

            def c(p): return eixo_institucional * (1 + (p/100))
            
            abs_c = abs(change_pct)
            s_txt, s_class = "ESTÁVEL", "bg-estavel"
            if abs_c >= 1.22: s_txt, s_class = "EXAUSTÃO", "target-blink-red" if change_pct > 0 else "target-blink-green"
            elif abs_c >= 0.83: s_txt, s_class = "PRÓX. TOPO", "bg-atencao"
            elif abs_c >= 0.61: s_txt, s_class = "DECISÃO", "bg-decisao"

            t_color = "#00FF00" if price >= eixo_institucional else "#FF0000"

            st.markdown(f"""
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37;">BTC/USDT</div>
                    <div class="w-col" style="color:#FFF;">{price:,.2f}<br><span style="font-size:12px; color:{t_color};">{change_pct:+.2f}%</span></div>
                    <div class="w-col" style="color:#FF4444;">{c(1.22):,.0f}</div>
                    <div class="w-col" style="color:#FFA500;">{c(0.83):,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{c(0.61):,.0f}</div>
                    <div class="w-col" style="color:#00CED1;">{c(0.40):,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{c(-0.61):,.0f}</div>
                    <div class="w-col" style="color:#00FF00;">{c(-1.22):,.0f}</div>
                    <div class="w-col"><div class="status-box {s_class}">{s_txt}</div></div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div style="color:#555; text-align:center; margin-top:30px; font-weight:bold;">🟢 LIVE / RESET 00:00 UTC / MÉDIA 11:30-18:00 BR</div>', unsafe_allow_html=True)
            
        time.sleep(3)
    except:
        time.sleep(5)
