import streamlit as st
import pandas as pd
import time
import yfinance as yf

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 28px; font-weight: 800; text-align: center; margin: 0; }
    .header-container { display: flex; align-items: center; padding: 5px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .col-head { font-size: 8px; flex: 1; text-align: center; font-weight: 800; color: #999; text-transform: uppercase; line-height: 1;}
    .row-container { display: flex; align-items: center; padding: 3px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 11px; flex: 1.2; font-weight: 700; padding-left: 5px; }
    .col-price { color: #FF8C00; font-weight: 800; font-size: 11px; flex: 1.5; text-align: center; }
    
    /* ALVOS ATIVOS */
    .target-yellow { background-color: #FFFF00; color: #000 !important; font-weight: 900; border-radius: 2px; padding: 0 3px; }
    .target-orange { background-color: #FFA500; color: #000 !important; font-weight: 900; border-radius: 2px; padding: 0 3px; }
    .target-blink-red { background-color: #FF0000; color: #FFF !important; animation: blinker 0.4s linear infinite; font-weight: 900; border-radius: 2px; padding: 0 3px; }
    .target-blink-green { background-color: #00FF00; color: #000 !important; animation: blinker 0.4s linear infinite; font-weight: 900; border-radius: 2px; padding: 0 3px; }
    
    @keyframes blinker { 50% { opacity: 0.1; } }

    .status-box { padding: 2px; border-radius: 3px; font-weight: 800; font-size: 8px; width: 98%; margin: auto; text-align: center; color: white; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-yellow { background-color: #FFFF00; color: #000; }
    .bg-orange { background-color: #FFA500; color: #000; }
    .bg-ex-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .bg-ex-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    </style>
    """, unsafe_allow_html=True)

# LISTA EXPANDIDA
assets = {
    'BTC-USD':'BTC','ETH-USD':'ETH','SOL-USD':'SOL','BNB-USD':'BNB','XRP-USD':'XRP','DOGE-USD':'DOGE',
    'ADA-USD':'ADA','AVAX-USD':'AVAX','SHIB-USD':'SHIB','DOT-USD':'DOT','LINK-USD':'LINK','TRX-USD':'TRX',
    'NEAR-USD':'NEAR','MATIC-USD':'POL','PEPE-USD':'PEPE','LTC-USD':'LTC','BCH-USD':'BCH','APT-USD':'APT',
    'SUI-USD':'SUI','EGLD-USD':'EGLD','GALA-USD':'GALA','FET-USD':'FET','RENDER-USD':'RENDER','TIA-USD':'TIA',
    'HBAR-USD':'HBAR','ATOM-USD':'ATOM','INJ-USD':'INJ','AAVE-USD':'AAVE','OP-USD':'OP','ARB-USD':'ARB'
}

st.markdown('<div class="title-gold">ALPHA VISION</div>', unsafe_allow_html=True)
placeholder = st.empty()

while True:
    try:
        tickers = yf.Tickers(' '.join(assets.keys()))
        with placeholder.container():
            st.markdown("""
                <div class="header-container">
                    <div class="col-head" style="flex:1.2;">ATIVO</div>
                    <div class="col-head" style="flex:1.5;">PREÇO (VAR%)</div>
                    <div class="col-head">RESIST</div>
                    <div class="col-head">PRÓX TOPO</div>
                    <div class="col-head">TETO EXAUST</div>
                    <div class="col-head">SUPORTE</div>
                    <div class="col-head">PRÓX FUNDO</div>
                    <div class="col-head">CHÃO EXAUST</div>
                    <div class="col-head">SINAL</div>
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
                    
                    s_txt = "MONITORANDO"; s_class = "bg-estavel"
                    v4_c, v8_c, v10_c, c4_c, c8_c, c10_c = "", "", "", "", "", ""

                    if price >= v10:
                        s_txt = "EXAUSTÃO"; s_class = "bg-ex-red"; v10_c = "target-blink-red"
                    elif price >= v8:
                        s_txt = "CUIDADO VOL"; s_class = "bg-orange"; v8_c = "target-orange"
                    elif price >= v4:
                        s_txt = "DECISÃO ATENÇÃO"; s_class = "bg-yellow"; v4_c = "target-yellow"
                    elif price <= c10:
                        s_txt = "EXAUSTÃO"; s_class = "bg-ex-green"; c10_c = "target-blink-green"
                    elif price <= c8:
                        s_txt = "CUIDADO VOL"; s_class = "bg-orange"; c8_c = "target-orange"
                    elif price <= c4:
                        s_txt = "DECISÃO ATENÇÃO"; s_class = "bg-yellow"; c4_c = "target-yellow"

                    prec = 6 if price < 0.1 else (4 if price < 10 else 2)
                    seta = '▲' if price >= open_p else '▼'
                    seta_c = '#00FF00' if price >= open_p else '#FF0000'

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="col-ativo">{name}</div>
                            <div class="col-price">{price:.{prec}f}<br><span style="font-size:8px; color:{seta_c};">{seta} {change:+.2f}%</span></div>
                            <div style="flex:1; text-align:center; font-size:9px; color:#FFFF00;"><span class="{v4_c}">{v4:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:9px; color:#FFA500;"><span class="{v8_c}">{v8:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:9px; color:#FF0000;"><span class="{v10_c}">{v10:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:9px; color:#FFFF00;"><span class="{c4_c}">{c4:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:9px; color:#FFA500;"><span class="{c8_c}">{c8:.{prec}f}</span></div>
                            <div style="flex:1; text-align:center; font-size:9px; color:#00FF00;"><span class="{c10_c}">{c10:.{prec}f}</span></div>
                            <div style="flex:1;"><div class="status-box {s_class}">{s_txt}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: time.sleep(10)
