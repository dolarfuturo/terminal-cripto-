import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - VISUAL REFINADO (ORIGINAL PRESERVADO)
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-container { text-align: center; padding: 10px; }
    .title-gold { color: #D4AF37; font-size: 30px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; }
    .subtitle-white { 
        color: #FFFFFF; 
        font-size: 14px; 
        font-weight: 300; 
        letter-spacing: 5.5px;
        margin-top: 2px;
        text-transform: lowercase;
    }
    .header-container { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; }
    .h-col { font-size: 9px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 12px 0; border-bottom: 1px solid #151515; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 18px; font-weight: 800; color: #FFF; white-space: nowrap; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 10px; font-size: 12px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 30px; z-index: 1000; }
    .dot { height: 8px; width: 8px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO MULTI-ATIVO
def get_midpoint_v13(symbol, fallback):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download(symbol, start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not df.empty:
            df.index = df.index.tz_convert(br_tz)
            df_window = df.between_time('11:30', '18:00')
            if not df_window.empty:
                return (float(df_window['High'].max()) + float(df_window['Low'].min())) / 2
        return fallback
    except:
        return fallback

# 3. DICIONÁRIO DE CONFIGURAÇÃO
assets = {
    "BTC/USDT": {"sym": "BTC-USD", "fb": 82632},
    "ETH/USDT": {"sym": "ETH-USD", "fb": 2500},
    "BNB/USDT": {"sym": "BNB-USD", "fb": 600},
    "SOL/USDT": {"sym": "SOL-USD", "fb": 150},
    "XRP/USDT": {"sym": "XRP-USD", "fb": 0.60},
    "DOGE/USDT": {"sym": "DOGE-USD", "fb": 0.15}
}

if 'states' not in st.session_state:
    st.session_state.states = {}
    for label, cfg in assets.items():
        val = get_midpoint_v13(cfg["sym"], cfg["fb"])
        st.session_state.states[label] = {"mp": val, "rv": val}

# 4. INTERFACE
st.markdown("""<div class="title-container"><div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div></div>""", unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        br_tz, ny_tz, lon_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York'), pytz.timezone('Europe/London')
        now_br, now_ny, now_lon = datetime.now(br_tz), datetime.now(ny_tz), datetime.now(lon_tz)
        
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
            for label, cfg in assets.items():
                val = get_midpoint_v13(cfg["sym"], cfg["fb"])
                st.session_state.states[label] = {"mp": val, "rv": val}
            st.rerun()

        with placeholder.container():
            st.markdown("""<div class="header-container"><div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div><div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div><div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div><div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div></div>""", unsafe_allow_html=True)

            for label, state in st.session_state.states.items():
                price = yf.Ticker(assets[label]["sym"]).fast_info['last_price']
                mp, rv = state["mp"], state["rv"]
                
                # Lógica Escada
                var = ((price / mp) - 1) * 100
                if var >= 1.35: st.session_state.states[label]["mp"] *= 1.0122
                elif var <= -1.35: st.session_state.states[label]["mp"] *= 0.9878

                var_reset = ((price / rv) - 1) * 100
                cor_v = "#00FF00" if var_reset >= 0 else "#FF4444"
                seta_v = "▲" if var_reset >= 0 else "▼"
                abs_var = abs(var)
                
                fundo_decisao = "background: rgba(255, 255, 0, 0.3);" if 0.59 <= abs_var <= 0.65 else ""
                estilo_ex_t = "color: #FF4444; animation: blink 0.4s infinite;" if (1.20 <= var < 1.35) else "color: #FF4444;"
                estilo_ex_f = "color: #00FF00; animation: blink 0.4s infinite;" if (-1.35 < var <= -1.20) else "color: #00FF00;"

                fmt = lambda x: f"{x:,.0f}" if x > 1 else f"{x:,.4f}"

                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{label}</div>
                        <div class="w-col"><div>{fmt(price)}</div><div style="color:{cor_v}; font-size:10px;">{seta_v} {var_reset:+.2f}%</div></div>
                        <div class="w-col" style="{estilo_ex_t}">{fmt(mp*1.0122)}</div>
                        <div class="w-col" style="color:#FFA500;">{fmt(mp*1.0083)}</div>
                        <div class="w-col" style="{fundo_decisao}">{fmt(mp*1.0061)}</div>
                        <div class="w-col" style="color:#00CED1;">{fmt(mp*1.0040)}</div>
                        <div class="w-col" style="color:#FFA500;">{fmt(mp*0.9939)}</div>
                        <div class="w-col" style="{estilo_ex_f}">{fmt(mp*0.9878)}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown(f"""
                <div class="footer">
                    <div><span class="dot"></span> LIVE</div>
                    <div>BRASÍLIA: {now_br.strftime('%H:%M:%S')}</div>
                    <div>LONDRES: {now_lon.strftime('%H:%M:%S')}</div>
                    <div>NY: {now_ny.strftime('%H:%M:%S')}</div>
                </div>""", unsafe_allow_html=True)
            
        time.sleep(1)
    except:
        time.sleep(5)
