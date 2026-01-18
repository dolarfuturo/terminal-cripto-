import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. LOGIN (FUNDO PRETO)
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    .stMarkdown h1 { color: #D4AF37 !important; }
    label { color: #C0C0C0 !important; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=10)
except:
    st.error("Erro de conexão.")
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
                        st.session_state.autenticado = True
                        st.rerun()
                    else: st.error("Erro de login.")
    st.stop()

# 2. SEU CÓDIGO ORIGINAL (ESTRUTURA E CORES PRESERVADAS)
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

    /* CLASSES DE DESTAQUE NOS VALORES */
    .t-y { background-color: #FFFF00; color: #000 !important; border-radius: 2px; padding: 2px 4px; }
    .t-o { background-color: #FFA500; color: #000 !important; border-radius: 2px; padding: 2px 4px; }
    .t-blink-r { background-color: #FF0000; color: #FFF !important; animation: blinker 0.4s linear infinite; border-radius: 2px; padding: 2px 4px; }
    .t-blink-g { background-color: #00FF00; color: #000 !important; animation: blinker 0.4s linear infinite; border-radius: 2px; padding: 2px 4px; }
    .t-purple { background-color: #8A2BE2; color: #FFF !important; font-weight: 900; border-radius: 2px; padding: 2px 4px; }
    
    @keyframes blinker { 50% { opacity: 0.2; } }

    .status-box { padding: 8px 2
