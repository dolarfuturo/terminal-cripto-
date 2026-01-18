import streamlit as st
import pandas as pd
import time
import yfinance as yf
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO ALPHA VISION
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide", initial_sidebar_state="collapsed")

# ESTILO VISUAL
st.markdown("""
    <style>
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    header, footer { visibility: hidden; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    .stMarkdown h1 { color: #D4AF37 !important; }
    div[data-testid="stForm"] { background-color: #050505; border: 1px solid #151515; border-radius: 5px; }
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; padding-top: 10px; }
    .subtitle-vision { color: #C0C0C0; font-size: 14px; text-align: center; letter-spacing: 5px; margin-bottom: 15px; }
    
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 10px; font-weight: 700; color: #FFFFFF; text-align: center; text-transform: uppercase; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; }
    .w-ativo { width: 14%; text-align: left; padding-left: 10px; color: #EEE; font-size: 14px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 13px; font-weight: 800; }
    .w-sinal { width: 14%; text-align: center; }

    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 9px; width: 100%; text-align: center; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-yellow { background-color: #FFFF00; color: #000; }
    .bg-orange { background-color: #FFA500; color: #000; }
    .bg-blink-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .bg-blink-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    .bg-purple { background-color: #8A2BE2; color: #FFF; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÃO PLANILHA
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=10)
    df_users.columns = df_users.columns.str.strip().str.lower()
except:
    st.error("Erro ao ler banco de dados.")
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
                        status_val = str(user_match.iloc[0].get('status', 'ativo')).strip().lower()
                        if status_val == 'ativo':
                            st.session_state.autenticado = True
                            st.rerun()
                        else: st.error("ACESSO BLOQUEADO.")
                    else: st.error("Senha incorreta.")
                else: st.error("Usuário não cadastrado.")
        st.markdown("<p style='text-align:center; color:gray;'>Sinal instável? Fale com o suporte.</p>", unsafe_allow_html=True)
    st.stop()

# 4. TERMINAL (80 ATIVOS)
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

while True:
    try:
        data_batch = yf.download(list(assets.keys()), period="1d", interval="1m", group_by='ticker', silent=True)
        with placeholder.container():
            st.markdown("""
                <div class="header-container">
                    <div class="h-col" style="width:14%; text-align:left; padding-left:10px;">ATIVO</div>
                    <div class="h-col" style="width:12%;">PREÇO</div>
                    <div class="h-col" style="width:10%;">RESIST</div>
                    <div class="h-col" style="width:10%;">TOPO</div>
                    <div class="h-col" style="width:10%;">TETO</div>
                    <div class="h-col" style="width:10%;">SUPORTE</div>
                    <div class="h-col" style="width:10%;">FUNDO</div>
                    <div class="h-col" style="width:10%;">CHÃO</div>
                    <div class="h-col" style="width:14%;">SINAL</div>
                </div>
            """, unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    df_ticker = data_batch[tid]
                    price = df_ticker['Close'].iloc[-1]
                    open_p = df_ticker['Open'].iloc[0]
                    change = ((price - open_p) / open_p) * 100
                    
                    # Níveis
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt, s_class = "ESTÁVEL", "bg-estavel"
                    if change >= 10: s_txt, s_class = "EXAUSTÃO", "bg-blink-red"
                    elif price >= v8: s_txt, s_class = "ALTA VOL", "bg-orange"
                    elif price >= v4: s_txt, s_class = "ATENÇÃO", "bg-yellow"
                    elif change <= -10: s_txt, s_class = "EXAUSTÃO", "bg-blink-green"
                    elif price <= c8: s_txt, s_class = "ALTA VOL", "bg-orange"
                    elif price <= c4: s_txt, s_class = "ATENÇÃO", "bg-yellow"

                    prec = 4 if price < 10 else 2
                    seta = '▲' if price >= open_p else '▼'
                    color = '#00FF00' if price >= open_p else '#FF0000'

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="w-ativo">{name}</div>
                            <div class="w-price">{price:.{prec}f}<br><span style="font-size:9px; color:{color};">{seta}{change:+.2f}%</span></div>
                            <div class="w-target" style="color:#FFFF00;">{v4:.{prec}f}</div>
                            <div class="w-target" style="color:#FFA500;">{v8:.{prec}f}</div>
                            <div class="w-target" style="color:#FF0000;">{v10:.{prec}f}</div>
                            <div class="w-target" style="color:#FFFF00;">{c4:.{prec}f}</div>
                            <div class="w-target" style="color:#FFA500;">{c8:.{prec}f}</div>
                            <div class="w-target" style="color:#00FF00;">{c10:.{prec}f}</div>
                            <div class="w-sinal"><div class="status-box {s_class}">{s_txt}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: time.sleep(10)
