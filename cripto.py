import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# CSS ESTILO TERMINAL ALPHA VISION
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
    .col-price { color: #FF8C00; font-weight: 800; font-size: 14px; flex: 1.5; text-align: center; }
    .status-box { padding: 4px; border-radius: 4px; font-weight: 800; font-size: 9px; width: 90%; margin: auto; text-align: center; color: white; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-exaustao { background-color: #FF0000; animation: blinker 0.6s linear infinite; } 
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# LISTA MASSIVA DE ATIVOS (TOP MARKET CAP)
assets = {
    'BTC-USD': 'BTC/USDT', 'ETH-USD': 'ETH/USDT', 'SOL-USD': 'SOL/USDT', 
    'BNB-USD': 'BNB/USDT', 'XRP-USD': 'XRP/USDT', 'DOGE-USD': 'DOGE/USDT',
    'ADA-USD': 'ADA/USDT', 'AVAX-USD': 'AVAX/USDT', 'DOT-USD': 'DOT/USDT',
    'LINK-USD': 'LINK/USDT', 'TRX-USD': 'TRX/USDT', 'MATIC-USD': 'POL/USDT',
    'SHIB-USD': 'SHIB/USDT', 'LTC-USD': 'LTC/USDT', 'BCH-USD': 'BCH/USDT',
    'NEAR-USD': 'NEAR/USDT', 'APT-USD': 'APT/USDT', 'ARB-USD': 'ARB/USDT',
    'OP-USD': 'OP/USDT', 'SUI-USD': 'SUI/USDT', 'PEPE-USD': 'PEPE/USDT',
    'BONK-USD': 'BONK/USDT', 'FLOKI-USD': 'FLOKI/USDT', 'STX-USD': 'STX/USDT',
    'RENDER-USD': 'RENDER/USDT', 'TIA-USD': 'TIA/USDT', 'INJ-USD': 'INJ/USDT',
    'ICP-USD': 'ICP/USDT', 'FIL-USD': 'FIL/USDT', 'KAS-USD': 'KAS/USDT',
    'FET-USD': 'FET/USDT', 'RUNE-USD': 'RUNE/USDT', 'GALA-USD': 'GALA/USDT',
    'LDO-USD': 'LDO/USDT', 'ENA-USD': 'ENA/USDT', 'WIF-USD': 'WIF/USDT'
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
                    <div class="col-head" style="flex:1.5;">PREÇO (VAR%)</div>
                    <div class="col-head" style="color:#FFFF00;">PONTO DECISÃO</div>
                    <div class="col-head" style="color:#FFA500;">PRÓX TOPO</div>
                    <div class="col-head" style="color:#FF0000;">TETO EXAUSTÃO</div>
                    <div class="col-head" style="color:#FFFF00;">SUPORTE DECISÃO</div>
                    <div class="col-head" style="color:#FFA500;">PRÓX FUNDO</div>
                    <div class="col-head" style="color:#00FF00;">CHÃO EXAUSTÃO</div>
                    <div class="col-head">SINAL</div>
                </div>
                """, unsafe_allow_html=True)

            for ticker_id, display_name in assets.items():
                try:
                    # Coleta segura de dados
                    t_obj = tickers.tickers[ticker_id]
                    info = t_obj.fast_info
                    
                    price = info.last_price
                    open_price = info.open
                    
                    if price is None or open_price is None or price == 0:
                        continue

                    change = ((price - open_price) / open_price) * 100
                    
                    # SETA ESTATÍSTICA (Abertura Diária Yahoo)
                    seta = '▲' if price >= open_price else '▼'
                    color_seta = "#00FF00" if price >= open_price else "#FF0000"
                    color_var = "#00FF00" if change >= 0 else "#FF0000"
                    
                    # PRECISÃO DECIMAL PARA MEMES E MOEDAS CARAS
                    prec = 8 if price < 0.01 else (4 if price < 1 else 2)
                    
                    # ALVOS ESTATÍSTICOS (4, 8, 10%)
                    v4, v8, v10 = price*1.04, price*1.08, price*1.10
                    c4, c8, c10 = price*0.96, price*0.92, price*0.90
                    
                    s_txt = "ESTÁVEL"; s_class = "bg-estavel"
                    if abs(change) >= 10: s_txt = "EXAUSTÃO"; s_class = "bg-exaustao"

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="col-ativo">{display_name}</div>
                            <div class="col-price">
                                {price:.{prec}f}<span style="color:{color_seta};">{seta}</span> 
                                <span style="color:{color_var}; font-size:10px;">({change:+.2f}%)</span>
                            </div>
                            <div style="flex:1; text-align:center; color:#FFFF00; font-size:11px;">{v4:.{prec}f}</div>
                            <div style="flex:1; text-align:center; color:#FFA500; font-size:11px;">{v8:.{prec}f}</div>
                            <div style="flex:1; text-align:center; color:#FF0000; font-size:11px;">{v10:.{prec}f}</div>
                            <div style="flex:1; text-align:center; color:#FFFF00; font-size:11px;">{c4:.{prec}f}</div>
                            <div style="flex:1; text-align:center; color:#FFA500; font-size:11px;">{c8:.{prec}f}</div>
                            <div style="flex:1; text-align:center; color:#00FF00; font-size:11px;">{c10:.{prec}f}</div>
                            <div style="flex:1;"><div class="status-box {s_class}">{s_txt}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
                except:
                    continue
        time.sleep(15)
    except Exception as e:
        time.sleep(10)
