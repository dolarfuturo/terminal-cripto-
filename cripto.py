import streamlit as st
import pandas as pd
import time
import yfinance as yf
import random
import string
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION PRO", layout="wide", initial_sidebar_state="collapsed")

# Estilo unificado para evitar quebras de renderização
st.markdown("""
    <style>
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    .stMarkdown h1 { color: #D4AF37 !important; text-align: center; }
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #D4AF37; }
    .header-alpha { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 10px; color: #FFF; text-align: center; font-weight: bold; width: 11%; }
    .row-alpha { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #181818; }
    .c-ativo { width: 14%; padding-left: 10px; color: #FFF; font-size: 13px; font-weight: 700; }
    .c-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .c-val { width: 10%; text-align: center; font-size: 12px; font-weight: 700; }
    .bg-alert { background-color: #FFFF00; color: #000; border-radius: 2px; padding: 0 4px; }
    .status-box { padding: 5px; border-radius: 3px; font-size: 9px; font-weight: 900; text-align: center; width: 90%; margin: auto; }
    .st-ok { background-color: #00CED1; color: #000; }
    .st-warn { background-color: #FFFF00; color: #000; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: GERADOR DE ACESSOS ---
with st.sidebar:
    st.markdown("<h3 style='color:#D4AF37;'>ALPHA ADMIN</h3>", unsafe_allow_html=True)
    if st.button("GERAR SENHA CLIENTE"):
        st.code(''.join(random.choice(string.digits) for _ in range(6)))
    if st.button("LOGOUT"):
        st.session_state.autenticado = False
        st.rerun()

# --- 2. GESTÃO DE ACESSO ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_users = conn.read(ttl=5)
    except: st.stop()
    
    st.markdown("<h1>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login"):
            u = st.text_input("USUÁRIO").strip()
            p = st.text_input("SENHA", type="password").strip()
            if st.form_submit_button("LIBERAR"):
                match = df_users[df_users['user'].astype(str) == u]
                if not match.empty and str(p) == str(match.iloc[0]['password']):
                    st.session_state.autenticado = True
                    st.rerun()
                else: st.error("NEGADO")
    st.stop()

# --- 3. TERMINAL AUTOMÁTICO (RESET 00:00 UTC) ---
assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT','NEAR-USD':'NEAR/USDT',
    'MATIC-USD':'POL/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT',
    'SUI-USD':'SUI/USDT','TIA-USD':'TIA/USDT','AAVE-USD':'AAVE/USDT','RENDER-USD':'RENDER/USDT','INJ-USD':'INJ/USDT'
}

st.markdown("<h2 style='color:#D4AF37; text-align:center; margin:0;'>ALPHA VISION CRYPTO</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#C0C0C0; font-size:12px; letter-spacing:4px;'>VISÃO DE TUBARÃO</p>", unsafe_allow_html=True)

monitor = st.empty()

while True:
    try:
        data = yf.download(list(assets.keys()), period="1d", interval="1m", group_by='ticker', silent=True)
        with monitor.container():
            st.markdown("""<div class="header-alpha">
                <div style="width:14%; color:#FFF; padding-left:10px; font-size:10px;">ATIVO</div>
                <div class="h-col">PREÇO</div><div class="h-col">ALVO 4%</div><div class="h-col">ALVO 8%</div>
                <div class="h-col">ALVO 10%</div><div class="h-col">SUP 4%</div><div class="h-col">SUP 8%</div>
                <div class="h-col">SUP 10%</div><div class="h-col" style="width:14%;">SINAL</div>
            </div>""", unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    tick = data[tid]
                    price = tick['Close'].iloc[-1]
                    open_p = tick['Open'].iloc[0] # Representa o preço de abertura do dia (00:00 UTC aprox)
                    
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt, s_style, p_style = "ESTÁVEL", "st-ok", ""
                    if price >= v4: s_txt, s_style, p_style = "DECISÃO ATENÇÃO", "st-warn", "bg-alert"

                    dec = 4 if price < 10 else 2
                    st.markdown(f"""<div class="row-alpha">
                        <div class="c-ativo">{name}</div>
                        <div class="c-price">{price:.{dec}f}</div>
                        <div class="c-val" style="color:#FFFF00;"><span class="{p_style}">{v4:.{dec}f}</span></div>
                        <div class="c-val" style="color:#FFA500;">{v8:.{dec}f}</div>
                        <div class="c-val" style="color:#FF0000;">{v10:.{dec}f}</div>
                        <div class="c-val" style="color:#FFFF00;">{c4:.{dec}f}</div>
                        <div class="c-val" style="color:#FFA500;">{c8:.{dec}f}</div>
                        <div class="c-val" style="color:#00FF00;">{c10:.{dec}f}</div>
                        <div style="width:14%;"><div class="status-box {s_style}">{s_txt}</div></div>
                    </div>""", unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: time.sleep(5)
