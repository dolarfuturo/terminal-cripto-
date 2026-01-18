import streamlit as st
import pandas as pd
import time
import yfinance as yf
import random
import string
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO E DESIGN ALPHA
st.set_page_config(page_title="ALPHA VISION", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    input { background-color: #151515 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    section[data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #D4AF37; }
    .header-alpha { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 10px; color: #FFF; text-align: center; font-weight: bold; width: 11%; }
    .row-alpha { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #181818; }
    .c-ativo { width: 14%; padding-left: 10px; color: #FFF; font-size: 13px; font-weight: 700; }
    .c-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .c-val { width: 10%; text-align: center; font-size: 12px; font-weight: 700; }
    .bg-alert { background-color: #FFFF00; color: #000; border-radius: 2px; padding: 2px 4px; }
    .status-box { padding: 5px; border-radius: 3px; font-size: 9px; font-weight: 900; text-align: center; width: 90%; margin: auto; }
    .st-ok { background-color: #00CED1; color: #000; }
    .st-warn { background-color: #FFFF00; color: #000; }
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- AJUSTE: GERADOR DE SENHA SIMPLES NA LATERAL ---
with st.sidebar:
    st.markdown("<h3 style='color:#D4AF37;'>ALPHA ADMIN</h3>", unsafe_allow_html=True)
    st.write("Gerar acesso numérico:")
    if st.button("GERAR NOVA SENHA"):
        # Gera apenas 6 números (ex: 482931) - Simples para o cliente
        senha_simples = ''.join(random.choice(string.digits) for _ in range(6))
        st.code(senha_simples)
        st.caption("Copie para a sua planilha Google.")
    st.markdown("---")
    if st.button("LOGOUT / SAIR"):
        st.session_state.autenticado = False
        st.rerun()

# --- 2. LÓGICA DE LOGIN ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_users = conn.read(ttl=5)
    except: st.stop()
    st.markdown("<h1 style='text-align:center; color:#D4AF37;'>ALPHA VISION LOGIN</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.form("login_form"):
            u = st.text_input("USUÁRIO").strip()
            p = st.text_input("SENHA", type="password").strip()
            if st.form_submit_button("LIBERAR"):
                match = df_users[df_users['user'].astype(str) == str(u)]
                if not match.empty and str(p) == str(match.iloc[0]['password']):
                    st.session_state.autenticado = True
                    st.rerun()
                else: st.error("ACESSO NEGADO")
    st.stop()

# --- 3. TERMINAL VISÃO DE TUBARÃO ---
# Ativos organizados em lista para evitar erro de string (SyntaxError)
ativos_lista = [
    'BTC-USD','ETH-USD','SOL-USD','BNB-USD','XRP-USD','DOGE-USD','ADA-USD','AVAX-USD','DOT-USD','LINK-USD',
    'NEAR-USD','PEPE-USD','EGLD-USD','GALA-USD','FET-USD','SUI-USD','TIA-USD','AAVE-USD','RENDER-USD','INJ-USD'
]

st.markdown('<h2 style="color:#D4AF37; text-align:center; margin:0;">ALPHA VISION CRYPTO</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#C0C0C0; letter-spacing:4px; font-size:12px;">VISÃO DE TUBARÃO</p>', unsafe_allow_html=True)

painel = st.empty()

while True:
    try:
        # Puxa os dados com reset automático (00:00 UTC)
        dados = yf.download(ativos_lista, period="1d", interval="1m", group_by='ticker', silent=True)
        
        with painel.container():
            # Cabeçalho
            st.markdown('<div class="header-alpha"><div style="width:14%; color:#FFF; padding-left:10px; font-size:10px;">ATIVO</div><div class="h-col">PREÇO</div><div class="h-col">ALVO 4%</div><div class="h-col">ALVO 8%</div><div class="h-col">ALVO 10%</div><div class="h-col">SUP 4%</div><div class="h-col">SUP 8%</div><div class="h-col">SUP 10%</div><div class="h-col" style="width:14%;">SINAL</div></div>', unsafe_allow_html=True)

            for ticker_id in ativos_lista:
                try:
                    df_ticker = dados[ticker_id]
                    preco_atual = df_ticker['Close'].iloc[-1]
                    preco_abertura = df_ticker['Open'].iloc[0]
                    
                    # Cálculos de Alvos e Suportes
                    v4, v8, v10 = preco_abertura*1.04, preco_abertura*1.08, preco_abertura*1.10
                    c4, c8, c10 = preco_abertura*0.96, preco_abertura*0.92, preco_abertura*0.90
                    
                    # Lógica de Alerta Visual (Igual ao seu padrão)
                    txt_sinal, css_sinal, css_preco = "ESTÁVEL", "st-ok", ""
                    if preco_atual >= v4:
                        txt_sinal, css_sinal, css_preco = "DECISÃO ATENÇÃO", "st-warn", "bg-alert"

                    decimais = 4 if preco_atual < 10 else 2
                    nome_exibicao = ticker_id.replace("-USD", "/USDT")
                    
                    # Construção da linha (Fragmentada para evitar erros de sintaxe)
                    linha = f'<div class="row-alpha">'
                    linha += f'<div class="c-ativo">{nome_exibicao}</div>'
                    linha += f'<div class="c-price">{preco_atual:.{decimais}f}</div>'
                    linha += f'<div class="c-val" style="color:#FFFF00;"><span class="{css_preco}">{v4:.{decimais}f}</span></div>'
                    linha += f'<div class="c-val" style="color:#FFA500;">{v8:.{decimais}f}</div>'
                    linha += f'<div class="c-val" style="color:#FF0000;">{v10:.{decimais}f}</div>'
                    linha += f'<div class="c-val" style="color:#FFFF00;">{c4:.{decimais}f}</div>'
                    linha += f'<div class="c-val" style="color:#FFA500;">{c8:.{decimais}f}</div>'
                    linha += f'<div class="c-val" style="color:#00FF00;">{c10:.{decimais}f}</div>'
                    linha += f'<div style="width:14%;"><div class="status-box {css_sinal}">{txt_sinal}</div></div></div>'
                    
                    st.markdown(linha, unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: time.sleep(5)
