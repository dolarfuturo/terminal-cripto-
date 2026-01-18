import streamlit as st
import pandas as pd
import time
import yfinance as yf
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO DE INTERFACE ALPHA VISION
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide", initial_sidebar_state="collapsed")

# ESTILO CSS ORIGINAL (PRETO, DOURADO E ALERTAS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    header, footer { visibility: hidden; }
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    /* Login Style */
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    .stMarkdown h1 { color: #D4AF37 !important; }
    div[data-testid="stForm"] { background-color: #050505; border: 1px solid #151515; border-radius: 5px; }

    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; padding-top: 10px; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 16px; text-align: center; margin-top: -5px; letter-spacing: 7px; margin-bottom: 15px; font-weight: 700; }
    
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 11px; font-weight: 400; color: #FFFFFF; text-transform: uppercase; text-align: center; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; gap: 0px; }
    .w-ativo { width: 14%; text-align: left; padding-left: 10px; color: #EEE; font-size: 14px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 14px; font-weight: 800; }
    .w-sinal { width: 14%; text-align: center; padding-right: 5px; }

    /* CLASSES DE ESTADO E ALERTAS */
    .t-active { border-radius: 2px; padding: 2px 4px; }
    .t-y { background-color: #FFFF00; color: #000 !important; border-radius: 2px; }
    .t-o { background-color: #FFA500; color: #000 !important; border-radius: 2px; }
    .t-blink-r { background-color: #FF0000; color: #FFF !important; animation: blinker 0.4s linear infinite; border-radius: 2px; }
    .t-blink-g { background-color: #00FF00; color: #000 !important; animation: blinker 0.4s linear infinite; border-radius: 2px; }
    .t-purple { background-color: #8A2BE2; color: #FFF !important; font-weight: 900; border-radius: 2px; }
    
    @keyframes blinker { 50% { opacity: 0.2; } }

    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 9px; width: 100%; text-align: center; text-transform: uppercase; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-yellow { background-color: #FFFF00; color: #000; }
    .bg-orange { background-color: #FFA500; color: #000; }
    .bg-blink-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .bg-blink-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    .bg-purple { background-color: #8A2BE2; color: #FFF; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÃO COM A PLANILHA (BLINDADA)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=15)
    df_users.columns = df_users.columns.str.strip().str.lower()
except:
    st.error("Erro de conexão com o banco de dados de usuários.")
    st.stop()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

# 3. LOGIN COM TRAVA DE STATUS
if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    left, mid, right = st.columns([1, 2, 1])
    with mid:
        with st.form("login_form"):
            u = st.text_input("USUÁRIO").strip()
            p = st.text_input("SENHA", type="password").strip()
            if st.form_submit_button("LIBERAR ACESSO"):
                user_match = df_users[df_users['user'].astype(str) == u]
                if not user_match.empty:
                    if str(p) == str(user_match.iloc[0]['password']):
                        # VERIFICAÇÃO DO STATUS NA PLANILHA
                        status_val = str(user_match.iloc[0].get('status', 'ativo')).strip().lower()
                        if status_val == 'ativo':
                            st.session_state.autenticado = True
                            st.rerun()
                        else:
                            st.error("🚫 ACESSO BLOQUEADO OU EXPIRADO.")
                    else: st.error("Senha incorreta.")
                else: st.error("Usuário não encontrado.")
        st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>Sinal caído ou instável? Fale com o suporte.</p>", unsafe_allow_html=True)
    st.stop()

# 4. LISTA DOS 80 ATIVOS
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
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO • RESET 00:00 UTC</div>', unsafe_allow_html=True)

placeholder = st.empty()

# 5. LOOP PRINCIPAL COM RESET 00:00 UTC
while True:
    try:
        # Puxa dados em lote para performance
        data_batch = yf.download(list(assets.keys()), period="1d", interval="1m", group_by='ticker', silent=True)
        
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

            for
