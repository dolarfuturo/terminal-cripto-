import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - CONFIGURAÇÃO ÚNICA
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

def apply_custom_css():
    st.markdown("""
        <style>
        .stApp { background-color: #000000; }
        .title-container { text-align: center; padding: 15px; }
        .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; }
        .subtitle-white { color: #FFFFFF; font-size: 16px; font-weight: 300; letter-spacing: 5.5px; margin-top: 2px; text-transform: lowercase; }
        .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; }
        .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
        .row-container { display: flex; width: 100%; align-items: center; padding: 25px 0; border-bottom: 1px solid #151515; justify-content: space-between; }
        .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; white-space: nowrap; }
        .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 13px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 35px; z-index: 1000; }
        .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
        </style>
        """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO UNIFICADO
def get_midpoint(ticker_symbol="BTC-USD"):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        # Reset automático conforme solicitado (00:00 UTC / 21:00 BRT ou 18:00 dependendo da janela)
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download(ticker_symbol, start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not df.empty:
            df.index = df.index.tz_convert(br_tz)
            df_window = df.between_time('11:30', '18:00')
            if not df_window.empty:
                return int((df_window['High'].max() + df_window['Low'].min()) / 2)
        return 82632 if "BTC" in ticker_symbol else 2500
    except Exception:
        return 82632 if "BTC" in ticker_symbol else 2500

# 3. INTERFACE E LOGICA DE EXECUÇÃO
apply_custom_css()

st.markdown("""
    <div class="title-container">
        <div class="title-gold">ALPHA VISION CRYPTO</div>
        <div class="subtitle-white">visão de tubarão</div>
    </div>
    """, unsafe_allow_html=True)

# Inicialização de Estado
if 'mp_current' not in st.session_state:
    st.session_state.mp_current = get_midpoint("BTC-USD")
    st.session_state.rv_fixed = st.session_state.mp_current

placeholder = st.empty()

# LOOP PRINCIPAL
while True:
    try:
        br_tz, ny_tz, lon_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York'), pytz.timezone('Europe/London')
        now_br = datetime.now(br_tz)
        
        # Auto-Reset Binance (21:00 BRT p/ 00:00 UTC ou conforme sua regra de 18:00)
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 5:
            st.session_state.mp_current = get_midpoint("BTC-USD")
            st.session_state.rv_fixed = st.session_state.mp_current
            st.rerun()

        # Dados em Tempo Real
        ticker = yf.Ticker("BTC-USD")
        price = ticker.fast_info['last_price']
        mp = st.session_state.mp_current
        var = ((price / mp) - 1) * 100

        # Lógica de Escada
        if var >= 1.35:
            st.session_state.mp_current = int(mp * 1.0122)
            st.rerun()
        elif var <= -1.35:
            st.session_state.mp_current = int(mp * 0.9878)
            st.rerun()

        # Renderização
        with placeholder.container():
            abs_var = abs(var)
            rv_valor = st.session_state.rv_fixed
            var_reset = ((price / rv_valor) - 1) * 100
            
            cor_v = "#00FF00" if var_reset >= 0 else "#FF4444"
            seta_v = "▲" if var_reset >= 0 else "▼"
            
            fundo_decisao = "background: rgba(255, 255, 0, 0.3);" if 0.59 <= abs_var <= 0.65 else ""
            estilo_ex_t = "color: #FF4444; animation: blink 0.4s infinite;" if (1.20 <= var < 1.35) else "color: #FF4444;"
            estilo_ex_f = "color: #00FF00; animation: blink 0.4s infinite;" if (-1.35 < var <= -1.20) else "color: #00FF00;"

            st.markdown(f"""
                <div class="header-container">
                    <div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div>
                    <div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                    <div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div>
                    <div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div>
                </div>
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37; font-weight:bold;">BTC/USDT</div>
                    <div class="w-col">
                        <div style="font-weight: bold;">{int(price):,}</div>
                        <div style="color:{cor_v}; font-size:11px;">{seta_v} {var_reset:+.2f}%</div>
                    </div>
                    <div class="w-col" style="{estilo_ex_t}">{int(mp*1.0122):,}</div>
                    <div class="w-col" style="color:#FFA500;">{int(mp*1.0083):,}</div>
                    <div class="w-col" style="{fundo_decisao}">{int(mp*1.0061):,}</div>
                    <div class="w-col" style="color:#00CED1;">{int(mp*1.0040):,}</div>
                    <div class="w-col" style="color:#FFA500;">{int(mp*0.9939):,}</div>
                    <div class="w-col" style="{estilo_ex_f}">{int(mp*0.9878):,}</div>
                </div>
                <div class="footer">
                    <div><span class="dot"></span> LIVE</div>
                    <div>ÂNCORA: <span style="color:#FFA500;">{int(mp):,}</span></div>
                    <div>BR: {datetime.now(br_tz).strftime('%H:%M:%S')}</div>
                    <div>NY: {datetime.now(ny_tz).strftime('%H:%M:%S')}</div>
                </div>
            """, unsafe_allow_html=True)
            
        time.sleep(1)
    except Exception as e:
        time.sleep(5)
