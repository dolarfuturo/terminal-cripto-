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
    .title-gold { color: #D4AF37; font-size: 30px; font-weight: 900; text-align: center; padding: 10px; }
    .header-container { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; }
    .h-col { font-size: 10px; color: #FFF; text-align: center; text-transform: uppercase; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 8px 0; border-bottom: 1px solid #151515; }
    .w-col { flex: 1; text-align: center; font-size: 13px; font-weight: 700; }
    .status-box { padding: 5px; border-radius: 2px; font-size: 10px; font-weight: 900; text-align: center; }
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-red { background-color: #FF0000; color: #FFF; animation: blinker 0.5s linear infinite; }
    .bg-green { background-color: #00FF00; color: #000; animation: blinker 0.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN (PLANILHA + STATUS)
if 'auth' not in st.session_state: st.session_state.auth = False

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=10)
    df_users.columns = df_users.columns.str.strip().str.lower()
except:
    df_users = pd.DataFrame()

if not st.session_state.auth:
    st.markdown('<div class="title-gold">ALPHA VISION LOGIN</div>', unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.form_submit_button("Acessar"):
            user_row = df_users[df_users['user'].astype(str) == u]
            if not user_row.empty and str(user_row.iloc[0]['password']) == p:
                if str(user_row.iloc[0].get('status', 'ativo')).lower() == 'ativo':
                    st.session_state.auth = True
                    st.rerun()
                else: st.error("Acesso Bloqueado.")
            else: st.error("Credenciais Inválidas.")
    st.stop()

# 3. MONITOR DE ATIVOS (CORRIGIDO PARA NÃO TRAVAR)
assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'NEAR-USD':'NEAR/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT'
    # ... adicione os outros aqui
}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
placeholder = st.empty()

while True:
    try:
        # Puxa os dados de uma vez só (mais rápido)
        data = yf.download(list(assets.keys()), period="1d", interval="1m", group_by='ticker', silent=True)
        
        with placeholder.container():
            st.markdown("""<div class="header-container">
                <div class="h-col">ATIVO</div><div class="h-col">PREÇO</div><div class="h-col">4%</div>
                <div class="h-col">8%</div><div class="h-col">10%</div><div class="h-col">SINAL</div>
                </div>""", unsafe_allow_html=True)

            for tid, name in assets.items():
                if tid not in data: continue
                df_t = data[tid]
                if df_t.empty: continue
                
                price = df_t['Close'].iloc[-1]
                open_p = df_t['Open'].iloc[0] # RESET 00:00 UTC (Início do DF de 1 dia)
                
                change = ((price - open_p) / open_p) * 100
                v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                
                # Lógica de Sinal
                s_txt, s_bg = "ESTÁVEL", "bg-estavel"
                if change >= 10: s_txt, s_bg = "EXAUSTÃO", "bg-red"
                elif change <= -10: s_txt, s_bg = "EXAUSTÃO", "bg-green"

                prec = 4 if price < 10 else 2
                
                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{name}</div>
                        <div class="w-col">{price:.{prec}f}</div>
                        <div class="w-col" style="color:#FFFF00;">{v4:.{prec}f}</div>
                        <div class="w-col" style="color:#FFA500;">{v8:.{prec}f}</div>
                        <div class="w-col" style="color:#FF0000;">{v10:.{prec}f}</div>
                        <div class="w-col"><div class="status-box {s_bg}">{s_txt}</div></div>
                    </div>
                """, unsafe_allow_html=True)
                
        time.sleep(15)
    except Exception as e:
        st.error(f"Erro ao carregar ativos: {e}")
        time.sleep(5)
