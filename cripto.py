import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - MODO COMPACTO TOTAL
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0.5rem 1rem !important; }
    .stApp { background-color: #000000; }
    
    .title-gold { color: #D4AF37; font-size: 26px; font-weight: 900; text-align: center; margin-bottom: 0; }
    .subtitle-white { color: #FFFFFF; font-size: 12px; text-align: center; letter-spacing: 4px; text-transform: lowercase; margin-bottom: 10px; }
    
    .main-table { width: 100%; border-collapse: collapse; color: white; font-family: 'monospace'; table-layout: fixed; }
    .header-style { background: #080808; border-bottom: 2px solid #D4AF37; font-size: 9px; height: 30px; text-align: center; font-weight: 800; }
    
    .price-row { height: 50px; text-align: center; font-size: 20px; font-weight: 800; border-top: 1px solid #111; }
    .vision-row { height: 40px; text-align: center; border-bottom: 1px solid #333; background: #050505; }
    
    .v-label { color: #777; font-size: 8px; text-transform: uppercase; }
    .v-value { color: #fff; font-size: 16px; font-weight: bold; }
    
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #666; text-align: center; padding: 5px; font-size: 10px; border-top: 1px solid #222; z-index: 9999; }
    .blink { animation: blinker 0.6s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

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
                return int((float(df_window['High'].max()) + float(df_window['Low'].min())) / 2)
        return fallback
    except: return fallback

COINS = {
    "BTC-USD": {"label": "BTC/USDT", "fb": 82632},
    "ETH-USD": {"label": "ETH/USDT", "fb": 2900}
}

if 'init' not in st.session_state:
    for t in COINS:
        val = get_midpoint_v13(t, COINS[t]['fb'])
        st.session_state[f'mp_{t}'] = val
        st.session_state[f'rv_{t}'] = val
    st.session_state['init'] = True

placeholder = st.empty()

while True:
    try:
        now_utc = datetime.now(pytz.utc)
        if now_utc.hour == 0 and now_utc.minute == 0 and now_utc.second < 2:
            for t in COINS:
                novo = get_midpoint_v13(t, COINS[t]['fb'])
                st.session_state[f'mp_{t}'] = novo
                st.session_state[f'rv_{t}'] = novo
            st.rerun()

        with placeholder.container():
            html = f'<div class="title-gold">ALPHA VISION</div><div class="subtitle-white">visão de tubarão</div>'
            html += '<table class="main-table">'
            html += '<tr class="header-style"><td>CÓDIGO</td><td>PREÇO</td><td style="color:#FF4444">EX. TOPO</td><td>PRÓX T.</td><td style="color:#FFFF00">DECISÃO</td><td>RESPIRO</td><td>PRÓX F.</td><td style="color:#00FF00">EX. FUNDO</td></tr>'
            
            for ticker, info in COINS.items():
                price = yf.Ticker(ticker).fast_info['last_price']
                mp, rv = st.session_state[f'mp_{ticker}'], st.session_state[f'rv_{ticker}']
                
                var = ((price / mp) - 1) * 100
                if var >= 1.35: st.session_state[f'mp_{ticker}'] = int(mp * 1.0122)
                elif var <= -1.35: st.session_state[f'mp_{ticker}'] = int(mp * 0.9878)
                
                var_reset = ((price / rv) - 1) * 100
                cor_v = "#00FF00" if var_reset >= 0 else "#FF4444"
                seta_v = "▲" if var_reset >= 0 else "▼"
                
                e_ext = "color:#FF4444;" + (" class='blink'" if var >= 1.20 else "")
                e_exf = "color:#00FF00;" + (" class='blink'" if var <= -1.20 else "")
                f_dec = "background:rgba(255,255,0,0.2);" if 0.59 <= abs(var) <= 0.65 else ""

                # Linha de Preços
                html += f'''
                <tr class="price-row">
                    <td style="color:#D4AF37">{info['label']}</td>
                    <td><div>{int(price):,}</div><div style="color:{cor_v};font-size:10px;">{seta_v} {var_reset:+.2f}%</div></td>
                    <td {e_ext}>{int(mp*1.0122):,}<br><span style="font-size:8px">+1.22%</span></td>
                    <td style="color:#FFA500">{int(mp*1.0083):,}</td>
                    <td style="{f_dec}">{int(mp*1.0061):,}</td>
                    <td style="color:#00CED1">{int(mp*1.0040):,}</td>
                    <td style="color:#FFA500">{int(mp*0.9939):,}</td>
                    <td {e_exf}>{int(mp*0.9878):,}<br><span style="font-size:8px">-1.22%</span></td>
                </tr>
                <tr class="vision-row">
                    <td colspan="4"><span class="v-label">ResetVision (24h):</span> <span class="v-value">{int(rv):,}</span></td>
                    <td colspan="4"><span class="v-label">ÂncoraVision (Móvel):</span> <span class="v-value" style="color:#00e6ff">{int(mp):,}</span></td>
                </tr>
                '''
            
            html += '</table>'
            st.markdown(html, unsafe_allow_html=True)
            st.markdown(f'<div class="footer">LIVE | UTC: {now_utc.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
            
        time.sleep(1)
    except: time.sleep(5)
