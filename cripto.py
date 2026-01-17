import streamlit as st
import pandas as pd
import time
import yfinance as yf

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# CSS ESTILO TERMINAL - FOCO TOTAL NOS ALVOS VIVOS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 40px; font-weight: 700; text-align: center; margin: 0; text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.6); }
    .subtitle-vision { color: #C0C0C0; font-size: 18px; text-align: center; margin-top: -5px; letter-spacing: 8px; margin-bottom: 20px; }
    .header-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .col-head { font-size: 9px; flex: 1; text-align: center; font-weight: 800; color: #BBB; text-transform: uppercase; }
    .row-container { display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 13px; flex: 1.2; font-weight: 700; padding-left: 10px; }
    .col-price { color: #FF8C00; font-weight: 800; font-size: 14px; flex: 1.5; text-align: center; }
    
    /* CLASSES DE SINALIZAÇÃO NOS ALVOS */
    .target-on-yellow { color: #000 !important; background-color: #FFFF00; font-weight: 900 !important; border-radius: 2px; }
    .target-on-orange { color: #000 !important; background-color: #FFA500; font-weight: 900 !important; border-radius: 2px; }
    .target-blink-red { color: #FFF !important; background-color: #FF0000; animation: blinker 0.4s linear infinite; font-weight: 900 !important; border-radius: 2px; }
    .target-blink-green { color: #000 !important; background-color: #00FF00; animation: blinker 0.4s linear infinite; font-weight: 900 !important; border-radius: 2px; }
    
    @keyframes blinker { 50% { opacity: 0.0; } }

    .status-box { padding: 4px; border-radius: 4px; font-weight: 800; font-size: 9px; width: 95%; margin: auto; text-align: center; color: white; }
    .bg-estavel { background-color: #111; color: #555; border: 1px solid #333; } 
    .bg-decisao { background-color: #FFFF00; color: #000; } 
    .bg-topo-fundo { background-color: #FFA500; color: #000; } 
    .bg-exaust-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .bg-exaust-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    </style>
    """, unsafe_allow_html=True)

# LISTA DE ATIVOS
assets = {
    'BTC-USD': 'BTC/USDT', 'ETH-USD': 'ETH/USDT', 'SOL-USD': 'SOL/USDT', 'BNB-USD': 'BNB/USDT', 
    'XRP-USD': 'XRP/USDT', 'DOGE-USD': 'DOGE/USDT', 'ADA-USD': 'ADA/USDT', 'AVAX-USD': 'AVAX/USDT', 
    'GALA-USD': 'GALA/USDT', 'PEPE-USD': 'PEPE/USDT', 'EGLD-USD': 'EGLD/USDT', 'SUI-USD': 'SUI/USDT'
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
                    <div class="col-head" style="flex:1.5;">PREÇO ATUAL</div>
                    <div class="col-head">PONTO DECISÃO</div>
                    <div class="col-head">PRÓX TOPO</div>
                    <div class="col-head">TETO EXAUSTÃO</div>
                    <div class="col-head">SUPORTE</div>
                    <div class="col-head">FUNDO</div>
                    <div class="col-head">CHÃO EXAUSTÃO</div>
                    <div class="col-head">SINALIZADOR</div>
                </div>
                """, unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    info = tickers.tickers[tid].fast_info
                    price = info.last_price
                    open_p = info.open
                    if price is None or open_p is None: continue
                    
                    # Definição Estática dos Alvos (VWAP 00:00)
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    # Classes de Estilo das Colunas de Alvo
                    s_txt = "MONITORANDO"; s_class = "bg-estavel"
                    v4_s, v8_s, v10_s, c4_s, c8_s, c10_s = "", "", "", "", "", ""

                    # LÓGICA DE ATIVAÇÃO DOS ALVOS
                    if price >= v10:
                        s_txt = "EXAUSTÃO ALTA"; s_class = "bg-exaust-red"; v10_s = "target-blink-red"
                    elif price >= v8:
                        s_txt = "ZONA DE TOPO"; s_class = "bg-topo-fundo"; v8_s = "target-on-orange"
                    elif price >= v4:
                        s_txt = "DECISÃO ALTA"; s_class = "bg-decisao"; v4_s = "target-on-yellow"
                    elif price <= c10:
                        s_txt = "EXAUSTÃO BAIXA"; s_class = "bg-exaust-green"; c10_s = "target-blink-green"
                    elif price <= c8:
                        s_txt = "ZONA DE FUNDO"; s_class = "bg-topo-fundo"; c8_s = "target-on-orange"
                    elif price <= c4:
                        s_txt = "DECISÃO BAIXA"; s_class = "bg-decisao"; c4_s = "target-on-yellow"

                    prec = 8 if price < 0.01 else (4 if price < 1 else 2)
                    seta = '▲' if price >= open_p else '▼'
                    seta_c = '#00FF00' if price >= open_p else '#FF0000'

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="col-ativo">{name}</div>
                            <div class="col-price">{price:.{prec}f} <span style="color:{seta_c}; font-size:10px;">{seta}</span></div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#FFFF00;"><span class="{v4_s}">{v4:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#FFA500;"><span class="{v8_s}">{v8:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#FF0000;"><span class="{v10_s}">{v10:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#FFFF00;"><span class="{c4_s}">{c4:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#FFA500;"><span class="{c8_s}">{c8:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#00FF00;"><span class="{c10_s}">{c10:.{prec}f}</span></div>
                            <div style="flex:1;"><div class="status-box {s_class}">{s_txt}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: time.sleep(10)
