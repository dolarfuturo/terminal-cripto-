import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO ALPHA VISION
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide", initial_sidebar_state="collapsed")

# Estilo para remover espaços brancos e fixar o fundo
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    header, footer { visibility: hidden; }
    
    /* Títulos */
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; padding-top: 10px; margin-bottom: 0px; font-family: 'JetBrains Mono', monospace; }
    .subtitle-vision { color: #C0C0C0; font-size: 16px; text-align: center; margin-top: -5px; letter-spacing: 7px; margin-bottom: 15px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    
    /* Cabeçalho Fixo */
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 10px; color: #FFFFFF; text-transform: uppercase; text-align: center; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    
    /* Linhas da Tabela */
    .row-container { display: flex; width: 100%; align-items: stretch; padding: 0; border-bottom: 1px solid #151515; min-height: 50px; }
    .w-ativo { width: 14%; display: flex; align-items: center; padding-left: 10px; color: #EEE; font-size: 14px; font-weight: 700; }
    .w-price { width: 12%; display: flex; flex-direction: column; justify-content: center; align-items: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .w-target { width: 10%; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 800; text-align: center; }
    
    /* Sinalizador - Barra Inteira */
    .w-sinal { width: 14%; display: flex; align-items: stretch; padding: 0; }
    .status-box { display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 11px; width: 100%; text-align: center; text-transform: uppercase; }
    
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-blink-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .bg-blink-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# LOGIN (CONECTADO AO SEU GSHEETS)
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    # ... (Mantendo sua lógica de login intacta aqui)
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_users = conn.read(ttl=10)
        df_users.columns = [str(c).strip().lower() for c in df_users.columns]
    except: st.stop()
    
    st.markdown("<h1 style='text-align:center; color:#D4AF37;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    u = st.text_input("USUÁRIO")
    p = st.text_input("SENHA", type="password")
    if st.button("LIBERAR ACESSO"):
        user_row = df_users[df_users['user'].astype(str) == u]
        if not user_row.empty and str(p) == str(user_row.iloc[0]['password']).strip():
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# INTERFACE DO TERMINAL
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT'
}

placeholder = st.empty()

while True:
    try:
        data_batch = yf.download(list(assets.keys()), period="2d", interval="1m", group_by='ticker', progress=False)
        with placeholder.container():
            # CABEÇALHO CORRIGIDO E ALINHADO
            st.markdown("""<div class="header-container">
                <div class="h-col" style="width:14%; text-align:left; padding-left:10px;">ATIVO</div>
                <div class="h-col" style="width:12%;">PREÇO ATUAL</div>
                <div class="h-col" style="width:10%;">RESISTÊNCIA</div>
                <div class="h-col" style="width:10%;">PRÓX AO TOPO</div>
                <div class="h-col" style="width:10%;">TETO EXAUSTÃO</div>
                <div class="h-col" style="width:10%;">SUPORTE</div>
                <div class="h-col" style="width:10%;">PRÓX FUNDO</div>
                <div class="h-col" style="width:10%;">CHÃO EXAUSTÃO</div>
                <div class="h-col" style="width:14%;">SINALIZADOR</div></div>""", unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    df = data_batch[tid].dropna()
                    if df.empty: continue
                    
                    price = float(df['Close'].iloc[-1])
                    open_p = float(df['Open'].iloc[0])
                    change = ((price - open_p) / open_p) * 100
                    
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt, s_class = "ESTÁVEL", "bg-estavel"
                    if change >= 10: s_txt, s_class = "EXAUSTÃO MÁXIMA", "bg-blink-red"
                    elif change <= -10: s_txt, s_class = "EXAUSTÃO MÁXIMA", "bg-blink-green"

                    prec = 4 if price < 10 else 2
                    color = "#00FF00" if price >= open_p else "#FF0000"

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="w-ativo">{name}</div>
                            <div class="w-price">{price:.{prec}f}<br><span style="font-size:9px; color:{color};">{change:+.2f}%</span></div>
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
