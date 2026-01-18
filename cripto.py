import streamlit as st
import pandas as pd
import time
import yfinance as yf
import random
import string
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO DE TELA
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# ESTILOS CSS (REVISADOS PARA EVITAR QUEBRAS)
st.markdown("""
    <style>
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    header, footer { visibility: hidden; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #D4AF37; }
    
    .title-gold { color: #D4AF37; font-size: 32px; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 14px; text-align: center; letter-spacing: 5px; margin-bottom: 15px; }
    
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 10px; color: #FFFFFF; text-transform: uppercase; text-align: center; font-weight: bold; width: 11%; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; }
    .w-ativo { width: 14%; padding-left: 10px; color: #EEE; font-size: 13px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 14px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 13px; font-weight: 800; }
    
    /* CORES DE ALERTA DINÂMICO */
    .t-y { background-color: #FFFF00; color: #000 !important; border-radius: 2px; padding: 1px 3px; }
    .t-o { background-color: #FFA500; color: #000 !important; border-radius: 2px; padding: 1px 3px; }
    .t-r { background-color: #FF0000; color: #FFF !important; border-radius: 2px; padding: 1px 3px; animation: blinker 0.4s linear infinite; }
    
    @keyframes blinker { 50% { opacity: 0.3; } }
    .status-box { padding: 6px 2px; border-radius: 2px; font-weight: 900; font-size: 9px; width: 90%; text-align: center; margin: auto; }
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-yellow { background-color: #FFFF00; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: GERADOR DE ACESSO NUMÉRICO ---
with st.sidebar:
    st.markdown("<h3 style='color:#D4AF37;'>ALPHA ADMIN</h3>", unsafe_allow_html=True)
    if st.button("GERAR ACESSO (6 DÍGITOS)"):
        senha_acesso = ''.join(random.choice(string.digits) for _ in range(6))
        st.code(senha_acesso)
        st.caption("Copie para o seu Google Sheets.")
    st.markdown("---")
    if st.button("SAIR / LOGOUT"):
        st.session_state.autenticado = False
        st.rerun()

# --- LÓGICA DE LOGIN ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_users = conn.read(ttl=5)
    except: st.stop()

    st.markdown("<h1 style='text-align:center;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            u = st.text_input("USUÁRIO").strip()
            p = st.text_input("SENHA", type="password").strip()
            if st.form_submit_button("LIBERAR ACESSO"):
                user_row = df_users[df_users['user'].astype(str) == u]
                if not user_row.empty and str(p) == str(user_row.iloc[0]['password']):
                    st.session_state.autenticado = True
                    st.rerun()
                else: st.error("DADOS INCORRETOS")
    st.stop()

# --- TERMINAL ALPHA VISION ---
assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'NEAR-USD':'NEAR/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT',
    'SUI-USD':'SUI/USDT','TIA-USD':'TIA/USDT','AAVE-USD':'AAVE/USDT','RENDER-USD':'RENDER/USDT','INJ-USD':'INJ/USDT'
}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

painel = st.empty()

while True:
    try:
        # Puxa dados (Yahoo Finance simula abertura 00:00 UTC no period 1d)
        data = yf.download(list(assets.keys()), period="1d", interval="1m", group_by='ticker', silent=True)
        
        with painel.container():
            st.markdown('<div class="header-container"><div class="h-col" style="width:14%; text-align:left; padding-left:10px;">ATIVO</div><div class="h-col" style="width:12%;">PREÇO</div><div class="h-col" style="width:10%;">ALVO 4%</div><div class="h-col" style="width:10%;">ALVO 8%</div><div class="h-col" style="width:10%;">ALVO 10%</div><div class="h-col" style="width:10%;">SUP 4%</div><div class="h-col" style="width:10%;">SUP 8%</div><div class="h-col" style="width:10%;">SUP 10%</div><div class="h-col" style="width:14%;">SINAL</div></div>', unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    df_t = data[tid]
                    price = df_t['Close'].iloc[-1]
                    open_p = df_t['Open'].iloc[0] # Abertura 00:00 UTC
                    
                    change = ((price - open_p) / open_p) * 100
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt, s_class, p_class = "ESTÁVEL", "bg-estavel", ""
                    if price >= v4: s_txt, s_class, p_class = "DECISÃO ATENÇÃO", "bg-yellow", "t-y"
                    
                    prec = 4 if price < 10 else 2
                    seta = '▲' if price >= open_p else '▼'
                    seta_c = '#00FF00' if price >= open_p else '#FF0000'

                    # Construção da linha fragmentada (Evita erro de string do Streamlit)
                    row = f'<div class="row-container">'
                    row += f'<div class="w-ativo">{name}</div>'
                    row += f'<div class="w-price">{price:.{prec}f}<br><span style="font-size:9px; color:{seta_c};">{seta}{change:+.2f}%</span></div>'
                    row += f'<div class="w-target" style="color:#FFFF00;"><span class="{p_class}">{v4:.{prec}f}</span></div>'
                    row += f'<div class="w-target" style="color:#FFA500;">{v8:.{prec}f}</div>'
                    row += f'<div class="w-target" style="color:#FF0000;">{v10:.{prec}f}</div>'
                    row += f'<div class="w-target" style="color:#FFFF00;">{c4:.{prec}f}</div>'
                    row += f'<div class="w-target" style="color:#FFA500;">{c8:.{prec}f}</div>'
                    row += f'<div class="w-target" style="color:#00FF00;">{c10:.{prec}f}</div>'
                    row += f'<div style="width:14%;"><div class="status-box {s_class}">{s_txt}</div></div></div>'
                    
                    st.markdown(row, unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: time.sleep(5)
