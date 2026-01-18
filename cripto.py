import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO E LOGIN (ESTRUTURA ORIGINAL)
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    div[data-testid="stForm"] { background-color: #050505; border: 1px solid #151515; border-radius: 5px; }
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    .stApp { font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; padding-top: 10px; }
    .subtitle-vision { color: #C0C0C0; font-size: 16px; text-align: center; letter-spacing: 7px; margin-bottom: 15px; font-weight: 700; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 11px; color: #FFFFFF; text-transform: uppercase; text-align: center; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; }
    .w-ativo { width: 14%; text-align: left; padding-left: 10px; color: #EEE; font-size: 14px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 14px; font-weight: 800; }
    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 9px; width: 100%; text-align: center; text-transform: uppercase; }
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-blink-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .bg-blink-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# CONEXÃO E TRAVA DE LOGIN
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=5)
    df_users.columns = [str(c).strip().lower() for c in df_users.columns]
    df_users = df_users.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)
except:
    st.stop()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center; color:#D4AF37;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            u = st.text_input("USUÁRIO").strip().lower()
            p = st.text_input("SENHA", type="password").strip()
            if st.form_submit_button("LIBERAR ACESSO"):
                user_match = df_users[df_users['user'].str.lower() == u]
                if not user_match.empty and p == str(user_match.iloc[0]['password']):
                    data_venc = pd.to_datetime(user_match.iloc[0]['vencimento']).date()
                    if datetime.now().date() > data_venc:
                        st.error(f"ACESSO EXPIRADO: {data_venc.strftime('%d/%m/%Y')}")
                        st.markdown(f'<a href="https://t.me/+GOzXsBo0BchkMzYx" target="_blank"><button style="width:100%; background-color:#D4AF37; color:black; border:none; padding:12px; font-weight:bold; cursor:pointer; border-radius:5px;">RENOVAR NO GRUPO DE SUPORTE</button></a>', unsafe_allow_html=True)
                    else:
                        st.session_state.autenticado = True
                        st.rerun()
                else: st.error("Acesso negado.")
    st.stop()

# 2. TERMINAL VISÃO DE TUBARÃO (DADOS ORIGINAIS)
assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'NEAR-USD':'NEAR/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT'
}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO • RESET 00:00 UTC</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        # Captura precisa para evitar "nan"
        data_batch = yf.download(list(assets.keys()), period="1d", interval="1m", group_by='ticker', progress=False)
        
        with placeholder.container():
            st.markdown("""<div class="header-container">
                <div class="h-col" style="width:14%; text-align:left; padding-left:10px;">ATIVO</div>
                <div class="h-col" style="width:12%;">PREÇO</div>
                <div class="h-col" style="width:10%;">4%</div><div class="h-col" style="width:10%;">8%</div><div class="h-col" style="width:10%;">10%</div>
                <div class="h-col" style="width:10%;">-4%</div><div class="h-col" style="width:10%;">-8%</div><div class="h-col" style="width:10%;">-10%</div>
                <div class="h-col" style="width:14%;">SINAL</div></div>""", unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    df_t = data_batch[tid]
                    if df_t.empty or len(df_t) < 1: continue
                    
                    current_p = float(df_t['Close'].iloc[-1])
                    open_p = float(df_t['Open'].iloc[0]) # Reset Binance 00:00 UTC
                    change = ((current_p - open_p) / open_p) * 100
                    
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt, s_class = "ESTÁVEL", "bg-estavel"
                    if change >= 10: s_txt, s_class = "EXAUSTÃO", "bg-blink-red"
                    elif change <= -10: s_txt, s_class = "EXAUSTÃO", "bg-blink-green"

                    prec = 4 if current_p < 10 else 2
                    color = "#00FF00" if current_p >= open_p else "#FF0000"

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="w-ativo">{name}</div>
                            <div class="w-price">{current_p:.{prec}f}<br><span style="font-size:9px; color:{color};">{change:+.2f}%</span></div>
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
