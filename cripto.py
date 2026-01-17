import streamlit as st
import pandas as pd
import time
import yfinance as yf

st.set_page_config(page_title="ALPHA VISION", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 0rem !important; }
    header {visibility: hidden;}
    .stApp { background-color: #000000; font-family: monospace; }
    .row-container { display: flex; width: 100%; align-items: center; border-bottom: 1px solid #151515; padding: 5px 0; }
    .w-col { flex: 1; text-align: center; font-size: 13px; color: #EEE; }
    .blink-red { background-color: #FF0000; color: white; animation: blinker 0.4s linear infinite; padding: 5px; border-radius: 2px; }
    .blink-green { background-color: #00FF00; color: black; animation: blinker 0.4s linear infinite; padding: 5px; border-radius: 2px; }
    .bg-purple { background-color: #8A2BE2; color: white; padding: 5px; border-radius: 2px; font-weight: bold; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'NEAR-USD':'NEAR/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT',
    'AAVE-USD':'AAVE/USDT','RENDER-USD':'RENDER/USDT','SUI-USD':'SUI/USDT','TIA-USD':'TIA/USDT','INJ-USD':'INJ/USDT',
    'MATIC-USD':'POL/USDT','SHIB-USD':'SHIB/USDT','LTC-USD':'LTC/USDT','BCH-USD':'BCH/USDT','APT-USD':'APT/USDT',
    'STX-USD':'STX/USDT','KAS-USD':'KAS/USDT','ARB-USD':'ARB/USDT','OP-USD':'OP/USDT','SEI-USD':'SEI/USDT',
    'FIL-USD':'FIL/USDT','HBAR-USD':'HBAR/USDT','ETC-USD':'ETC/USDT','ICP-USD':'ICP/USDT','BONK-USD':'BONK/USDT',
    'FLOKI-USD':'FLOKI/USDT','WIF-USD':'WIF/USDT','PYTH-USD':'PYTH/USDT','JUP-USD':'JUP/USDT','RAY-USD':'RAY/USDT',
    'ORDI-USD':'ORDI/USDT','BEAM-USD':'BEAM/USDT','IMX-USD':'IMX/USDT','GNS-USD':'GNS/USDT','DYDX-USD':'DYDX/USDT',
    'LDO-USD':'LDO/USDT','PENDLE-USD':'PENDLE/USDT','ENA-USD':'ENA/USDT','TRX-USD':'TRX/USDT','ATOM-USD':'ATOM/USDT',
    'MKR-USD':'MKR/USDT','GRT-USD':'GRT/USDT','THETA-USD':'THETA/USDT','FTM-USD':'FTM/USDT','VET-USD':'VET/USDT',
    'ALGO-USD':'ALGO/USDT','FLOW-USD':'FLOW/USDT','QNT-USD':'QNT/USDT','SNX-USD':'SNX/USDT','EOS-USD':'EOS/USDT',
    'NEO-USD':'NEO/USDT','IOTA-USD':'IOTA/USDT','CFX-USD':'CFX/USDT','AXS-USD':'AXS/USDT','MANA-USD':'MANA/USDT',
    'SAND-USD':'SAND/USDT','APE-USD':'APE/USDT','RUNE-USD':'RUNE/USDT','CHZ-USD':'CHZ/USDT','MINA-USD':'MINA/USDT',
    'ROSE-USD':'ROSE/USDT','WOO-USD':'WOO/USDT','ANKR-USD':'ANKR/USDT','1INCH-USD':'1INCH/USDT','ZIL-USD':'ZIL/USDT',
    'LRC-USD':'LRC/USDT','CRV-USD':'CRV/USDT'
}

placeholder = st.empty()

while True:
    try:
        tickers = yf.Tickers(' '.join(assets.keys()))
        with placeholder.container():
            st.write("### ALPHA VISION CRYPTO")
            for tid, name in assets.items():
                try:
                    info = tickers.tickers[tid].fast_info
                    p, o = info.last_price, info.open
                    var = ((p - o) / o) * 100
                    
                    s_txt, s_class = "ESTÁVEL", ""
                    if var >= 15: s_txt, s_class = "ALTA PARABÓLICA", "bg-purple"
                    elif var >= 10: s_txt, s_class = "EXAUSTÃO MÁXIMA", "blink-red"
                    elif var <= -15: s_txt, s_class = "QUEDA PARABÓLICA", "bg-purple"
                    elif var <= -10: s_txt, s_class = "EXAUSTÃO MÁXIMA", "blink-green"

                    st.markdown(f'''
                        <div class="row-container">
                            <div class="w-col">{name}</div>
                            <div class="w-col">{p:.4f}</div>
                            <div class="w-col">{var:+.2f}%</div>
                            <div class="w-col"><span class="{s_class}">{s_txt}</span></div>
                        </div>
                    ''', unsafe_allow_html=True)
                except: continue
        time.sleep(10)
    except: time.sleep(10)
