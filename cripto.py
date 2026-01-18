import streamlit as st
import pandas as pd
import time
import yfinance as yf
import random
import string
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO DE TELA
st.set_page_config(page_title="ALPHA VISION PRO", layout="wide", initial_sidebar_state="collapsed")

# CSS EM LINHAS ÚNICAS PARA EVITAR ERRO DE STRING NO SERVIDOR
st.markdown('<style>.stApp { background-color: #000000; font-family: monospace; }</style>', unsafe_allow_html=True)
st.markdown('<style>header, footer { visibility: hidden; }</style>', unsafe_allow_html=True)
st.markdown('<style>input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }</style>', unsafe_allow_html=True)
st.markdown('<style>section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #D4AF37; }</style>', unsafe_allow_html=True)
st.markdown('<style>.title-gold { color: #D4AF37; font-size: 30px; font-weight: 900; text-align: center; }</style>', unsafe_allow_html=True)
st.markdown('<style>.header-alpha { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background: #080808; position: sticky; top: 0; z-index: 99; }</style>', unsafe_allow_html=True)
st.markdown('<style>.h-col { font-size: 10px; color: #FFF; text-align: center; width: 11%; font-weight: bold; }</style>', unsafe_allow_html=True)
st.markdown('<style>.row-alpha { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; }</style>', unsafe_allow_html=True)
st.markdown('<style>.c-ativo { width: 14%; padding-left: 10px; color: #FFF; font-size: 13px; font-weight: 700; }</style>', unsafe_allow_html=True)
st.markdown('<style>.c-price { width: 12%; text-align: center; color: #FF8C00; font-size: 14px; font-weight: 900; }</style>', unsafe_allow_html=True)
st.markdown('<style>.c-val { width: 10%; text-align: center; font-size: 12px; font-weight: 700; }</style>', unsafe_allow_html=True)
st.markdown('<style>.bg-y { background-color: #FFFF00; color: #000; border-radius: 2px; padding: 1px 3px; }</style>', unsafe_allow_html=True)
st.markdown('<style>.st-box { padding: 6px; border-radius: 2px; font-size: 9px; font-weight: 900; text-align: center; width: 90%; margin: auto; }</style>', unsafe_allow_html=True)

# --- SIDEBAR COM GERADOR DE SENHA SIMPLES ---
with st.sidebar:
    st.markdown('<h3 style="color:#D4AF37;">ALPHA ADMIN</h3>', unsafe_allow_html=True)
    if st.button("GERAR NOVA SENHA"):
        # Gera 6 números aleatórios
        acesso = ''.join(random.choice(string.digits) for _ in range(6))
        st.code(acesso)
    st.markdown('---')
    if st.button("LOGOUT"):
        st.session_state.autenticado = False
        st.rerun()

# --- SISTEMA DE LOGIN ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_users = conn.read(ttl=5)
    except:
        st.error("Erro na Planilha")
        st.stop()

    st.markdown('<div class="title-gold">ALPHA VISION LOGIN</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.form("login_f"):
            u = st.text_input("USUÁRIO").strip()
            p = st.text_input("SENHA", type="password").strip()
            if st.form_submit_button("ENTRAR"):
                match = df_users[df_users['user'].astype(str) == u]
                if not match.empty and str(p) == str(match.iloc[0]['password']):
                    st.session_state.autenticado = True
                    st.rerun()
                else: st.error("Incorreto")
    st.stop()

# --- TERMINAL ALPHA (ESTRUTURA SEM ASPAS TRIPLAS PARA EVITAR TELA PRETA) ---
assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'NEAR-USD':'NEAR/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT',
    'SUI-USD':'SUI/USDT','TIA-USD':'TIA/USDT','AAVE-USD':'AAVE/USDT','RENDER-USD':'RENDER/USDT','INJ-USD':'INJ/USDT'
}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; color:#C0C0C0; letter-spacing:5px; font-size:12px;">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

painel = st.empty()

while True:
    try:
        # Puxa dados considerando abertura 00:00 UTC
        data = yf.download(list(assets.keys()), period="1d", interval="1m", group_by='ticker', silent=True)
        
        with painel.container():
            # Cabeçalho da Tabela
            st.markdown('<div class="header-alpha"><div style="width:14%; color:#FFF; padding-left:10px; font-size:10px;">ATIVO</div><div class="h-col">PREÇO</div><div class="h-col">ALVO 4%</div><div class="h-col">ALVO 8%</div><div class="h-col">ALVO 10%</div><div class="h-col">SUP 4%</div><div class="h-col">SUP 8%</div><div class="h-col">SUP 10%</div><div class="h-col" style="width:14%;">SINAL</div></div>', unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    df_ticker = data[tid]
                    price = df_ticker['Close'].iloc[-1]
                    open_p = df_ticker['Open'].iloc[0] # RESET AUTOMÁTICO BINANCE 00:00 UTC
                    
                    change = ((price - open_p) / open_p) * 100
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt, s_bg, p_class = "ESTÁVEL", "background-color:#00CED1; color:#000;", ""
                    if price >= v4: s_txt, s_bg, p_class = "DECISÃO ATENÇÃO", "background-color:#FFFF00; color:#000;", "bg-y"

                    dec = 4 if price < 10 else 2
                    
                    # MONTAGEM DA LINHA SEM ASPAS TRIPLAS (PARA NÃO DAR ERRO DE SINTAXE)
                    row = '<div class="row-alpha">'
                    row += '<div class="c-ativo">' + name + '</div>'
                    row += '<div class="c-price">' + f'{price:.{dec}f}' + '</div>'
                    row += '<div class="c-val" style="color:#FFFF00;"><span class="' + p_class + '">' + f'{v4:.{dec}f}' + '</span></div>'
                    row += '<div class="c-val" style="color:#FFA500;">' + f'{v8:.{dec}f}' + '</div>'
                    row += '<div class="c-val" style="color:#FF0000;">' + f'{v10:.{dec}f}' + '</div>'
                    row += '<div class="c-val" style="color:#FFFF00;">' + f'{c4:.{dec}f}' + '</div>'
                    row += '<div class="c-val" style="color:#FFA500;">' + f'{c8:.{dec}f}' + '</div>'
                    row += '<div class="c-val" style="color:#00FF00;">' + f'{c10:.{dec}f}' + '</div>'
                    row += '<div style="width:14%;"><div class="st-box" style="' + s_bg + '">' + s_txt + '</div></div></div>'
                    
                    st.markdown(row, unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: time.sleep(5)
