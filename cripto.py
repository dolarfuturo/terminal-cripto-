import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - RESTAURAÇÃO TOTAL ORIGINAL
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 32px; font-weight: 900; text-align: center; padding: 10px; }
    
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; gap: 5px; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    
    /* Row com fonte 18px e espaçamento para as 3 casas decimais */
    .row-container { display: flex; width: 100%; align-items: center; padding: 25px 0; border-bottom: 1px solid #151515; justify-content: space-between; gap: 5px; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 18px; font-weight: 800; color: #FFF; white-space: nowrap; }
    
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 12px; font-size: 13px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 30px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    
    .reset-alert { background-color: #D4AF37; color: #000; text-align: center; font-weight: 900; padding: 8px; font-size: 14px; position: fixed; top: 0; width: 100%; z-index: 2000; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO (HLC MIDPOINT)
def get_alpha_eixo_v10():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        if now_br.weekday() >= 5 or (now_br.weekday() == 0 and now_br.hour < 18):
            return 89792.500
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download("BTC-USD", start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_janela = df.between_time('11:30', '18:00')
        if not df_janela.empty:
            # Cálculo do ponto médio arredondado para 3 casas
            return round((float(df_janela['High'].max()) + float(df_janela['Low'].min())) / 2, 3)
        return 89792.500
    except:
        return 89792.500

# 3. INTERFACE REAL-TIME
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)

if 'eixo_final' not in st.session_state:
    st.session_state.eixo_final = get_alpha_eixo_v10()

placeholder = st.empty()

while True:
    try:
        br_tz, ny_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York')
        now_br, now_ny = datetime.now(br_tz), datetime.now(ny_tz)
        
        # Reset Automático na virada do Candle
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
            st.session_state.eixo_final = get_alpha_eixo_v10()

        ticker = yf.Ticker("BTC-USD")
        price = ticker.fast_info['last_price']
        eixo = st.session_state.eixo_final
        var = ((price / eixo) - 1) * 100
        cor_var = "#00FF00" if var >= 0 else "#FF0000"
        
        with placeholder.container():
            if now_br.hour == 18 and now_br.minute == 0:
