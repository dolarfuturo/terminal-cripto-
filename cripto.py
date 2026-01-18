import streamlit as st
import pandas as pd
import time
import yfinance as yf
import random
import string
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO DE TELA E ESTILO PRETO
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    .stMarkdown h1 { color: #D4AF37 !important; }
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #D4AF37; }
    div[data-testid="stForm"] { background-color: #050505; border: 1px solid #151515; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- GERADOR DE SENHA SIMPLES NA LATERAL ---
with st.sidebar:
    st.markdown("<h3 style='color:#D4AF37;'>GERADOR ALPHA</h3>", unsafe_allow_html=True)
    if st.button("GERAR SENHA NUMÉRICA"):
        senha_simples = ''.join(random.choice(string.digits) for i in range(6))
        st.code(senha_simples)
        st.caption("Copie para o seu Google Sheets.")
    st.markdown("---")
    if st.button("SAIR / LOGOUT"):
        st.session_state.autenticado = False
        st.rerun()

# --- LÓGICA DE LOGIN ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=5)
except:
    st.error("Erro ao conectar com a planilha de usuários.")
    st.stop()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    with st.container():
        left, mid, right = st.columns([1, 2, 1])
        with mid:
            with st.form("login_form"):
                u = st.text_input("USUÁRIO").strip()
                p = st.text_input("SENHA", type="password").strip()
                if st.form_submit_button("LIBERAR ACESSO"):
                    user_row = df_users[df_users['user'].astype(str).str.strip() == str(u)]
                    if not user_row.empty and str(p) == str(user_row.iloc[0]['password']):
                        st.session_state.autenticado = True
                        st.rerun()
                    else: st.error("DADOS INCORRETOS")
    st.stop()

# --- 2. TERMINAL VISÃO DE TUBARÃO (DESIGN REFINADO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    .stApp { font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 32px; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 14px; text-align: center; letter-spacing: 5px; margin-bottom: 10px; }
    .header-container { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 10px; color: #FFFFFF; text-transform: uppercase; text-align: center; font-weight: bold; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 5px 0; border-bottom: 1px solid #151515; }
    .w-ativo { width: 14%; padding-left: 10px; color: #EEE; font-size: 13px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 14px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 13px; font-weight: 800; }
    /* CLASSES DE ALERTA */
    .t-y { background-color: #FFFF00; color: #000 !important; border-radius: 2px; padding: 0px 4px; }
    .t-o { background-color: #FFA500; color: #000 !important; border-radius: 2px; padding: 0px 4px; }
    .t-r { background-color: #FF0000; color: #FFF !important; border-radius: 2px; padding: 0px 4px; animation: blinker 0.4s linear infinite; }
    .t-g { background-color: #00FF00; color: #000 !important; border-radius: 2px; padding: 0px 4px; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    .status-box { padding: 6px 2px; border-radius: 2px; font-weight: 900; font-size: 9px; width: 90%; text-align: center; margin: auto; }
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-yellow { background-color: #FFFF00; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# DICIONÁRIO COMPLETO E SEGURO (MANTIDO 80 ATIVOS)
assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'NEAR-USD':'NEAR/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT',
    'AAVE-USD':'AAVE/USDT','RENDER-USD':'RENDER/USDT','SUI-USD':'SUI/USDT','TIA-USD':'TIA/USDT','INJ-USD':'INJ/USDT',
    'POL-USD':'POL/USDT','SHIB-USD':'SHIB/USDT','LTC-USD':'LTC/USDT','BCH-USD':'BCH/USDT','APT-USD':'APT/USDT',
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
        t_list = list(assets.keys())
        data = yf.download(t_list, period="1d", interval="1m", group_by='ticker', silent=True)
        
        with placeholder.container():
            st.markdown("""<div class="header-container">
                <div class="h-col" style="width:14%; text-align:left; padding-left:10px;">ATIVO</div>
                <div class="h-col" style="width:12%;">PREÇO</div><div class="h-col" style="width:10%;">ALVO 4%</div>
                <div class="h-col" style="width:10%;">ALVO 8%</div><div class="h-col" style="width:10%;">ALVO 10%</div>
                <div class="h-col" style="width:10%;">SUP 4%</div><div class="h-col" style="width:10%;">SUP 8%</div>
                <div class="h-col" style="width:10%;">SUP 10%</div><div class="h-col" style="width:14%;">SINAL</div>
            </div>""", unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    tick_data = data[tid]
                    price = tick_data['Close'].iloc[-1]
                    open_p = tick_data['Open'].iloc[0]
                    change = ((price - open_p) / open_p) * 100
                    
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt, s_class, v4_c, v8_c, v10_c = "ESTÁVEL", "bg-estavel", "", "", ""
                    if price >= v4: s_txt, s_class, v4_c = "DECISÃO ATENÇÃO", "bg-yellow", "t-y"
                    if price >= v8: v8_c = "t-o"
                    if price >= v10: v10_c = "t-r"

                    prec = 6 if price < 0.1 else (4 if price < 10 else 2)
                    
                    st.markdown(f"""<div class="row-container">
                        <div class="w-ativo">{name}</div>
                        <div class="w-price">{price:.{prec}f}<br><span style="font-size:9px;">{change:
