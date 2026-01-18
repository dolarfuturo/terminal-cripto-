import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO ALPHA VISION
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide", initial_sidebar_state="collapsed")

# ESTILO VISUAL (FUNDO PRETO E DOURADO)
st.markdown("""
    <style>
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    header, footer { visibility: hidden; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    .stMarkdown h1 { color: #D4AF37 !important; }
    label { color: #C0C0C0 !important; }
    div[data-testid="stForm"] { background-color: #050505; border: 1px solid #151515; border-radius: 5px; }
    
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; padding-top: 10px; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 14px; text-align: center; margin-top: -5px; letter-spacing: 5px; margin-bottom: 15px; font-weight: 700; }
    
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 10px; font-weight: 700; color: #FFFFFF; text-transform: uppercase; text-align: center; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; }
    .w-ativo { width: 14%; text-align: left; padding-left: 10px; color: #EEE; font-size: 14px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 13px; font-weight: 800; }
    .w-sinal { width: 14%; text-align: center; padding-right: 5px; }

    /* ESTILO DE ALERTAS */
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

# 2. CONEXÃO E LEITURA (BLINDADA)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=10)
    # Garante que as colunas lidas sejam strings e limpas de espaços
    df_users.columns = df_users.columns.str.strip().str.lower()
except:
    st.error("Erro na base de dados. Tente atualizar a página.")
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
                        # Verifica se a coluna status existe
                        if 'status' in user_match.columns:
                            s_val = str(user_match.iloc[0]['status']).strip().lower()
                            if s_val == 'ativo':
                                st.session_state.autenticado = True
                                st.rerun()
                            else:
                                st.error("Acesso bloqueado. Fale com o suporte.")
                        else:
                            # Se você esqueceu de criar a coluna, ele deixa passar para não dar tela preta
                            st.session_state.autenticado = True
                            st.rerun()
                    else: st.error("Senha incorreta.")
                else: st.error("Usuário não encontrado.")
        st.caption("Dúvida ou erro de sinal? Fale com o suporte.")
    st.stop()

# 4. TERMINAL (80 ATIVOS + RESET BINANCE 00:00 UTC)
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
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO • AUTOMATIC RESET 00:00 UTC</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
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

            for tid, name in assets.items():
                try:
                    df_ticker = data_batch[tid]
                    price = df_ticker['Close'].iloc[-1]
                    open_p = df_ticker['Open'].iloc[0] # OPENING BINANCE TIME
                    
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
                            <div class="w-price">{price:.{prec}f}<br><span style="font-size:9px; color:{seta_c};">{set
