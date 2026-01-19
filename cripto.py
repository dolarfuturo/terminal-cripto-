import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURAÇÃO ALPHA VISION
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .block-container { padding: 0rem 1rem !important; }
    header, footer { visibility: hidden; }
    
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; padding-top: 10px; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 16px; text-align: center; margin-top: -5px; letter-spacing: 7px; margin-bottom: 25px; font-weight: 700; }
    
    /* CABEÇALHO MAIOR */
    .header-container { display: flex; width: 100%; padding: 15px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 13px; color: #FFFFFF; text-transform: uppercase; text-align: center; font-weight: 800; letter-spacing: 1px; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 10px 0; border-bottom: 1px solid #151515; }
    
    /* NÚMEROS E TABELA */
    .w-ativo { width: 14%; text-align: left; padding-left: 10px; color: #EEE; font-size: 16px; font-weight: 700; }
    .w-price { width: 15%; text-align: center; color: #FF8C00; font-size: 18px; font-weight: 900; }
    .w-target { width: 9%; text-align: center; font-size: 14px; font-weight: 800; border-radius: 4px; padding: 6px 0; }
    .w-sinal { width: 14%; text-align: center; padding-right: 5px; }
    
    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 10px; width: 100%; text-align: center; text-transform: uppercase; }
    
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-decisao { background-color: #FFFF00 !important; color: #000 !important; font-weight: 900; }
    .bg-atencao { background-color: #FFA500 !important; color: #000 !important; font-weight: 900; }
    .bg-parabolica { background-color: #800080; color: #FFF; }
    
    .target-blink-red { background-color: #FF0000 !important; color: #FFF !important; animation: blinker 0.6s linear infinite; }
    .target-blink-green { background-color: #00FF00 !important; color: #000 !important; animation: blinker 0.6s linear infinite; }
    
    @keyframes blinker { 50% { opacity: 0.3; } }
    .perc-val { font-size: 12px; display: block; margin-top: 2px; font-weight: 600; }
    
    .footer-live { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #000; color: #00FF00; text-align: center; padding: 10px; font-size: 13px; font-weight: bold; border-top: 1px solid #333; z-index: 100; }

    /* BOTÃO SUPORTE LOGIN */
    .btn-suporte {
        display: inline-block;
        width: 100%;
        padding: 10px;
        background-color: #262626;
        color: white !important;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        border-radius: 5px;
        border: 1px solid #444;
        margin-top: 10px;
    }
    .btn-suporte:hover { background-color: #333; border-color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN E CONEXÃO
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def safe_connect():
    for i in range(3):
        try:
            st.cache_data.clear()
            conn = st.connection("gsheets", type=GSheetsConnection)
            return conn.read(ttl=0)
        except:
            time.sleep(1)
    return None

if not st.session_state.autenticado:
    st.markdown('<div class="title-gold">ALPHA VISION</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        if st.button("LIBERAR ACESSO", use_container_width=True):
            df_users = safe_connect()
            if df_users is not None:
                df_users.columns = [str(c).strip().lower() for c in df_users.columns]
                user_row = df_users[df_users['user'].astype(str) == u]
                if not user_row.empty and str(p) == str(user_row.iloc[0]['password']).strip():
                    st.session_state.autenticado = True
                    st.rerun()
                else: st.error("Acesso negado.")
            else: st.error("Erro de conexão.")
        
        # BOTÃO SUPORTE TELA DE LOGIN
        st.markdown(f'''<a href="https://t.me/+GOzXsBo0BchkMzYx" target="_blank" class="btn-suporte">SUPORTE</a>''', unsafe_allow_html=True)
    st.stop()

# 3. MONITORAMENTO
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'NEAR-USD':'NEAR/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT',
    'AAVE-USD':'AAVE/USDT','RENDER-USD':'RENDER/USDT','SUI-USD':'SUI/USDT','TIA-USD':'TIA/USDT','INJ-USD':'INJ/USDT',
    'MATIC-USD':'POL/USDT','SHIB-USD':'SHIB/USDT','LTC-USD':'LTC/USDT','BCH-USD':'BCH/USDT','APT-USD':'APT/USDT',
    'STX-USD':'STX/USDT','KAS-USD':'KAS/USDT','ARB-USD':'ARB/USDT','OP-USD':'OP/USDT','SEI-USD':'SEI/USDT',
    'FIL-USD':'FIL/USDT','HBAR-USD':'HBAR/USDT','ETC-USD':'ETC/USDT','ICP-USD':'ICP/USDT','BONK-USD':'BONK/USDT',
    'FLOKI-USD':'FLOKI/USDT','WIF-USD':'WIF/USDT','PYTH-USD':'PYTH/USDT','JUP-USD':'JUP/USDT','RAY-USD':'RAY/USDT',
    'ORDI-USD':'ORDI/USDT','BEAM-USD':'BEAM/USDT','IMX-USD':'IMX/USDT','GNS-USD':'GNS/USDT','DYDX-USD':'DYDX/USDT',
    'LDO-USD':'LDO/USDT','PENDLE-USD':'PENDLE/USDT','ENA-USD':'ENA/USDT','TRX-USD':'TRX/USDT','ATOM-USD':'ATOM/USDT',
    'MKR-USD':'MKR/USDT','GRT-USD':'GRT/USDT','THETA-USD':'THETA/USDT','FTM-USD':'FTM/USDT','VET-USD':'VET/USDT',
    'ALGO-USD':'ALGO/USDT','FLOW-USD':'FLOW/USDT','QNT-USD':'QNT/USDT','SNX-USD':'SNX/USDT','EOS-USD':'EOS/USDT',
    'NEO-USD':'NEO/USDT','IOTA-USD':'IOTA/USDT','CFX-USD':'CFX/USDT','AXS-USD':'AXS/USDT','MANA-USD':'MANA/USDT',
    'SAND-USD':'SAND/USDT','APE-USD':'APE/USDT','RUNE-USD':'RUNE/USDT','CHZ-USD':'CHZ/USDT','MINA-USD':'MINA/USDT',
    'ROSE-USD':'ROSE/USDT','WOO-USD':'WOO/USDT','ANKR-USD':'ANKR/USDT','1INCH-USD':'1INCH/USDT','ZIL-USD':'ZIL/USDT',
    'LRC-USD':'LRC/USDT','CRV-USD':'CRV/USDT','JASMY-USD':'JASMY/USDT','W-USD':'W/USDT','STRK-USD':'STRK/USDT'
}

placeholder = st.empty()

while True:
    try:
        data_batch = yf.download(list(assets.keys()), period="1d", interval="1m", group_by='ticker', progress=False)
        with placeholder.container():
            st.markdown("""<div class="header-container">
                <div class="h-col" style="width:14%; text-align:left; padding-left:10px;">ATIVO</div>
                <div class="h-col" style="width:15%;">PREÇO ATUAL</div>
                <div class="h-col" style="width:9%;">RESISTÊNCIA</div>
                <div class="h-col" style="width:9%;">PRÓX AO TOPO</div>
                <div class="h-col" style="width:9%;">TETO EXAUSTÃO</div>
                <div class="h-col" style="width:9%;">SUPORTE</div>
                <div class="h-col" style="width:9%;">PRÓX FUNDO</div>
                <div class="h-col" style="width:9%;">CHÃO EXAUSTÃO</div>
                <div class="h-col" style="width:14%;">SINALIZADOR</div></div>""", unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    df = data_batch[tid].dropna()
                    if df.empty: continue
                    price = float(df['Close'].iloc[-1])
                    open_p = float(df['Open'].iloc[0]) 
                    diff_pts = price - open_p
                    change_pct = (diff_pts / open_p) * 100
                    abs_c = abs(change_pct)
                    
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt, s_class, rh4, rh8, rh10 = "ESTÁVEL", "bg-estavel", "", "", ""
                    
                    if abs_c >= 12: s_txt, s_class = "PARABÓLICA", "bg-parabolica"
                    elif 10.0 <= abs_c <= 11.0:
                        s_txt, s_class = "EXAUSTÃO", ("target-blink-red" if change_pct > 0 else "target-blink-green")
                        rh10 = s_class
                    elif 8.0 <= abs_c <= 9.0: s_txt, s_class, rh8 = "PRÓX TOPO", "bg-atencao", "bg-atencao"
                    elif 4.0 <= abs_c <= 5.0: s_txt, s_class, rh4 = "REGIÃO DE DECISÃO", "bg-decisao", "bg-decisao"

                    arrow = "▲" if change_pct >= 0 else "▼"
                    t_color = "#00FF00" if change_pct >= 0 else "#FF0000"

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="w-ativo">{name}</div>
                            <div class="w-price">{price:.3f} <span style="color:{t_color}; font-size:14px;">{arrow}</span>
                                <span class="perc-val" style="color:{t_color};">{diff_pts:+.3f} ({change_pct:+.2f}%)</span></div>
                            <div class="w-target {rh4 if (change_pct > 0 and rh4) else ''}" style="color:#FFFF00;">{v4:.3f}</div>
                            <div class="w-target {rh8 if (change_pct > 0 and rh8) else ''}" style="color:#FFA500;">{v8:.3f}</div>
                            <div class="w-target {rh10 if (change_pct > 0 and rh10) else ''}" style="color:#FF0000;">{v10:.3f}</div>
                            <div class="w-target {rh4 if (change_pct < 0 and rh4) else ''}" style="color:#FFFF00;">{c4:.3f}</div>
                            <div class="w-target {rh8 if (change_pct < 0 and rh8) else ''}" style="color:#FFA500;">{c8:.3f}</div>
                            <div class="w-target {rh10 if (change_pct < 0 and rh10) else ''}" style="color:#00FF00;">{c10:.3f}</div>
                            <div class="w-sinal"><div class="status-box {s_class}">{s_txt}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
                except: continue
            
            st.markdown('<div class="footer-live">🟢 LIVE STREAM / ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
            
        time.sleep(10)
    except: time.sleep(5)
