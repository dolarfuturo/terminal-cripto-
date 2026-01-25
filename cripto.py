import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 32px; font-weight: 900; text-align: center; padding: 10px; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; }
    .h-col { font-size: 11px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 20px 0; border-bottom: 1px solid #151515; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; }
    
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 10px; font-size: 14px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 25px; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; box-shadow: 0 0 10px #00FF00; animation: blink 1s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    
    .reset-alert { background-color: #D4AF37; color: #000; text-align: center; font-weight: 900; padding: 5px; font-size: 14px; position: fixed; top: 0; width: 100%; z-index: 1000; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO (TRAVADO NO SEU DADO)
def get_alpha_eixo_final():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        
        # Sábado, Domingo e Segunda (até 18h) -> Eixo Fixo Validado
        if now_br.weekday() >= 5 or (now_br.weekday() == 0 and now_br.hour < 18):
            return 89792.500
            
        # Reset Automático Diário pós 18h
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download("BTC-USD", start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_janela = df.between_time('11:30', '18:00')
        
        if not df_janela.empty:
            return (float(df_janela['High'].max()) + float(df_janela['Low'].min())) / 2
        return 89792.500
    except:
        return 89792.500

# 3. INTERFACE
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)

if 'eixo_mestre' not in st.session_state:
    st.session_state.eixo_mestre = get_alpha_eixo_final()

placeholder = st.empty()

while True:
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        ny_tz = pytz.timezone('America/New_York')
        now_br = datetime.now(br_tz)
        now_ny = datetime.now(ny_tz)
        
        # Reset Automático
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
            st.session_state.eixo_mestre = get_alpha_eixo_final()

        # Preço Real-Time
        ticker = yf.Ticker("BTC-USD")
        price = ticker.fast_info['last_price']
        
        eixo = st.session_state.eixo_mestre
        var = ((price / eixo) - 1) * 100
        cor_var = "#00FF00" if var >= 0 else "#FF0000"
        
        with placeholder.container():
            if now_br.hour == 18 and now_br.minute == 0:
                st.markdown('<div class="reset-alert">⚠️ SISTEMA RECALCULADO: NOVO EIXO MESTRE ATUALIZADO</div>', unsafe_allow_html=True)

            st.markdown(f"""
                <div class="header-container">
                    <div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div>
                    <div class="h-col">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                    <div class="h-col">DECISÃO</div><div class="h-col">RESPIRO</div>
                    <div class="h-col">DECISÃO F.</div><div class="h-col">EXAUSTÃO F.</div>
                </div>
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37;">BTC/USDT</div>
                    <div class="w-col">{price:,.3f}<br><span style="color:{cor_var}; font-size:16px;">{var:+.2f}%</span></div>
                    <div class="w-col" style="color:#FF4444;">{(eixo*1.0122):,.3f}</div>
