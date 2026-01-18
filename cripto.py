import streamlit as st
import pandas as pd
import time
import yfinance as yf
import random
import string
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO E LOGIN (ESTILO PRETO)
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #D4AF37; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- GERADOR DE SENHA SIMPLES NA LATERAL ---
with st.sidebar:
    st.markdown("<h3 style='color:#D4AF37;'>GERADOR ALPHA</h3>", unsafe_allow_html=True)
    if st.button("GERAR SENHA NUMÉRICA"):
        senha = ''.join(random.choice(string.digits) for i in range(6))
        st.code(senha)
    st.markdown("---")
    if st.button("LIMPAR CACHE / SAIR"):
        st.cache_data.clear()
        st.session_state.autenticado = False
        st.rerun()

# --- LÓGICA DE ACESSO ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=5)
except:
    st.error("Erro de conexão.")
    st.stop()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center; color:#D4AF37;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login"):
                u = st.text_input("USUÁRIO").strip()
                p = st.text_input("SENHA", type="password").strip()
                if st.form_submit_button("LIBERAR ACESSO"):
                    # Busca robusta para evitar KeyError (Imagem 1000026030)
                    user_row = df_users[df_users['user'].astype(str) == str(u)]
                    if not user_row.empty and str(p) == str(user_row.iloc[0]['password']):
                        st.session_state.autenticado = True
                        st.rerun()
                    else: st.error("DADOS INVORRETOS")
    st.stop()

# --- 2. TERMINAL VISÃO DE TUBARÃO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    .stApp { font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 32px; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .header-container { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; }
    .h-col { font-size: 10px; color: #FFF; text-align: center; font-weight: bold; width: 11%; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 5px 0; border-bottom: 1px solid #151515; }
    .w-ativo { width: 14%; padding-left: 10px; color: #EEE; font-size: 13px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 14px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 12px; font-weight: 800; }
    .t-y { background-color: #FFFF00; color: #000; border-radius: 2px; padding: 0 3px; }
    .status-box { padding: 6px 2px; border-radius: 2px; font-weight: 900; font-size: 9px; width: 90%; text-align: center; margin: auto; }
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-yellow { background-color: #FFFF00; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# Dicionário de ativos (Compactado para evitar erros de leitura no Streamlit)
assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT','NEAR-USD':'NEAR/USDT',
    'MATIC-USD':'POL/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT',
    'AAVE-USD':'AAVE/USDT','RENDER-USD':'RENDER/USDT','SUI-USD':'SUI/USDT','TIA-USD':'TIA/USDT','INJ-USD':'INJ/USDT',
    'SHIB-USD':'SHIB/USDT','LTC-USD':'LTC/USDT','BCH-USD':'BCH/USDT','APT-USD':'APT/USDT','STX-USD':'STX/USDT',
    'KAS-USD':'KAS/USDT','ARB-USD':'ARB/USDT','OP-USD':'OP/USDT','SEI-USD':'SEI/USDT','FIL-USD':'FIL/USDT',
    'HBAR-USD':'HBAR/USDT','ETC-USD':'ETC/USDT','ICP-USD':'ICP/USDT','BONK-USD':'BONK/USDT','FLOKI-USD':'FLOKI/USDT',
    'WIF-USD':'WIF/USDT','PYTH-USD':'PYTH/USDT','JUP-USD':'JUP/USDT','RAY-USD':'RAY/USDT','ORDI-USD':'ORDI/USDT',
    'IMX-USD':'IMX/USDT','LDO-USD':'LDO/USDT','TRX-USD':'TRX/USDT','ATOM-USD':'ATOM/USDT','MKR-USD':'MKR/USDT'
}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
placeholder = st.empty()

while True:
    try:
        data = yf.download(list(assets.keys()), period="1d", interval="1m", group_by='ticker', silent=True)
        with placeholder.container():
            st.markdown("""<div class="header-container">
                <div style="width:14%; color:#FFF; padding-left:10px; font-size:10px;">ATIVO</div>
                <div class="h-col">PREÇO</div><div class="h-col">ALVO 4%</div><div class="h-col">ALVO 8%</div>
                <div class="h-col">ALVO 10%</div><div class="h-col">SUP 4%</div><div class="h-col">SUP 8%</div>
                <div class="h-col">SUP 10%</div><div class="h-col" style="width:14%;">SINAL</div>
            </div>""", unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    price = data[tid]['Close'].iloc[-1]
                    open_p = data[tid]['Open'].iloc[0]
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt, s_cls, v4_cls = "ESTÁVEL", "bg-estavel", ""
                    if price >= v4: s_txt, s_cls, v4_cls = "DECISÃO ATENÇÃO", "bg-yellow", "t-y"
                    
                    prec = 4 if price < 10 else 2
                    st.markdown(f"""<div class="row-container">
                        <div class="w-ativo">{name}</div>
                        <div class="w-price">{price:.{prec}f}</div>
                        <div class="w-target" style="color:#FFFF00;"><span class="{v4_cls}">{v4:.{prec}f}</span></div>
                        <div class="w-target" style="color:#FFA500;">{v8:.{prec}f}</div>
                        <div class="w-target" style="color:#FF0000;">{v10:.{prec}f}</div>
                        <div class="w-target" style="color:#FFFF00;">{c4:.{prec}f}</div>
                        <div class="w-target" style="color:#FFA500;">{c8:.{prec}f}</div>
                        <div class="w-target" style="color:#00FF00;">{c10:.{prec}f}</div>
                        <div style="width:14%;"><div class="status-box {s_cls}">{s_txt}</div></div>
                    </div>""", unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: time.sleep(10)
