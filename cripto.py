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
    .subtitle-white { color: #FFFFFF; font-size: 16px; font-weight: 300; letter-spacing: 5.5px; margin-top: 2px; text-transform: lowercase; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 20px 0 5px 0; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; white-space: nowrap; }
    .vision-sub-row { display: flex; justify-content: center; gap: 80px; margin-top: 5px; padding-bottom: 20px; border-bottom: 1px solid #151515; }
    .v-item { text-align: center; }
    .v-lab { color: #888; font-size: 10px; text-transform: uppercase; }
    .v-val { color: #ffffff; font-size: 19px; font-weight: bold; font-family: 'monospace'; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 10px; font-size: 12px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 30px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO UNIFICADO
def get_midpoint_v13(symbol, fallback):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        if now_br.weekday() >= 5 or (now_br.weekday() == 0 and now_br.hour < 18):
            return fallback
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download(symbol, start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_window = df.between_time('11:30', '18:00')
        if not df_window.empty:
            return int((float(df_window['High'].max()) + float(df_window['Low'].min())) / 2)
        return fallback
    except: return fallback

# 3. CONFIGURAÇÃO DOS ATIVOS
COINS = {
    "BTC-USD": {"label": "BTC/USDT", "fb": 82632},
    "ETH-USD": {"label": "ETH/USDT", "fb": 2900}
}

st.markdown("""<div class="title-container"><div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div></div>""", unsafe_allow_html=True)

for ticker in COINS:
    if f'mp_{ticker}' not in st.session_state:
        val = get_midpoint_v13(ticker, COINS[ticker]['fb'])
        st.session_state[f'mp_{ticker}'] = val
        st.session_state[f'rv_{ticker}'] = val

placeholder = st.empty()

while True:
    try:
        br_tz, lon_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('Europe/London')
        now_br, now_lon = datetime.now(br_tz), datetime.now(lon_tz)
        
        # Auto-Reset Binance (18:00 BR)
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
            for ticker in COINS:
                novo = get_midpoint_v13(ticker, COINS[ticker]['fb'])
                st.session_state[f'mp_{ticker}'] = novo
                st.session_state[f'rv_{ticker}'] = novo
            st.rerun()

        with placeholder.container():
            st.markdown("""<div class="header-container"><div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div><div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div><div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div><div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div></div>""", unsafe_allow_html=True)
            
            for ticker, info in COINS.items():
                price = yf.Ticker(ticker).fast_info['last_price']
                mp = st.session_state[f'mp_{ticker}']
                rv = st.session_state[f'rv_{ticker}']
                
                var = ((price / mp) - 1) * 100
                if var >= 1.35: st.session_state[f'mp_{ticker}'] = int(mp * 1.0122)
                elif var <= -1.35: st.session_state[f'mp_{ticker}'] = int(mp * 0.9878)
                
                var_reset = ((price / rv) - 1) * 100
                cor_v, seta_v = ("#00FF00", "▲") if var_reset >= 0 else ("#FF4444", "▼")
                
                abs_var = abs(var)
                f_dec = "background: rgba(255, 255, 0, 0.3);" if 0.59 <= abs_var <= 0.65 else ""
                e_ext = "color: #FF4444; animation: blink 0.4s infinite;" if (1.20 <= var < 1.35) else "color: #FF4444;"
                e_exf = "color: #00FF00; animation: blink 0.4s infinite;" if (-1.35 < var <= -1.20) else "color: #00FF00;"

                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{info['label']}</div>
                        <div class="w-col"><div>{int(price):,}</div><div style="color:{cor_v}; font-size:11px;">{seta_v} {var_reset:+.2f}%</div></div>
                        <div class="w-col" style="{e_ext}">{int(mp*1.0122):,}</div>
                        <div class="w-col" style="color:#FFA500;">{int(mp*1.0083):,}</div>
                        <div class="w-col" style="{f_dec}">{int(mp*1.0061):,}</div>
                        <div class="w-col" style="color:#00CED1;">{int(mp*1.0040):,}</div>
                        <div class="w-col" style="color:#FFA500;">{int(mp*0.9939):,}</div>
                        <div class="w-col" style="{e_exf}">{int(mp*0.9878):,}</div>
                    </div>
                    <div class="vision-sub-row">
                        <div class="v-item"><div class="v-lab">ResetVision (24h)</div><div class="v-val">{int(rv):,}</div></div>
                        <div class="v-item"><div class="v-lab">ÂncoraVision (Móvel)</div><div class="v-val" style="color: #00e6ff;">{int(mp):,}</div></div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""<div class="footer"><div><span class="dot"></span> LIVESTREAM ATIVO</div><div>LONDRES: {now_lon.strftime('%H:%M:%S')}</div><div>BRASÍLIA: {now_br.strftime('%H:%M:%S')}</div></div>""", unsafe_allow_html=True)
            
        time.sleep(1)
    except: time.sleep(5)
