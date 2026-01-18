import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. LOGIN COM FUNDO PRETO
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    .stMarkdown h1 { color: #D4AF37 !important; }
    label { color: #C0C0C0 !important; }
    div[data-testid="stForm"] { background-color: #050505; border: 1px solid #151515; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=10)
except:
    st.error("Erro de conexão com a base de dados.")
    st.stop()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    with st.container():
        left, mid, right = st.columns([1, 2, 1])
        with mid:
            with st.form("login_form"):
                u = st.text_input("USUÁRIO")
                p = st.text_input("SENHA", type="password")
                if st.form_submit_button("LIBERAR ACESSO"):
                    user_row = df_users[df_users['user'] == u]
                    if not user_row.empty and str(p) == str(user_row.iloc[0]['password']):
                        st.session_state.autenticado = True
                        st.rerun()
                    else: st.error("Acesso negado.")
    st.stop()

# 2. TERMINAL VISÃO DE TUBARÃO (80 ATIVOS + CORES ORIGINAIS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; padding-top: 10px; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 16px; text-align: center; margin-top: -5px; letter-spacing: 7px; margin-bottom: 15px; font-weight: 700; }
    
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 11px; font-weight: 400; color: #FFFFFF; text-transform: uppercase; text-align: center; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; gap: 0px; }
    .w-ativo { width: 14%; text-align: left; padding-left: 10px; color: #EEE; font-size: 14px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 14px; font-weight: 800; }
    .w-sinal { width: 14%; text-align: center; padding-right: 5px; }

    /* ESTILO PARA PINTAR O FUNDO DOS NÚMEROS QUANDO ATINGE ALERTA */
    .t-y { background-color: #FFFF00; color: #000 !important; border-radius: 2px; padding: 1px 3px; }
    .t-o { background-color: #FFA500; color: #000 !important; border-radius: 2px; padding: 1px 3px; }
    .t-r { background-color: #FF0000; color: #FFF !important; border-radius: 2px; padding: 1px 3px; animation: blinker 0.4s linear infinite; }
    .t-g { background-color: #00FF00; color: #000 !important; border-radius: 2px; padding: 1px 3px; animation: blinker 0.4s linear infinite; }
    .t-p { background-color: #8A2BE2; color: #FFF !important; border-radius: 2px; padding: 1px 3px; }
    
    @keyframes blinker { 50% { opacity: 0.3; } }

    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 9px; width: 100%; text-align: center; text-transform: uppercase; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-yellow { background-color: #FFFF00; color: #000; }
    .bg-orange { background-color: #FFA500; color: #000; }
    .bg-blink-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .bg-blink-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    .bg-purple { background-color: #8A2BE2; color: #FFF; }
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

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        tickers = yf.Tickers(' '.join(assets.keys()))
        with placeholder.container():
            st.markdown("""
                <div class="header-container">
                    <div class="h-col" style="width:14%; text-align:left; padding-left:10px;">ATIVO</div>
                    <div class="h-col" style="width:12%;">PREÇO ATUAL</div>
                    <div class="h-col" style="width:10%;">RESISTÊNCIA</div>
                    <div class="h-col" style="width:10%;">PRÓX AO TOPO</div>
                    <div class="h-col" style="width:10%;">TETO EXAUSTÃO</div>
                    <div class="h-col" style="width:10%;">SUPORTE</div>
                    <div class="h-col" style="width:10%;">PRÓX FUNDO</div>
                    <div class="h-col" style="width:10%;">CHÃO EXAUSTÃO</div>
                    <div class="h-col" style="width:14%;">SINALIZADOR</div>
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
                    
                    s_txt, s_class = "ESTÁVEL", "bg-estavel"
                    v4_c, v8_c, v10_c, c4_c, c8_c, c10_c = "", "", "", "", "", ""

                    if change >= 15: s_txt, s_class, v10_c = "ALTA PARABÓLICA", "bg-purple", "t-p"
                    elif change >= 10: s_txt, s_class, v10_c = "EXAUSTÃO MÁXIMA", "bg-blink-red", "t-r"
                    elif price >= v8: s_txt, s_class, v8_c = "CUIDADO ALTA VOL", "bg-orange", "t-o"
                    elif price >= v4: s_txt, s_class, v4_c = "DECISÃO ATENÇÃO", "bg-yellow", "t-y"
                    elif change <= -15: s_txt, s_class, c10_c = "QUEDA PARABÓLICA", "bg-purple", "t-p"
                    elif change <= -10: s_txt, s_class, c10_c = "EXAUSTÃO MÁXIMA", "bg-blink-green", "t-g"
                    elif price <= c8: s_txt, s_class, c8_c = "CUIDADO ALTA VOL", "bg-orange", "t-o"
                    elif price <= c4: s_txt, s_class, c4_c = "DECISÃO ATENÇÃO", "bg-yellow", "t-y"

                    prec = 6 if price < 0.1 else (4 if price < 10 else 2)
                    seta = '▲' if price >= open_p else '▼'
                    seta_c = '#00FF00' if price >= open_p else '#FF0000'

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="w-ativo">{name}</div>
                            <div class="w-price">{price:.{prec}f}<br><span style="font-size:9px; color:{seta_c};">{seta}{change:+.2f}%</span></div>
                            <div class="w-target" style="color:#FFFF00;"><span class="{v4_c}">{v4:.{prec}f}</span></div>
                            <div class="w-target" style="color:#FFA500;"><span class="{v8_c}">{v8:.{prec}f}</span></div>
                            <div class="w-target" style="color:#FF0000;"><span class="{v10_c}">{v10:.{prec}f}</span></div>
                            <div class="w-target" style="color:#FFFF00;"><span class="{c4_c}">{c4:.{prec}f}</span></div>
                            <div class="w-target" style="color:#FFA500;"><span class="{c8_c}">{c8:.{prec}f}</span></div>
                            <div class="w-target" style="color:#00FF00;"><span class="{c10_c}">{c10:.{prec}f}</span></div>
                            <div class="w-sinal"><div class="status-box {s_class}">{s_txt}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
                except: continue
        time.sleep(10)
    except: time.sleep(10)
