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
    .stMarkdown h1 { color: #D4AF37 !important; }
    label { color: #C0C0C0 !important; }
    /* Estilo da barra lateral */
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- GERADOR DE SENHA SIMPLES NA LATERAL ---
with st.sidebar:
    st.markdown("<h3 style='color:#D4AF37;'>GERADOR DE ACESSO</h3>", unsafe_allow_html=True)
    st.write("Crie senhas numéricas rápidas:")
    col_g1, col_g2 = st.columns(2)
    if st.button("GERAR SENHA"):
        # Gera apenas números (ex: 847293)
        senha_simples = ''.join(random.choice(string.digits) for i in range(6))
        st.code(senha_simples)
        st.caption("Apenas números para evitar erros do cliente.")

# --- LÓGICA DE ACESSO ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=10)
except:
    st.error("Erro de conexão com a planilha.")
    st.stop()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    with st.container():
        left, mid, right = st.columns([1, 2, 1])
        with mid:
            with st.form("login_form"):
                u = st.text_input("USUÁRIO")
                p = st.text_input("SENHA", type="password")
                if st.form_submit_button("LIBERAR ACESSO"):
                    user_row = df_users[df_users['user'] == u]
                    if not user_row.empty and str(p) == str(user_row.iloc[0]['password']):
                        venc = pd.to_datetime(user_row.iloc[0]['vencimento']).date()
                        if datetime.now().date() <= venc:
                            st.session_state.autenticado = True
                            st.rerun()
                        else: st.error("ACESSO EXPIRADO.")
                    else: st.error("DADOS INCORRETOS.")
    st.stop()

# --- 2. TERMINAL VISÃO DE TUBARÃO (80 ATIVOS + CORES ORIGINAIS + DESTAQUE NOS VALORES) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; padding-top: 10px; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 16px; text-align: center; margin-top: -5px; letter-spacing: 7px; margin-bottom: 15px; font-weight: 700; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 11px; font-weight: 400; color: #FFFFFF; text-transform: uppercase; text-align: center; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; gap: 0px; }
    .w-ativo { width: 14%; text-align: left; padding-left: 10px; color: #EEE; font-size: 14px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 14px; font-weight: 800; }
    .w-sinal { width: 14%; text-align: center; padding-right: 5px; }
    .t-y { background-color: #FFFF00; color: #000 !important; border-radius: 2px; padding: 1px 3px; }
    .t-o { background-color: #FFA500; color: #000 !important; border-radius: 2px; padding: 1px 3px; }
    .t-r { background-color: #FF0000; color: #FFF !important; border-radius: 2px; padding: 1px 3px; animation: blinker 0.4s linear infinite; }
    .t-g { background-color: #00FF00; color: #000 !important; border-radius: 2px; padding: 1px 3px; animation: blinker 0.4s linear infinite; }
    .t-p { background-color: #8A2BE2; color: #FFF !important; border-radius: 2px; padding: 1px 3px; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 9px; width: 100%; text-align: center; text-transform: uppercase; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-yellow { background-color: #FFFF00; color: #000; }
    .bg-orange { background-color: #FFA500; color: #000; }
    .bg-blink-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .bg-blink-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    .bg-purple { background-color: #8A2BE2; color: #FFF; }
    </style>
    """, unsafe_allow_html=True)

# [AQUI CONTINUA O DICIONÁRIO 'assets' COM OS 80 ATIVOS E O LOOP 'while True' QUE JÁ FUNCIONA]
