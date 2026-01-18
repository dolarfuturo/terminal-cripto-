import streamlit as st
import pandas as pd
import yfinance as yf
import time
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO ESSENCIAL
st.set_page_config(page_title="ALPHA VISION PRO", layout="wide", initial_sidebar_state="collapsed")

# CSS Simplificado em bloco único para evitar quebras de script
st.markdown("""
    <style>
    .stApp { background-color: #000000; font-family: sans-serif; }
    header, footer { visibility: hidden; }
    .title-gold { color: #D4AF37; font-size: 28px; font-weight: 900; text-align: center; margin-bottom: 10px; }
    .header-container { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 9px; color: #FFFFFF; text-align: center; font-weight: bold; width: 11%; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 5px 0; border-bottom: 1px solid #111; }
    .w-ativo { width: 14%; padding-left: 10px; color: #EEE; font-size: 13px; font-weight: bold; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 14px; font-weight: bold; }
    .w-target { width: 10%; text-align: center; font-size: 12px; }
    .bg-alert { background-color: #FFFF00; color: #000; border-radius: 2px; padding: 2px; }
    .status-box { padding: 5px; border-radius: 2px; font-weight: bold; font-size: 9px; width: 90%; text-align: center; margin: auto; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE LOGIN (GSHEETS)
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_users = conn.read(ttl=5)
    except:
        st.error("Erro na base de dados")
        st.stop()

    st.markdown("<h1 style='text-align:center; color:#D4AF37;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        with st.form("login"):
            u = st.text_input("USUÁRIO").strip()
            p = st.text_input("SENHA", type="password").strip()
            if st.form_submit_button("ENTRAR"):
                match = df_users[df_users['user'].astype(str) == u]
                if not match.empty and str(p) == str(match.iloc[0]['password']):
                    st.session_state.autenticado = True
                    st.rerun()
                else: st.error("Acesso Negado")
    st.stop()

# 3. TERMINAL (REMOVIDO GERADOR)
assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'NEAR-USD':'NEAR/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT',
    'SUI-USD':'SUI/USDT','TIA-USD':'TIA/USDT','AAVE-USD':'AAVE/USDT','RENDER-USD':'RENDER/USDT','INJ-USD':'INJ/USDT'
}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
monitor = st.empty()

while True:
    try:
        # Download otimizado (apenas o necessário)
        data = yf.download(list(assets.keys()), period="1d", interval="1m", silent=True)
        
        with monitor.container():
            # Cabeçalho Fixo
            st.markdown('<div class="header-container"><div style="width:14%; color:#FFF; padding-left:10px; font-size:9px;">ATIVO</div><div class="h-col">PREÇO</div><div class="h-col">ALVO 4%</div><div class="h-col">ALVO 8%</div><div class="h-col">ALVO 10%</div><div class="h-col">SUP 4%</div><div class="h-col">SUP 8%</div><div class="h-col">SUP 10%</div><div class="h-col" style="width:14%;">SINAL</div></div>', unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    # Lógica de Preços (Reset 00:00 UTC via yfinance period 1d)
                    price = data['Close'][tid].iloc[-1]
                    open_p = data['Open'][tid].iloc[0]
                    
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt, s_color, p_class = "ESTÁVEL", "#00CED1", ""
                    if price >= v4: s_txt, s_color, p_class = "ALERTA", "#FFFF00", "bg-alert"
                    
                    dec = 4 if price < 10 else 2
                    
                    row_html = f'<div class="row-container">'
                    row_html += f'<div class="w-ativo">{name}</div>'
                    row_html += f'<div class="w-price">{price:.{dec}f}</div>'
                    row_html += f'<div class="w-target" style="color:#FFFF00;"><span class="{p_class}">{v4:.{dec}f}</span></div>'
                    row_html += f'<div class="w-target" style="color:#FFA500;">{v8:.{dec}f}</div>'
                    row_html += f'<div class="w-target" style="color:#FF0000;">{v10:.{dec}f}</div>'
                    row_html += f'<div class="w-target" style="color:#FFFF00;">{c4:.{dec}f}</div>'
                    row_html += f'<div class="w-target" style="color:#FFA500;">{c8:.{dec}f}</div>'
                    row_html += f'<div class="w-target" style="color:#00FF00;">{c10:.{dec}f}</div>'
                    row_html += f'<div style="width:14%;"><div class="status-box" style="background:{s_color}; color:#000;">{s_txt}</div></div></div>'
                    
                    st.markdown(row_html, unsafe_allow_html=True)
                except: continue
        
        time.sleep(20) # Aumentado para 20s para evitar bloqueio do Yahoo Finance
    except:
        time.sleep(10)
