import streamlit as st
import pandas as pd
import time
import yfinance as yf
import secrets
import string
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

# ==========================================
# CONFIGURAÇÃO DE INTERFACE & CSS
# ==========================================
st.set_page_config(page_title="ALPHA VISION PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    header {visibility: hidden;}
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    .title-gold { color: #D4AF37; font-size: 42px; font-weight: 900; text-align: center; padding: 20px 0 5px 0; }
    .subtitle-vision { color: #C0C0C0; font-size: 14px; text-align: center; letter-spacing: 8px; margin-bottom: 20px; text-transform: uppercase; }
    
    .header-container { display: flex; width: 100%; padding: 15px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 10px; font-weight: 700; color: #FFF; text-align: center; text-transform: uppercase; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 8px 0; border-bottom: 1px solid #1A1A1A; }
    .w-ativo { width: 14%; padding-left: 15px; color: #EEE; font-size: 14px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 16px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 13px; font-weight: 700; }
    
    .t-y { background-color: #FFFF00; color: #000; border-radius: 2px; padding: 2px 5px; }
    .t-o { background-color: #FFA500; color: #000; border-radius: 2px; padding: 2px 5px; }
    .t-blink-r { background-color: #FF0000; color: #FFF; animation: blinker 0.5s linear infinite; border-radius: 2px; padding: 2px 5px; }
    .t-blink-g { background-color: #00FF00; color: #000; animation: blinker 0.5s linear infinite; border-radius: 2px; padding: 2px 5px; }
    
    @keyframes blinker { 50% { opacity: 0.1; } }

    .status-box { padding: 6px; border-radius: 3px; font-weight: 900; font-size: 10px; width: 90%; text-align: center; margin: auto; }
    .bg-estavel { background-color: #1A1A1A; color: #555; border: 1px solid #333; }
    .bg-yellow { background-color: #FFFF00; color: #000; }
    .bg-orange { background-color: #FFA500; color: #000; }
    .bg-red { background-color: #FF0000; color: #FFF; animation: blinker 0.5s linear infinite; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# CONEXÃO E GESTÃO DE ACESSOS
# ==========================================
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_users = conn.read(ttl=10)
except:
    st.error("Erro de conexão com a Base de Dados.")
    st.stop()

if 'auth' not in st.session_state: st.session_state.auth = False

# TELA DE LOGIN
if not st.session_state.auth:
    st.markdown('<div class="title-gold">ALPHA VISION</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-vision">Terminal Restrito</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        with st.form("login"):
            u = st.text_input("USUÁRIO")
            p = st.text_input("SENHA", type="password")
            if st.form_submit_button("LIBERAR ACESSO"):
                user_row = df_users[df_users['user'] == u]
                if not user_row.empty:
                    if p == str(user_row.iloc[0]['password']):
                        venc = pd.to_datetime(user_row.iloc[0]['vencimento']).date()
                        if datetime.now().date() <= venc:
                            st.session_state.auth = True
                            st.session_state.user = u
                            st.rerun()
                        else: st.error("⚠️ ACESSO EXPIRADO.")
                    else: st.error("❌ SENHA INCORRETA.")
                else: st.error("❌ USUÁRIO NÃO ENCONTRADO.")
    st.stop()

# PAINEL DO DONO (SIDEBAR)
with st.sidebar:
    st.write(f"Operador: **{st.session_state.user}**")
    if st.button("SAIR"): 
        st.session_state.auth = False
        st.rerun()
    
    st.divider()
    admin_pw = st.text_input("Área Admin (Senha)", type="password")
    if admin_pw == "mestrealpha2026":
        st.subheader("Gerar Novo Cliente")
        nome = st.text_input("Nome Cliente")
        dias = st.slider("Dias", 1, 365, 30)
        if st.button("GERAR ACESSO"):
            nova_pw = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(6))
            data_v = (datetime.now() + timedelta(days=dias)).strftime('%Y-%m-%d')
            msg = f"Acesso Alpha Vision:\nUser: {nome}\nPass: {nova_pw}\nVenc: {data_v}"
            st.code(msg)
            st.info("Copie e cole os dados acima na sua Planilha Google agora.")

# ==========================================
# LOOP DO TERMINAL (80 ATIVOS)
# ==========================================
assets = {
    'BTC-USD':'BTC/USDT', 'ETH-USD':'ETH/USDT', 'SOL-USD':'SOL/USDT', 'BNB-USD':'BNB/USDT',
    'XRP-USD':'XRP/USDT', 'ADA-USD':'ADA/USDT', 'AVAX-USD':'AVAX/USDT', 'DOT-USD':'DOT/USDT',
    'LINK-USD':'LINK/USDT', 'NEAR-USD':'NEAR/USDT', 'MATIC-USD':'POL/USDT', 'PEPE-USD':'PEPE/USDT'
    # Adicione as demais aqui...
}

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">Sincronizado Binance 00:00 UTC</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    tickers = yf.Tickers(' '.join(assets.keys()))
    with placeholder.container():
        st.markdown("""
            <div class="header-container">
                <div class="h-col" style="width:14%; text-align:left; padding-left:15px;">ATIVO</div>
                <div class="h-col" style="width:12%;">PREÇO</div>
                <div class="h-col" style="width:10%;">ALVO 4%</div>
                <div class="h-col" style="width:10%;">ALVO 8%</div>
                <div class="h-col" style="width:10%;">ALVO 10%</div>
                <div class="h-col" style="width:10%;">SUP 4%</div>
                <div class="h-col" style="width:10%;">SUP 8%</div>
                <div class="h-col" style="width:10%;">SUP 10%</div>
                <div class="h-col" style="width:14%;">SINAL</div>
            </div>
        """, unsafe_allow_html=True)

        for tid, name in assets.items():
            try:
                data = tickers.tickers[tid].fast_info
                price = data.last_price
                open_p = data.open
                change = ((price - open_p) / open_p) * 100
                
                # Alvos de Simetria
                v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                s4, s8, s10 = open_p*0.96, open_p*0.92, open_p*0.90
                
                status, s_class = "ESTÁVEL", "bg-estavel"
                c4, c8, c10, cs4, cs8, cs10 = "", "", "", "", "", ""

                if change >= 10: status, s_class, c10 = "EXAUSTÃO", "bg-red", "t-blink-r"
                elif change >= 8: status, s_class, c8 = "VOL. ALTA", "bg-orange", "t-o"
                elif change >= 4: status, s_class, c4 = "ATENÇÃO", "bg-yellow", "t-y"
                elif change <= -10: status, s_class, cs10 = "EXAUSTÃO", "bg-red", "t-blink-g"
                elif change <= -8: status, s_class, cs8 = "VOL. ALTA", "bg-orange", "t-o"
                elif change <= -4: status, s_class, cs4 = "ATENÇÃO", "bg-yellow", "t-y"

                p_dec = 2 if price > 1 else 6
                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-ativo">{name}</div>
                        <div class="w-price">{price:.{p_dec}f}<br><span style="font-size:10px;">{change:+.2f}%</span></div>
                        <div class="w-target" style="color:#FFFF00;"><span class="{c4}">{v4:.{p_dec}f}</span></div>
                        <div class="w-target" style="color:#FFA500;"><span class="{c8}">{v8:.{p_dec}f}</span></div>
                        <div class="w-target" style="color:#FF0000;"><span class="{c10}">{v10:.{p_dec}f}</span></div>
                        <div class="w-target" style="color:#FFFF00;"><span class="{cs4}">{s4:.{p_dec}f}</span></div>
                        <div class="w-target" style="color:#FFA500;"><span class="{cs8}">{s8:.{p_dec}f}</span></div>
                        <div class="w-target" style="color:#00FF00;"><span class="{cs10}">{s10:.{p_dec}f}</span></div>
                        <div class="w-target" style="width:14%;"><div class="status-box {s_class}">{status}</div></div>
                    </div>
                """, unsafe_allow_html=True)
            except: continue
    time.sleep(10)
