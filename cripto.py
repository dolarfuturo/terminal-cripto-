import streamlit as st
import pandas as pd
import yfinance as yf
import random, string, time
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="ALPHA VISION", layout="wide", initial_sidebar_state="collapsed")

# Estilo Simplificado para evitar erro de renderização
st.markdown("""<style>
    .stApp { background-color: #000; font-family: monospace; }
    input { background-color: #111 !important; color: gold !important; border: 1px solid #D4AF37 !important; }
    .title { color: #D4AF37; text-align: center; font-size: 28px; font-weight: bold; }
    .header-table { display: flex; border-bottom: 2px solid #D4AF37; background: #080808; padding: 10px 0; }
    .h-col { font-size: 9px; color: #FFF; text-align: center; width: 11%; font-weight: bold; }
    .row-alpha { display: flex; align-items: center; padding: 5px 0; border-bottom: 1px solid #111; }
    .c-ativo { width: 14%; padding-left: 10px; color: #FFF; font-size: 12px; }
    .c-price { width: 12%; text-align: center; color: #FF8C00; font-weight: bold; }
    .c-val { width: 10%; text-align: center; font-size: 11px; }
    .bg-yellow { background-color: #FFFF00; color: #000; padding: 1px 3px; border-radius: 2px; }
    .st-box { padding: 4px; border-radius: 3px; font-size: 9px; font-weight: bold; text-align: center; width: 90%; margin: auto; }
</style>""", unsafe_allow_html=True)

# 1. GERADOR DE SENHA (SIDEBAR)
with st.sidebar:
    st.title("ALPHA ADMIN")
    if st.button("GERAR SENHA NUMÉRICA"):
        senha = ''.join(random.choice(string.digits) for _ in range(6))
        st.code(senha)
    if st.button("LOGOUT"):
        st.session_state.autenticado = False
        st.rerun()

# 2. LOGIN
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if not st.session_state.autenticado:
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=5)
    except: st.stop()
    st.markdown("<div class='title'>ALPHA VISION LOGIN</div>", unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("USUÁRIO").strip()
        p = st.text_input("SENHA", type="password").strip()
        if st.form_submit_button("ENTRAR"):
            match = df[df['user'].astype(str) == str(u)]
            if not match.empty and str(p) == str(match.iloc[0]['password']):
                st.session_state.autenticado = True
                st.rerun()
            else: st.error("Erro nos dados")
    st.stop()

# 3. TERMINAL (80 ATIVOS - FORMATO CURTO)
t_list = [
    'BTC-USD','ETH-USD','SOL-USD','BNB-USD','XRP-USD','ADA-USD','AVAX-USD','DOT-USD','LINK-USD','NEAR-USD',
    'MATIC-USD','PEPE-USD','EGLD-USD','GALA-USD','FET-USD','SUI-USD','TIA-USD','AAVE-USD','RENDER-USD','INJ-USD',
    'SHIB-USD','LTC-USD','BCH-USD','APT-USD','STX-USD','KAS-USD','ARB-USD','OP-USD','SEI-USD','FIL-USD',
    'HBAR-USD','ETC-USD','ICP-USD','BONK-USD','FLOKI-USD','WIF-USD','PYTH-USD','JUP-USD','RAY-USD','ORDI-USD'
]

st.markdown("<div class='title'>ALPHA VISION CRYPTO</div>", unsafe_allow_html=True)
monitor = st.empty()

while True:
    try:
        data = yf.download(t_list, period="1d", interval="1m", group_by='ticker', silent=True)
        with monitor.container():
            st.markdown('<div class="header-table"><div style="width:14%; color:white; padding-left:10px;">ATIVO</div><div class="h-col">PREÇO</div><div class="h-col">ALVO 4%</div><div class="h-col">ALVO 8%</div><div class="h-col">ALVO 10%</div><div class="h-col">SUP 4%</div><div class="h-col">SUP 8%</div><div class="h-col">SUP 10%</div><div class="h-col" style="width:14%;">SINAL</div></div>', unsafe_allow_html=True)
            for tid in t_list:
                try:
                    tick = data[tid]
                    p_atual = tick['Close'].iloc[-1]
                    p_open = tick['Open'].iloc[0] # Reset 00:00 UTC
                    v4, v8, v10 = p_open*1.04, p_open*1.08, p_open*1.10
                    c4, c8, c10 = p_open*0.96, p_open*0.92, p_open*0.90
                    
                    s_txt, s_bg, p_style = "ESTÁVEL", "background:#00CED1", ""
                    if p_atual >= v4: s_txt, s_bg, p_style = "ALERTA", "background:#FFFF00", "class='bg-yellow'"
                    
                    dec = 4 if p_atual < 10 else 2
                    row = f"""<div class="row-alpha">
                        <div class="c-ativo">{tid.replace('-USD','/T')}</div>
                        <div class="c-price">{p_atual:.{dec}f}</div>
                        <div class="c-val" style="color:#FFFF00;"><span {p_style}>{v4:.{dec}f}</span></div>
                        <div class="c-val" style="color:#FFA500;">{v8:.{dec}f}</div>
                        <div class="c-val" style="color:#FF0000;">{v10:.{dec}f}</div>
                        <div class="c-val" style="color:#FFFF00;">{c4:.{dec}f}</div>
                        <div class="c-val" style="color:#FFA500;">{c8:.{dec}f}</div>
                        <div class="c-val" style="color:#00FF00;">{c10:.{dec}f}</div>
                        <div style="width:14%;"><div class="st-box" style="{s_bg}; color:#000;">{s_txt}</div></div>
                    </div>"""
                    st.markdown(row, unsafe_allow_html=True)
                except: continue
        time.sleep(15)
    except: time.sleep(5)
