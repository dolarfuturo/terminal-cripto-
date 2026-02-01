import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - VISUAL REFINADO
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

COINS_CONFIG = {
    "BTC-USD": {"label": "BTC/USDT", "fb": 82632, "dec": 0},
    "ETH-USD": {"label": "ETH/USDT", "fb": 2400, "dec": 0},
    "SOL-USD": {"label": "SOL/USDT", "fb": 160.00, "dec": 2},
    "BNB-USD": {"label": "BNB/USDT", "fb": 600.00, "dec": 2},
    "XRP-USD": {"label": "XRP/USDT", "fb": 2.5000, "dec": 4},
    "DOGE-USD": {"label": "DOGE/USDT", "fb": 0.3500, "dec": 4}
}

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-container { text-align: center; padding: 15px; }
    .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; }
    .subtitle-white { color: #FFFFFF; font-size: 16px; font-weight: 300; letter-spacing: 5.5px; margin-top: 2px; text-transform: lowercase; }
    
    .header-container { display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; }
    
    .row-container { display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; width: 100%; align-items: center; padding: 20px 0; border-bottom: 1px solid #151515; }
    .w-col { text-align: center; font-family: 'monospace'; font-size: 19px; font-weight: 800; color: #FFF; white-space: nowrap; }
    
    .vision-block { display: flex; justify-content: center; gap: 80px; margin-top: 10px; padding-bottom: 15px; border-bottom: 2px solid #111; }
    .v-item { text-align: center; }
    .v-label { color: #888; font-size: 9px; text-transform: uppercase; }
    .v-val { font-size: 18px; font-weight: bold; }

    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 13px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 35px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# Inicialização de Session State
for t, info in COINS_CONFIG.items():
    if f'mp_{t}' not in st.session_state:
        st.session_state[f'mp_{t}'] = info['fb']
        st.session_state[f'rv_{t}'] = info['fb']

placeholder = st.empty()

while True:
    try:
        br_tz, ny_tz, lon_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York'), pytz.timezone('Europe/London')
        now_br, now_ny, now_lon = datetime.now(br_tz), datetime.now(ny_tz), datetime.now(lon_tz)
        
        # Reset Automático (Binance 18:00 BR)
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
            for t in COINS_CONFIG:
                p_reset = yf.Ticker(t).fast_info['last_price']
                st.session_state[f'mp_{t}'] = p_reset
                st.session_state[f'rv_{t}'] = p_reset
            st.rerun()

        with placeholder.container():
            st.markdown('<div class="title-container"><div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div></div>', unsafe_allow_html=True)
            
            st.markdown("""
                <div class="header-container">
                    <div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div>
                    <div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                    <div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div>
                    <div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div>
                </div>
            """, unsafe_allow_html=True)

            for t, info in COINS_CONFIG.items():
                price = yf.Ticker(t).fast_info['last_price']
                mp = st.session_state[f'mp_{t}']
                rv = st.session_state[f'rv_{t}']
                
                # Lógica de Escada
                var_escada = ((price / mp) - 1) * 100
                if var_escada >= 1.35: st.session_state[f'mp_{t}'] = mp * 1.0122
                elif var_escada <= -1.35: st.session_state[f'mp_{t}'] = mp * 0.9878
                
                # Variação ResetVision
                var_reset = ((price / rv) - 1) * 100
                cor_v, seta_v = ("#00FF00", "▲") if var_reset >= 0 else ("#FF4444", "▼")
                
                # Estilos
                abs_v = abs(var_escada)
                fundo_d = "background: rgba(255, 255, 0, 0.25);" if 0.59 <= abs_v <= 0.65 else ""
                estilo_t = "color: #FF4444; animation: blink 0.4s infinite;" if (1.20 <= var_escada < 1.35) else "color: #FF4444;"
                estilo_f = "color: #00FF00; animation: blink 0.4s infinite;" if (-1.35 < var_escada <= -1.20) else "color: #00FF00;"

                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{info['label']}</div>
                        <div class="w-col">
                            <div style="font-weight: bold;">{f"{price:,.{info['dec']}f}"}</div>
                            <div style="color:{cor_v}; font-size:11px;">{seta_v} {var_reset:+.2f}%</div>
                        </div>
                        <div class="w-col" style="{estilo_t}">{f"{(mp * 1.0135):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#FFA500;">{f"{(mp * 1.0122):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="{fundo_d}">{f"{(mp * 1.0061):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#00CED1;">{f"{(mp * 0.9939):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#FFA500;">{f"{(mp * 0.9878):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="{estilo_f}">{f"{(mp * 0.9865):,.{info['dec']}f}"}</div>
                    </div>
                    <div class="vision-block">
                        <div class="v-item">
                            <div class="v-label">ResetVision (Fixo)</div>
                            <div class="v-val" style="color:#FFF;">{f"{rv:,.{info['dec']}f}"}</div>
                        </div>
                        <div class="v-item">
                            <div class="v-label">ÂncoraVision (Móvel)</div>
                            <div class="v-val" style="color:#00e6ff;">{f"{mp:,.{info['dec']}f}"}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="footer">
                    <div><span class="dot"></span> LIVESTREAM ATIVO</div>
                    <div>LONDRES: {now_lon.strftime('%H:%M:%S')}</div>
                    <div>BRASÍLIA: {now_br.strftime('%H:%M:%S')}</div>
                    <div>NEW YORK: {now_ny.strftime('%H:%M:%S')}</div>
                </div>
            """, unsafe_allow_html=True)
            
        time.sleep(1)
    except Exception as e:
        time.sleep(5)
