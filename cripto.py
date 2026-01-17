import streamlit as st
import pandas as pd
import time
import yfinance as yf

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# CSS ESTILO TERMINAL ALPHA VISION - COMANDOS REAIS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 35px; font-weight: 700; text-align: center; margin: 0; text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.6); }
    .subtitle-vision { color: #C0C0C0; font-size: 14px; text-align: center; margin-top: -5px; letter-spacing: 5px; margin-bottom: 20px; }
    .header-container { display: flex; align-items: center; padding: 10px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .col-head { font-size: 8px; flex: 1; text-align: center; font-weight: 800; color: #BBB; text-transform: uppercase; }
    .row-container { display: flex; align-items: center; padding: 6px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 12px; flex: 1.2; font-weight: 700; padding-left: 10px; }
    .col-price { color: #FF8C00; font-weight: 800; font-size: 13px; flex: 1.5; text-align: center; }
    
    /* ALVOS ATIVOS */
    .target-yellow { background-color: #FFFF00; color: #000 !important; font-weight: 900 !important; border-radius: 3px; padding: 2px 4px; }
    .target-orange { background-color: #FFA500; color: #000 !important; font-weight: 900 !important; border-radius: 3px; padding: 2px 4px; }
    .target-blink-red { background-color: #FF0000; color: #FFF !important; animation: blinker 0.4s linear infinite; font-weight: 900 !important; border-radius: 3px; padding: 2px 4px; }
    .target-blink-green { background-color: #00FF00; color: #000 !important; animation: blinker 0.4s linear infinite; font-weight: 900 !important; border-radius: 3px; padding: 2px 4px; }
    
    @keyframes blinker { 50% { opacity: 0.1; } }

    .status-box { padding: 4px; border-radius: 4px; font-weight: 800; font-size: 8px; width: 95%; margin: auto; text-align: center; color: white; }
    .bg-monitor { background-color: #111; color: #444; border: 1px solid #222; }
    .bg-yellow { background-color: #FFFF00; color: #000; }
    .bg-orange { background-color: #FFA500; color: #000; }
    .bg-ex-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .bg-ex-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    </style>
    """, unsafe_allow_html=True)

# LISTA DE ATIVOS
assets = {
    'BTC-USD': 'BTC/USDT', 'ETH-USD': 'ETH/USDT', 'SOL-USD': 'SOL/USDT', 'BNB-USD': 'BNB/USDT', 
    'XRP-USD': 'XRP/USDT', 'DOGE-USD': 'DOGE/USDT', 'ADA-USD': 'ADA/USDT', 'AVAX-USD': 'AVAX/USDT', 
    'GALA-USD': 'GALA/USDT', 'EGLD-USD': 'EGLD/USDT', 'NEAR-USD': 'NEAR/USDT', 'PEPE-USD': 'PEPE/USDT'
}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">TERMINAL DE COMANDO INSTITUCIONAL</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        tickers = yf.Tickers(' '.join(assets.keys()))
        with placeholder.container():
            st.markdown("""
                <div class="header-container">
                    <div class="col-head" style="flex:1.2;">ATIVO</div>
                    <div class="col-head" style="flex:1.5;">PREÇO ATUAL (VAR%)</div>
                    <div class="col-head" style="color:#FFFF00;">RESISTÊNCIA</div>
                    <div class="col-head" style="color:#FFA500;">PRÓX AO TOPO</div>
                    <div class="col-head" style="color:#FF0000;">TETO EXAUSTÃO</div>
                    <div class="col-head" style="color:#FFFF00;">SUPORTE</div>
                    <div class="col-head" style="color:#FFA500;">PRÓX FUNDO</div>
                    <div class="col-head" style="color:#00FF00;">CHÃO EXAUSTÃO</div>
                    <div class="col-head">ALERTA OPERACIONAL</div>
                </div>
                """, unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    info = tickers.tickers[tid].fast_info
                    price = info.last_price
                    open_p = info.open
                    if price is None or open_p is None: continue
                    
                    change = ((price - open_p) / open_p) * 100
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt = "AGUARDANDO SINAL"; s_class = "bg-monitor"
                    v4_c, v8_c, v10_c, c4_c, c8_c, c10_c = "", "", "", "", "", ""

                    # ALTA
                    if price >= v10:
                        s_txt = "EXAUSTÃO"; s_class = "bg-ex-red"; v10_c = "target-blink-red"
                    elif price >= v8:
                        s_txt = "CUIDADO ALTA VOL"; s_class = "bg-orange"; v8_c = "target-orange"
                    elif price >= v4:
                        s_txt = "PONTO DECISAO ATENÇÃO"; s_class = "bg-yellow"; v4_c = "target-yellow"
                    # BAIXA
                    elif price <= c10:
                        s_txt = "EXAUSTÃO"; s_class = "bg-ex-green"; c10_c = "target-blink-green"
                    elif price <= c8:
                        s_txt = "CUIDADO ALTA VOL"; s_class = "bg-orange"; c8_c = "target-orange"
                    elif price <= c4:
                        s_txt = "PONTO DECISAO ATENÇÃO"; s_class = "bg-yellow"; c4_c = "target-yellow"

                    prec = 8 if price < 0.01 else (4 if price < 1 else 2)
                    seta = '▲' if price >= open_p else '▼'
                    seta_c = '#00FF00' if price >= open_p else '#FF0000'

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="col-ativo">{name}</div>
                            <div class="col-price">
                                {price:.{prec}f} <span style="font-size:9px; color:{seta_c};">({change:+.2f}%)</span>
                            </div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#FFFF00;"><span class="{v4_c}">{v4:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#FFA500;"><span class="{v8_c}">{v8:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#FF0000;"><span class="{v10_c}">{v10:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#FFFF00;"><span class="{c4_c}">{c4:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#FFA500;"><span class="{c8_c}">{c8:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:11px; color:#00FF00;"><span class="{c10_c}">{c10:.{prec}f}</span></div>
                            <div style="flex:1;"><div class="status-box {s_class}">{s_txt}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: time.sleep(10)
