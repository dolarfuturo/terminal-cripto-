import streamlit as st
import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; color: white; }
    .title-gold { color: #D4AF37; font-size: 28px; font-weight: 900; text-align: center; padding: 15px 0; }
    .header-container { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; margin-bottom: 5px; }
    .h-col { font-size: 10px; color: #FFF; text-align: center; flex: 1; font-weight: bold; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 10px 0; border-bottom: 1px solid #181818; }
    .w-col { flex: 1; text-align: center; font-size: 14px; font-weight: 700; }
    .status-box { padding: 6px; border-radius: 2px; font-size: 10px; font-weight: 900; text-align: center; width: 90%; margin: 0 auto; }
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-red { background-color: #FF0000; color: #FFF; }
    .bg-green { background-color: #00FF00; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN (PLANILHA)
if 'auth' not in st.session_state: st.session_state.auth = False

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=10)
    df_users.columns = df_users.columns.str.strip().str.lower()
except:
    df_users = pd.DataFrame([{"user":"admin","password":"123","status":"ativo"}])

if not st.session_state.auth:
    st.markdown('<div class="title-gold">ALPHA VISION LOGIN</div>', unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.form_submit_button("Acessar"):
            user_row = df_users[df_users['user'].astype(str) == u]
            if not user_row.empty and str(user_row.iloc[0]['password']) == p:
                st.session_state.auth = True
                st.rerun()
            else: st.error("Erro no login")
    st.stop()

# 3. LISTA DE ATIVOS
assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT'
}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        # Cabeçalho da Tabela
        st.markdown("""<div class="header-container">
            <div class="h-col">ATIVO</div><div class="h-col">PREÇO</div>
            <div class="h-col">VARIAÇÃO</div><div class="h-col">RESISTÊNCIA (10%)</div>
            <div class="h-col">SINAL</div></div>""", unsafe_allow_html=True)

        for tid, name in assets.items():
            try:
                # Busca dado individual (Mais lento porém 100% seguro contra tela preta)
                ticker = yf.Ticker(tid)
                hist = ticker.history(period="1d", interval="1m")
                
                if hist.empty: continue
                
                price = hist['Close'].iloc[-1]
                open_p = hist['Open'].iloc[0]
                change = ((price - open_p) / open_p) * 100
                v10 = open_p * 1.10
                
                s_txt, s_bg = "ESTÁVEL", "bg-estavel"
                if change >= 10: s_txt, s_bg = "EXAUSTÃO", "bg-red"
                elif change <= -10: s_txt, s_bg = "EXAUSTÃO", "bg-green"

                color = "#00FF00" if change >= 0 else "#FF0000"
                prec = 2 if price > 1 else 4

                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{name}</div>
                        <div class="w-col">{price:.{prec}f}</div>
                        <div class="w-col" style="color:{color};">{change:+.2f}%</div>
                        <div class="w-col">{v10:.{prec}f}</div>
                        <div class="w-col"><div class="status-box {s_bg}">{s_txt}</div></div>
                    </div>
                """, unsafe_allow_html=True)
            except:
                continue
    
    time.sleep(15)
