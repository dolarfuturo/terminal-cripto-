import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO E TRAVA DE LOGIN (FUNDO PRETO)
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
                        st.session_state.autenticado = True
                        st.rerun()
                    else: st.error("Acesso Negado.")
    st.stop()

# 2. LAYOUT VISÃO DE TUBARÃO COM CORES NOS VALORES
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    header {visibility: hidden;}
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 16px; text-align: center; letter-spacing: 7px; margin-bottom: 15px; }
    
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 11px; color: #FFFFFF; text-align: center; flex: 1; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; }
    .w-col { flex: 1; text-align: center; font-size: 14px; }

    /* Estilos de destaque para as células de valores */
    .val-y { background-color: #FFFF00; color: #000 !important; font-weight: 900; border-radius: 2px; padding: 2px 4px; }
    .val-o { background-color: #FFA500; color: #000 !important; font-weight: 900; border-radius: 2px; padding: 2px 4px; }
    .val-r { background-color: #FF0000; color: #FFF !important; font-weight: 900; border-radius: 2px; padding: 2px 4px; animation: blinker 0.4s linear infinite; }
    .val-g { background-color: #00FF00; color: #000 !important; font-weight: 900; border-radius: 2px; padding: 2px 4px; animation: blinker 0.4s linear infinite; }
    .val-p { background-color: #8A2BE2; color: #FFF !important; font-weight: 900; border-radius: 2px; padding: 2px 4px; }

    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 9px; width: 90%; margin: 0 auto; text-transform: uppercase; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

assets = {'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT','NEAR-USD':'NEAR/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT','AAVE-USD':'AAVE/USDT','RENDER-USD':'RENDER/USDT','TIA-USD':'TIA/USDT','INJ-USD':'INJ/USDT','SHIB-USD':'SHIB/USDT'}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        tickers = yf.Tickers(' '.join(assets.keys()))
        with placeholder.container():
            st.markdown('<div class="header-container"><div class="h-col">ATIVO</div><div class="h-col">PREÇO</div><div class="h-col">RESISTÊNCIA</div><div class="h-col">PRÓX TOPO</div><div class="h-col">TETO</div><div class="h-col">SUPORTE</div><div class="h-col">PRÓX FUNDO</div><div class="h-col">CHÃO</div><div class="h-col">SINAL</div></div>', unsafe_allow_html=True)

            for tid, name in assets.items():
                info = tickers.tickers[tid].fast_info
                price = info.last_price
                open_p = info.open
                change = ((price - open_p) / open_p) * 100
                
                # Alvos
                v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                
                s_txt, s_class = "ESTÁVEL", "background-color: #00CED1; color: #000;"
                v4_s, v8_s, v10_s, c4_s, c8_s, c10_s = "", "", "", "", "", ""

                # Lógica de Cores nos valores e no sinalizador
                if change >= 15: s_txt, s_class, v10_s = "ALTA PARABÓLICA", "background-color:#8A2BE2; color:#FFF;", "val-p"
                elif change >= 10: s_txt, s_class, v10_s = "EXAUSTÃO MÁXIMA", "background-color:#FF0000; color:#FFF; animation: blinker 0.4s linear infinite;", "val-r"
                elif price >= v8: s_txt, s_class, v8_s = "CUIDADO ALTA VOL", "background-color:#FFA500; color:#000;", "val-o"
                elif price >= v4: s_txt, s_class, v4_s = "DECISÃO ATENÇÃO", "background-color:#FFFF00; color:#000;", "val-y"
                elif change <= -15: s_txt, s_class, c10_s = "QUEDA PARABÓLICA", "background-color:#8A2BE2; color:#FFF;", "val-p"
                elif change <= -10: s_txt, s_class, c10_s = "EXAUSTÃO MÁXIMA", "background-color:#00FF00; color:#000; animation: blinker 0.4s linear infinite;", "val-g"
                elif price <= c8: s_txt, s_class, c8_s = "CUIDADO ALTA VOL", "background-color:#FFA500; color:#000;", "val-o"
                elif price <= c4: s_txt, s_class, c4_s = "DECISÃO ATENÇÃO", "background-color:#FFFF00; color:#000;", "val-y"

                prec = 6 if price < 0.1 else (4 if price < 10 else 2)
                
                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="text-align:left; padding-left:10px; font-weight:700;">{name}</div>
                        <div class="w-col" style="color:#FF8C00; font-weight:900;">{price:.{prec}f}<br><span style="font-size:9px;">{change:+.2f}%</span></div>
                        <div class="w-col" style="color:#FFFF00;"><span class="{v4_s}">{v4:.{prec}f}</span></div>
                        <div class="w-col" style="color:#FFA500;"><span class="{v8_s}">{v8:.{prec}f}</span></div>
                        <div class="w-col" style="color:#FF0000;"><span class="{v10_s}">{v10:.{prec}f}</span></div>
                        <div class="w-col" style="color:#FFFF00;"><span class="{c4_s}">{c4:.{prec}f}</span></div>
                        <div class="w-col" style="color:#FFA500;"><span class="{c8_s}">{c8:.{prec}f}</span></div>
                        <div class="w-col" style="color:#00FF00;"><span class="{c10_s}">{c10:.{prec}f}</span></div>
                        <div class="w-col"><div class="status-box" style="{s_class}">{s_txt}</div></div>
                    </div>
                """, unsafe_allow_html=True)
        time.sleep(10)
    except: time.sleep(10)
