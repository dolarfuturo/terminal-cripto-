import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO ALPHA VISION
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .block-container { padding: 0rem 1rem !important; }
    header, footer { visibility: hidden; }
    
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; padding-top: 10px; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 16px; text-align: center; margin-top: -5px; letter-spacing: 7px; margin-bottom: 25px; font-weight: 700; }
    
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 10px; color: #FFFFFF; text-transform: uppercase; text-align: center; font-weight: 700; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; }
    .w-ativo { width: 14%; text-align: left; padding-left: 10px; color: #EEE; font-size: 14px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 12px; font-weight: 800; border-radius: 4px; margin: 0 2px; }
    .w-sinal { width: 14%; text-align: center; padding-right: 5px; }
    
    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 9px; width: 100%; text-align: center; text-transform: uppercase; }
    
    /* Blocos Sólidos (Estilo Barra) */
    .bar-amarela { background-color: #FFFF00 !important; color: #000 !important; font-weight: 900; box-shadow: 0 0 10px #FFFF00; }
    .bar-laranja { background-color: #FFA500 !important; color: #000 !important; font-weight: 900; box-shadow: 0 0 10px #FFA500; }
    
    /* Outros Estados */
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-amarelo { background-color: #FFFF00; color: #000; }
    .bg-laranja { background-color: #FFA500; color: #000; }
    .bg-parabolica { background-color: #800080; color: #FFF; }
    
    /* Exaustão Piscante */
    .blink-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .blink-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    .target-blink { color: #FF0000; animation: blinker 0.6s linear infinite; font-size: 14px !important; }
    .target-blink-down { color: #00FF00; animation: blinker 0.6s linear infinite; font-size: 14px !important; }
    
    @keyframes blinker { 50% { opacity: 0.1; } }
    
    .delta-price { font-size: 8px; display: block; opacity: 0.8; }
    </style>
    """, unsafe_allow_html=True)

# LOGIN
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('<div class="title-gold">ALPHA VISION</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        if st.button("LIBERAR ACESSO"):
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_users = conn.read(ttl=10)
                df_users.columns = [str(c).strip().lower() for c in df_users.columns]
                user_row = df_users[df_users['user'].astype(str) == u]
                if not user_row.empty and str(p) == str(user_row.iloc[0]['password']).strip():
                    st.session_state.autenticado = True
                    st.rerun()
            except: st.error("Erro de conexão.")
    st.stop()

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

# LISTA ATIVOS (Simplificada para o exemplo, mas você deve manter a sua de 80)
assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'CRV-USD':'CRV/USDT' # Adicione todos os outros aqui
}

placeholder = st.empty()

while True:
    try:
        data_batch = yf.download(list(assets.keys()), period="2d", interval="1m", group_by='ticker', progress=False)
        with placeholder.container():
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
                    price = float(df['Close'].iloc[-1]); open_p = float(df['Open'].iloc[0])
                    change = ((price - open_p) / open_p) * 100
                    
                    # Cálculos Alvos
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    # Setas e Cores de Tendência
                    arrow = "▲" if change >= 0 else "▼"
                    t_color = "#00FF00" if change >= 0 else "#FF0000"
                    
                    s_txt, s_class = "ESTÁVEL", "bg-estavel"
                    h4, h8, h10 = "", "", ""
                    
                    abs_c = abs(change)
                    if abs_c >= 12: 
                        s_txt, s_class = "PARABÓLICA", "bg-parabolica"
                        h4, h8, h10 = "bar-amarela", "bar-laranja", "target-blink"
                    elif abs_c >= 10: 
                        s_txt, s_class = "EXAUSTÃO", ("blink-red" if change > 0 else "blink-green")
                        h10 = "target-blink" if change > 0 else "target-blink-down"
                    elif abs_c >= 8: 
                        s_txt, s_class, h8 = "ATENÇÃO ALTA VOL", "bg-laranja", "bar-laranja"
                    elif abs_c >= 4: 
                        s_txt, s_class, h4 = "REGIÃO DE DECISÃO", "bg-amarelo", "bar-amarela"

                    prec = 4 if price < 1 else 2

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="w-ativo">{name}</div>
                            <div class="w-price"><span style="color:{t_color};">{arrow}</span> {price:.{prec}f}</div>
                            <div class="w-target {h4 if change > 0 else ''}" style="color:#FFFF00;">{v4:.{prec}f}<span class="delta-price">+{v4-open_p:.{prec}f}</span></div>
                            <div class="w-target {h8 if change > 0 else ''}" style="color:#FFA500;">{v8:.{prec}f}<span class="delta-price">+{v8-open_p:.{prec}f}</span></div>
                            <div class="w-target {h10 if change > 0 else ''}">{v10:.{prec}f}<span class="delta-price">+{v10-open_p:.{prec}f}</span></div>
                            <div class="w-target {h4 if change < 0 else ''}" style="color:#FFFF00;">{c4:.{prec}f}<span class="delta-price">-{open_p-c4:.{prec}f}</span></div>
                            <div class="w-target {h8 if change < 0 else ''}" style="color:#FFA500;">{c8:.{prec}f}<span class="delta-price">-{open_p-c8:.{prec}f}</span></div>
                            <div class="w-target {h10 if change < 0 else ''}">{c10:.{prec}f}<span class="delta-price">-{open_p-c10:.{prec}f}</span></div>
                            <div class="w-sinal"><div class="status-box {s_class}">{s_txt}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
                except: continue
        time.sleep(10)
    except: time.sleep(5)
