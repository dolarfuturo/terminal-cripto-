import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. ALPHA CORE SETUP
st.set_page_config(page_title="ALPHA TERMINAL", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 24px; font-weight: 900; text-align: center; padding: 15px; letter-spacing: 3px; }
    
    /* Grid Técnico com maior espaçamento (Gap) */
    .header-container { display: flex; width: 100%; padding: 15px 0; border-bottom: 2px solid #D4AF37; background: #050505; justify-content: space-between; gap: 10px; }
    .h-col { font-size: 10px; color: #666; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; letter-spacing: 1px; }
    
    /* Row ajustada: Fonte 18px para não embolar as 3 casas */
    .row-container { display: flex; width: 100%; align-items: center; padding: 30px 0; border-bottom: 1px solid #111; justify-content: space-between; gap: 10px; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 18px; font-weight: 800; color: #EEE; white-space: nowrap; }
    
    /* Footer Stream */
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 12px; border-top: 1px solid #222; display: flex; justify-content: center; align-items: center; gap: 40px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 10px; box-shadow: 0 0 15px #00FF00; animation: blink 1.5s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.1; } 100% { opacity: 1; } }
    
    .reset-alert { background-color: #D4AF37; color: #000; text-align: center; font-weight: 900; padding: 10px; font-size: 13px; position: fixed; top: 0; width: 100%; z-index: 2000; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CALIBRAGEM
def get_midpoint_institutional():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        if now_br.weekday() >= 5 or (now_br.weekday() == 0 and now_br.hour < 18):
            return 89792.500
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download("BTC-USD", start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_window = df.between_time('11:30', '18:00')
        if not df_window.empty:
            return round((float(df_window['High'].max()) + float(df_window['Low'].min())) / 2, 3)
        return 89792.500
    except:
        return 89792.500

# 3. INTERFACE
st.markdown('<div class="title-gold">ALPHA VISION • MIDPOINT TERMINAL</div>', unsafe_allow_html=True)

if 'midpoint' not in st.session_state:
    st.session_state.midpoint = get_midpoint_institutional()

placeholder = st.empty()

while True:
    try:
        br_tz, ny_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York')
        now_br, now_ny = datetime.now(br_tz), datetime.now(ny_tz)
        
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 3:
            st.session_state.midpoint = get_midpoint_institutional()

        ticker = yf.Ticker("BTC-USD")
        price = ticker.fast_info['last_price']
        mp = st.session_state.midpoint
        var = ((price / mp) - 1) * 100
        cor_var = "#00FF00" if var >= 0 else "#FF4444"
        
        with placeholder.container():
            if now_br.hour == 18 and now_br.minute == 0:
                st.markdown('<div class="reset-alert">⚠️ ALERTA: MIDPOINT RECALIBRADO (11:30-18:00)</div>', unsafe_allow_html=True)

            st.markdown(f"""
                <div class="header-container">
                    <div class="h-col">ASSET</div><div class="h-col">LAST PRICE</div>
                    <div class="h-col">EXHAUSTION UP</div><div class="h-col">TARGET TOP</div>
                    <div class="h-col">DECISION LEVEL</div><div class="h-col">BREATHER</div>
                    <div class="h-col">DECISION DOWN</div><div class="h-col">EXHAUSTION DOWN</div>
                </div>
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37;">BTC/USDT</div>
                    <div class="w-col">{price:,.3f}<br><span style="color:{cor_var}; font-size:14px;">{var:+.2f}%</span></div>
                    <div class="w-col" style="color:#FF4444;">{(mp*1.0122):,.3f}</div>
                    <div class="w-col" style="color:#FFA500;">{(mp*1.0083):,.3f}</div>
                    <div class="w-col" style="color:#FFFF00;">{(mp*1.0061):,.3f}</div>
                    <div class="w-col" style="color:#00CED1;">{(mp*1.0040):,.3f}</div>
                    <div class="w-col" style="color:#FFFF00;">{(mp*0.9939):,.3f}</div>
                    <div class="w-col" style="color:#00FF00;">{(mp*0.9878):,.3f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="footer">
                    <div><span class="dot"></span> LIVE DATASTREAM</div>
                    <div>MIDPOINT: <span style="color:#D4AF37; font-family:monospace;">{mp:,.3f}</span></div>
                    <div>BRASÍLIA: {now_br.strftime('%H:%M:%S')}</div>
                    <div>NEW YORK: {now_ny.strftime('%H:%M:%S')}</div>
                </div>
            """, unsafe_allow_html=True)
            
        time.sleep(1)
    except:
        time.sleep(5)
