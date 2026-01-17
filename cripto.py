import streamlit as st
import pandas as pd
import time
import yfinance as yf

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    
    .block-container { padding: 0.2rem !important; }
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    .title-gold { color: #D4AF37; font-size: 26px; font-weight: 900; text-align: center; margin: 0; }
    .subtitle-vision { color: #C0C0C0; font-size: 14px; text-align: center; margin-bottom: 5px; letter-spacing: 5px; }
    
    /* CABEÇALHO COLADO */
    .header-container { display: flex; align-items: center; padding: 2px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .col-head { font-size: 7px; flex: 1; text-align: center; font-weight: 800; color: #555; text-transform: uppercase; line-height: 1; margin: 0 -2px; }
    
    /* LINHAS COM NÚMEROS BRUTAIS */
    .row-container { display: flex; align-items: center; padding: 1px 0; border-bottom: 1px solid #151515; gap: 0px !important; }
    .col-ativo { color: #AAA; font-size: 10px; flex: 0.8; font-weight: 400; padding-left: 5px; white-space: nowrap; }
    .col-price { color: #FF8C00; font-weight: 900; font-size: 16px !important; flex: 1.3; text-align: center; line-height: 1; margin: 0 -5px; }
    
    /* ALVOS GIGANTES E COLADOS */
    .col-target { flex: 1; text-align: center; font-size: 16px !important; font-weight: 900 !important; margin: 0 -3px; letter-spacing: -1px; }
    .col-sinal { flex: 1.4; padding: 0 2px; }

    /* ESTILOS DE ATIVAÇÃO */
    .target-yellow { background-color: #FFFF00; color: #000 !important; border-radius: 0px; }
    .target-orange { background-color: #FFA500; color: #000 !important; border-radius: 0px; }
    .target-blink-red { background-color: #FF0000; color: #FFF !important; animation: blinker 0.4s linear infinite; border-radius: 0px; }
    .target-blink-green { background-color: #00FF00; color: #000 !important; animation: blinker 0.4s linear infinite; border-radius: 0px; }
    
    @keyframes blinker { 50% { opacity: 0.1; } }

    .status-box { padding: 8px 1px; border-radius: 1px; font-weight: 900; font-size: 8px; width: 100%; text-align: center; line-height: 1; text-transform: uppercase; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-yellow { background-color: #FFFF00; color: #000; }
    .bg-orange { background-color: #FFA500; color: #000; }
    .bg-ex-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .bg-ex-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    </style>
    """, unsafe_allow_html=True)

assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'NEAR-USD':'NEAR/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT',
    'AAVE-USD':'AAVE/USDT','RENDER-USD':'RENDER/USDT','SUI-USD':'SUI/USDT','TIA-USD':'TIA/USDT','INJ-USD':'INJ/USDT'
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
                    <div class="col-head" style="flex:0.8; text-align:left; padding-left:5px;">ATIVO</div>
                    <div class="col-head" style="flex:1.3;">PREÇO ATUAL</div>
                    <div class="col-head">RESIST</div>
                    <div class="col-head">TOPO</div>
                    <div class="col-head">TETO</div>
                    <div class="col-head">SUPORTE</div>
                    <div class="col-head">FUNDO</div>
                    <div class="col-head">CHÃO</div>
                    <div class="col-head" style="flex:1.4;">ALERTA OPERACIONAL</div>
                </div>
                """, unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    info = tickers.tickers[tid].fast_info
                    price = info.last_price
                    open_p = info.open
                    if price is None: continue
                    
                    change = ((price - open_p) / open_p) * 100
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt = "ESTÁVEL"; s_class = "bg-estavel"
                    v4_c, v8_c, v10_c, c4_c, c8_c, c10_c = "", "", "", "", "", ""

                    if price >= v10:
                        s_txt = "EXAUSTÃO"; s_class = "bg-ex-red"; v10_c = "target-blink-red"
                    elif price >= v8:
                        s_txt = "CUIDADO ALTA VOL"; s_class = "bg-orange"; v8_c = "target-orange"
                    elif price >= v4:
                        s_txt = "PONTO DECISAO ATENÇÃO"; s_class = "bg-yellow"; v4_c = "target-yellow"
                    elif price <= c10:
                        s_txt = "EXAUSTÃO"; s_class = "bg-ex-green"; c10_c = "target-blink-green"
                    elif price <= c8:
                        s_txt = "CUIDADO ALTA VOL"; s_class = "bg-orange"; c8_c = "target-orange"
                    elif price <= c4:
                        s_txt = "PONTO DECISAO ATENÇÃO"; s_class = "bg-yellow"; c4_c = "target-yellow"

                    prec = 6 if price < 0.1 else (4 if price < 10 else 2)
                    seta = '▲' if price >= open_p else '▼'
                    seta_c = '#00FF00' if price >= open_p else '#FF0000'

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="col-ativo">{name}</div>
                            <div class="col-price">
                                {price:.{prec}f}<br><span style="font-size:8px; color:{seta_c};">{seta}{change:+.2f}%</span>
                            </div>
                            <div class="col-target" style="color:#FFFF00;"><span class="{v4_c}">{v4:.{prec}f}</span></div>
                            <div class="col-target" style="color:#FFA500;"><span class="{v8_c}">{v8:.{prec}f}</span></div>
                            <div class="col-target" style="color:#FF0000;"><span class="{v10_c}">{v10:.{prec}f}</span></div>
                            <div class="col-target" style="color:#FFFF00;"><span class="{c4_c}">{c4:.{prec}f}</span></div>
                            <div class="col-target" style="color:#FFA500;"><span class="{c8_c}">{c8:.{prec}f}</span></div>
                            <div class="col-target" style="color:#00FF00;"><span class="{c10_c}">{c10:.{prec}f}</span></div>
                            <div class="col-sinal"><div class="status-box {s_class}">{s_txt}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
                except: continue
        time.sleep(10)
    except: time.sleep(10)
