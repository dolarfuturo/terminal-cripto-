import streamlit as st
import pandas as pd
import time
import yfinance as yf
import random
import string
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO INICIAL
st.set_page_config(page_title="ALPHA VISION PRO", layout="wide", initial_sidebar_state="collapsed")

# Estilo para garantir fundo preto e inputs dourados
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #D4AF37; }
    header, footer { visibility: hidden; }
    .stMarkdown h1 { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: GERADOR E LOGOUT ---
with st.sidebar:
    st.markdown("<h3 style='color:#D4AF37;'>PAINEL ALPHA</h3>", unsafe_allow_html=True)
    if st.button("GERAR SENHA CLIENTE"):
        senha_nova = ''.join(random.choice(string.digits) for i in range(6))
        st.code(senha_nova)
    st.markdown("---")
    if st.button("SAIR DO SISTEMA"):
        st.session_state.autenticado = False
        st.rerun()

# --- 2. SISTEMA DE LOGIN ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=5)
except:
    st.error("Erro de conexão com a planilha.")
    st.stop()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_alpha"):
            u = st.text_input("USUÁRIO").strip()
            p = st.text_input("SENHA", type="password").strip()
            if st.form_submit_button("LIBERAR ACESSO"):
                user_match = df_users[df_users['user'].astype(str) == str(u)]
                if not user_match.empty and str(p) == str(user_match.iloc[0]['password']):
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("ACESSO NEGADO")
    st.stop()

# --- 3. TERMINAL VISÃO DE TUBARÃO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700;900&display=swap');
    .stApp { font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 35px; font-weight: 900; text-align: center; margin: 0; }
    .header-table { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background: #080808; position: sticky; top: 0; }
    .h-col { font-size: 10px; color: #FFF; text-align: center; font-weight: bold; width: 11%; }
    .row-alpha { display: flex; width: 100%; align-items: center; padding: 8px 0; border-bottom: 1px solid #181818; }
    .c-ativo { width: 14%; padding-left: 10px; color: #FFF; font-size: 13px; font-weight: 700; }
    .c-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .c-val { width: 10%; text-align: center; font-size: 13px; font-weight: 700; }
    /* CORES DE DESTAQUE */
    .bg-yellow { background-color: #FFFF00; color: #000; border-radius: 2px; padding: 1px 4px; }
    .status-btn { padding: 6px; border-radius: 3px; font-size: 9px; font-weight: 900; text-align: center; width: 90%; margin: auto; }
    .st-estavel { background-color: #00CED1; color: #000; }
    .st-alerta { background-color: #FFFF00; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# LISTA DE ATIVOS REORGANIZADA PARA EVITAR ERROS
assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'NEAR-USD':'NEAR/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT',
    'SUI-USD':'SUI/USDT','TIA-USD':'TIA/USDT','AAVE-USD':'AAVE/USDT','RENDER-USD':'RENDER/USDT','INJ-USD':'INJ/USDT',
    'MATIC-USD':'POL/USDT','SHIB-USD':'SHIB/USDT','LTC-USD':'LTC/USDT','BCH-USD':'BCH/USDT','APT-USD':'APT/USDT'
}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#C0C0C0; letter-spacing:5px;'>VISÃO DE TUBARÃO</p>", unsafe_allow_html=True)

monitor = st.empty()

while True:
    try:
        data = yf.download(list(assets.keys()), period="1d", interval="1m", group_by='ticker', silent=True)
        with monitor.container():
            st.markdown("""<div class="header-table">
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
                    
                    s_txt, s_style, price_style = "ESTÁVEL", "st-estavel", ""
                    if price >= v4: 
                        s_txt, s_style, price_style = "DECISÃO ATENÇÃO", "st-alerta", "bg-yellow"

                    p_dec = 4 if price < 10 else 2
                    st.markdown(f"""<div class="row-alpha">
                        <div class="c-ativo">{name}</div>
                        <div class="c-price">{price:.{p_dec}f}</div>
                        <div class="c-val" style="color:#FFFF00;"><span class="{price_style}">{v4:.{p_dec}f}</span></div>
                        <div class="c-val" style="color:#FFA500;">{v8:.{p_dec}f}</div>
                        <div class="c-val" style="color:#FF0000;">{v10:.{p_dec}f}</div>
                        <div class="c-val" style="color:#FFFF00;">{c4:.{p_dec}f}</div>
                        <div class="c-val" style="color:#FFA500;">{c8:.{p_dec}f}</div>
                        <div class="c-val" style="color:#00FF00;">{c10:.{p_dec}f}</div>
                        <div style="width:14%;"><div class="status-btn {s_style}">{s_txt}</div></div>
                    </div>""", unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: 
        time.sleep(5)
