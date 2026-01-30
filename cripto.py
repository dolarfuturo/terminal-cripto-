import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - VISUAL REFINADO
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-container { text-align: center; padding: 15px; }
    .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; }
    
    /* Ajuste Preciso do Subtítulo (H até Y) */
    .subtitle-white { 
        color: #FFFFFF; 
        font-size: 16px; 
        font-weight: 300; 
        letter-spacing: 5.5px; /* Calibrado para largura média H-Y */
        margin-top: 2px;
        text-transform: lowercase;
    }
    
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 25px 0; border-bottom: 1px solid #151515; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; white-space: nowrap; }
    
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 13px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 35px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO
def get_midpoint_v13():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        if now_br.weekday() >= 5 or (now_br.weekday() == 0 and now_br.hour < 18):
            return 89792
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download("BTC-USD", start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_window = df.between_time('11:30', '18:00')
        if not df_window.empty:
            return int((float(df_window['High'].max()) + float(df_window['Low'].min())) / 2)
        return 89792
    except:
        return 89792

# 3. INTERFACE REAL-TIME
st.markdown("""
    <div class="title-container">
        <div class="title-gold">ALPHA VISION CRYPTO</div>
        <div class="subtitle-white">visão de tubarão</div>
    </div>
    """, unsafe_allow_html=True)

if 'mp_current' not in st.session_state:
    st.session_state.mp_current = get_midpoint_v13()

placeholder = st.empty()

while True:
    try:
        br_tz, ny_tz, lon_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York'), pytz.timezone('Europe/London')
        now_br, now_ny, now_lon = datetime.now(br_tz), datetime.now(ny_tz), datetime.now(lon_tz)
        
        # Auto-Reset Binance (18:00 BR)
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
            st.session_state.mp_current = get_midpoint_v13()

        ticker = yf.Ticker("BTC-USD")
        price = ticker.fast_info['last_price']
        mp = st.session_state.mp_current
        var = ((price / mp) - 1) * 100
                    # --- LÓGICA DE ESCADA: GATILHO 1.35% | MOVIMENTO 1.22% ---
        if var >= 1.35:
            st.session_state.mp_current = int(mp * 1.0122)
            st.toast("⚡ ROMPIMENTO: NOVO EIXO (1.22%)", icon="📈")
            st.rerun() 
            
        elif var <= -1.35:
            st.session_state.mp_current = int(mp * 0.9878)
            st.toast("⚠️ QUEDA: EIXO RECALIBRADO (1.22%)", icon="📉")
            st.rerun()

        cor_var = "#00FF00" if var >= 0 else "#FF0000"
        seta = "▲" if var >= 0 else "▼"
        
        with placeholder.container():
            abs_var = abs(var)
            # Lógica dos Alarmes
            fundo_decisao = "background: rgba(255, 255, 0, 0.3);" if 0.59 <= abs_var <= 0.65 else ""
            estilo_ex_t = "color: #FF4444; animation: blink 0.4s infinite;" if (1.20 <= var < 1.35) else "color: #FF4444;"
            estilo_ex_f = "color: #00FF00; animation: blink 0.4s infinite;" if (-1.35 < var <= -1.20) else "color: #00FF00;"

                                    st.markdown(f"""
                <div class="header-container">
                    <div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div>
                    <div class="h-col" style="color:#FF4444; {estilo_ex_t}">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                    <div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div>
                    <div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00; {estilo_ex_f}">EXAUSTÃO F.</div>
                </div>
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37; font-weight:bold;">BTC/USDT</div>
                    <div class="w-col">
                        <span style="font-size:16px;">{int(price):,}</span><br>
                        <span style="color:{cor_var}; font-size:11px; font-weight:bold;">{seta} {var:+.2f}%</span>
                    </div>
                    <div class="w-col" style="color:#FF4444; {estilo_ex_t}">{int(mp*1.0122):,}</div>
                    <div class="w-col" style="color:#FFA500;">{int(mp*1.0083):,}</div>
                    <div class="w-col" style="color:#FFFF00; {fundo_decisao}">{int(mp*1.0061):,}</div>
                    <div class="w-col" style="color:#00CED1;">{int(mp*1.0040):,}</div>
                    <div class="w-col" style="color:#FFA500;">{int(mp*0.9939):,}</div>
                    <div class="w-col" style="color:#00FF00; {estilo_ex_f}">{int(mp*0.9878):,}</div>
                </div>
            """, unsafe_allow_html=True)

                                               
            st.markdown(f"""
                <div class="footer">
                    <div><span class="dot"></span> LIVESTREAM ATIVO</div>
                    <div>ancoravision: <span style="color:#FFA500; font-family:monospace;">{int(mp):,}</span></div>
                    <div>LONDRES: {now_lon.strftime('%H:%M:%S')}</div>
                    <div>BRASÍLIA: {now_br.strftime('%H:%M:%S')}</div>
                    <div>NEW YORK: {now_ny.strftime('%H:%M:%S')}</div>
                </div>
            """, unsafe_allow_html=True)
            
        time.sleep(1)
    except:
        time.sleep(5)
