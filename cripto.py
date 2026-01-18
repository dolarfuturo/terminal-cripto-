import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. LOGIN E CONFIGURAÇÃO
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    .stMarkdown h1 { color: #D4AF37 !important; }
    label { color: #C0C0C0 !important; }
    div[data-testid="stForm"] { background-color: #050505; border: 1px solid #151515; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=10)
    df_users.columns = [str(c).strip().lower() for c in df_users.columns]
except:
    st.error("Erro de conexão com a base de dados.")
    st.stop()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align:center;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    with st.container():
        left, mid, right = st.columns([1, 2, 1])
        with mid:
            with st.form("login_form"):
                u = st.text_input("USUÁRIO").strip()
                p = st.text_input("SENHA", type="password").strip()
                if st.form_submit_button("LIBERAR ACESSO"):
                    user_row = df_users[df_users['user'].astype(str) == u]
                    if not user_row.empty and str(p) == str(user_row.iloc[0]['password']).strip():
                        # TRAVA DE VENCIMENTO E STATUS
                        data_venc = pd.to_datetime(user_row.iloc[0]['vencimento']).date()
                        hoje = datetime.now().date()
                        status = str(user_row.iloc[0]['status']).strip().lower()
                        
                        if status != 'ativo':
                            st.error("CONTA INATIVA. FALE COM O SUPORTE.")
                        elif hoje > data_venc:
                            st.error(f"ACESSO EXPIRADO EM {data_venc.strftime('%d/%m/%Y')}")
                            st.markdown("<a href='https://wa.me/SEUNUMERO' target='_blank'><button style='width:100%; background-color:#D4AF37; color:black; border:none; padding:10px; font-weight:bold; cursor:pointer;'>FALAR COM SUPORTE PARA RENOVAR</button></a>", unsafe_allow_html=True)
                        else:
                            st.session_state.autenticado = True
                            st.rerun()
                    else: st.error("Usuário ou senha incorretos.")
    st.stop()

# 2. TERMINAL VISÃO DE TUBARÃO (80 ATIVOS + LAYOUT ORIGINAL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    header, footer {visibility: hidden;}
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; padding-top: 10px; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 16px; text-align: center; margin-top: -5px; letter-spacing: 7px; margin-bottom: 15px; font-weight: 700; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 11px; font-weight: 400; color: #FFFFFF; text-transform: uppercase; text-align: center; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; }
    .w-ativo { width: 14%; text-align: left; padding-left: 10px; color: #EEE; font-size: 14px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 14px; font-weight: 800; }
    .w-sinal { width: 14%; text-align: center; padding-right: 5px; }
    .t-y { background-color: #FFFF00; color: #000 !important; border-radius: 2px; padding: 1px 3px; }
    .t-o { background-color: #FFA500; color: #000 !important; border-radius: 2px; padding: 1px 3px; }
    .t-r { background-color: #FF0000; color: #FFF !important; border-radius: 2px; padding: 1px 3px; animation: blinker
