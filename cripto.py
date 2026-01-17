import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# CSS ESTILO TERMINAL COM PISCA-PISCA SINCRONIZADO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 40px; font-weight: 700; text-align: center; margin-bottom: 0px; text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.6); }
    .subtitle-vision { color: #C0C0C0; font-size: 18px; text-align: center; margin-top: -5px; letter-spacing: 8px; margin-bottom: 20px; }
    .header-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .col-head { font-size: 9px; flex: 1; text-align: center; font-weight: 800; color: #BBB; text-transform: uppercase; }
    .row-container { display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 13px; flex: 1.2; font-weight: 700; padding-left: 10px; }
    .col-price { font-weight: 800; font-size: 14px; flex: 1.5; text-align: center; }
    
    /* ANIMAÇÕES DE EXAUSTÃO */
    .blink-alta { color: #FF0000 !important; animation: blinker 0.6s linear infinite; font-size: 16px !important; }
    .blink-baixa { color: #00FFFF !important; animation: blinker 0.8s linear infinite; font-size: 16px !important; }
    
    .status-box { padding: 4px; border-radius: 4px; font-weight: 800; font-size: 9px; width: 95%; margin: auto; text-align: center; color: white; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-exaust-alta { background-color: #FF0000; animation: blinker 0.6s linear infinite; }
    .bg-exaust-baixa { background-color: #0000FF; animation: blinker 0.8s linear infinite; }

    @keyframes blinker { 50% { opacity: 0.1; } }
    </style>
    """, unsafe_allow_html=True)

# LISTA DE ATIVOS EXPANDIDA
assets = {
    'BTC-USD': 'BTC/USDT', 'ETH-USD': 'ETH/USDT', 'SOL-USD': 'SOL/USDT', 'BNB-USD': 'BNB/USDT', 
    'XRP-USD': 'XRP/USDT', 'DOGE-USD': 'DOGE/USDT', 'ADA-USD': 'ADA/USDT', 'AVAX-USD': 'AVAX/USDT', 
    'DOT-USD': 'DOT/USDT', 'LINK-USD': 'LINK/USDT', 'TRX-USD': 'TRX/USDT', 'MATIC-USD': 'POL/USDT', 
    'SHIB-USD': 'SHIB/USDT', 'LTC-USD': 'LTC/USDT', 'BCH-USD': 'BCH/USDT', 'NEAR-USD': 'NEAR/USDT', 
    'GALA-USD': 'GALA/USDT', 'PEPE-USD': 'PEPE/USDT', 'EGLD-USD': 'EGLD/USDT', 'AAVE-USD': 'AAVE/USDT',
    'RENDER-USD': 'RENDER/USDT', 'SUI-USD': 'SUI/USDT', 'FET-USD': 'FET/USDT', 'FIL-USD': 'FIL/USDT'
}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        tickers = yf.Tickers(' '.join(assets.keys()))
        with placeholder.container():
            st.markdown("""
                <div class="header-container">
                    <div class="col-head" style="flex:1.2;">ATIVO</div>
                    <div class="col-head" style="flex:1.5;">PREÇO (VWAP)</div>
                    <div class="col-head" style="color:#FFFF00;">PONTO DECISÃO</div>
                    <div class="col-head" style="color:#FFA500;">PRÓX TOPO</div>
                    <div class="col-head" style="color:#FF0000;">TETO EXAUSTÃO</div>
                    <div class="col-head" style="color:#FFFF00;">SUPORTE</div>
                    <div class="col-head" style="color:#FFA500;">FUNDO</div>
                    <div class="col-head" style="color:#00FF00;">CHÃO EXAUSTÃO</div>
                    <div class="col-head">SINAL</div>
                </div>
                """, unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    info = tickers.tickers[tid].fast_info
                    price = info.last_price
                    open_p = info.open
                    if price is None or open_p is None: continue
                    change = ((price - open_p) / open_p) * 100
                    
                    # Alvos
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    # LÓGICA DE ALERTA E PISCA-PISCA
                    s_txt = "ESTÁVEL"; s_class = "bg-estavel"; p_class = ""
                    teto_style = ""; chao_style = ""
                    
                    if price >= v10:
                        s_txt = "EXAUST. ALTA"; s_class = "bg-exaust-alta"; p_class = "blink-alta"
                        teto_style = "font-weight:900; font-size:14px; text-decoration:underline;"
                    elif price <= c10:
                        s_txt = "EXAUST. BAIXA"; s_class = "bg-exaust-baixa"; p_class = "blink-baixa"
                        chao_style = "font-weight:900; font-size:14px; text-decoration:underline;"

                    prec = 8 if price < 0.01 else (4 if price < 1 else 2)
                    seta = '▲' if price >= open_p else '▼'
                    seta_c = '#00FF00' if price >= open_p else '#FF0000'

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="col-ativo">{name}</div>
                            <div class="col-price {p_class}" style="color:#FF8C00;">
                                {price:.{prec}f} <span style="color:{seta_c};">{seta}</span>
                                <div style="font-size:9px; color:{seta_c};">({change:+.2f}%)</div>
                            </div>
                            <div style="flex:1; text-align:center; color:#FFFF00; font-size:11px;">{v4:.{prec}f}</div>
                            <div style="flex:1; text-align:center; color:#FFA500; font-size:11px;">{v8:.{prec}f}</div>
                            <div style="flex:1; text-align:center; color:#FF0000; font-size:11px; {teto_style}">{v10:.{prec}f}</div>
                            <div style="flex:1; text-align:center; color:#FFFF00; font-size:11px;">{c4:.{prec}f}</div>
                            <div style="flex:1; text-align:center; color:#FFA500; font-size:11px;">{c8:.{prec}f}</div>
                            <div style="flex:1; text-align:center; color:#00FF00; font-size:11px; {chao_style}">{c10:.{prec}f}</div>
                            <div style="flex:1;"><div class="status-box {s_class}">{s_txt}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: time.sleep(10)
