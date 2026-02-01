import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

COINS_CONFIG = {
    "BTC-USD": {"label": "BTC/USDT", "dec": 0},
    "ETH-USD": {"label": "ETH/USDT", "dec": 0},
    "SOL-USD": {"label": "SOL/USDT", "dec": 2},
    "BNB-USD": {"label": "BNB/USDT", "dec": 2},
    "XRP-USD": {"label": "XRP/USDT", "dec": 4},
    "DOGE-USD": {"label": "DOGE/USDT", "dec": 4}
}

# FUNÇÃO MESTRE: Cálculo (Máx + Mín) / 2 entre 11:30 e 18:00 BR
def get_alpha_midpoint(ticker):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        # Se for fim de semana ou antes das 18h de segunda, busca o último dia útil
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        
        df = yf.download(ticker, start=(target_date - timedelta(days=2)).strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        
        # Filtra entre 11:30 e 18:00
        df_window = df.between_time('11:30', '18:00')
        
        if not df_window.empty:
            midpoint = (float(df_window['High'].max()) + float(df_window['Low'].min())) / 2
            return midpoint
        return yf.Ticker(ticker).fast_info['last_price']
    except:
        return yf.Ticker(ticker).fast_info['last_price']

# CSS VISUAL
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; text-align: center; letter-spacing: 2px; }
    .subtitle-white { color: #FFFFFF; font-size: 16px; text-align: center; letter-spacing: 5.5px; text-transform: lowercase; margin-bottom: 20px; }
    .header-container { display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; }
    .h-col { font-size: 10px; color: #FFF; text-align: center; font-weight: 800; }
    .row-container { display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; width: 100%; align-items: center; padding: 15px 0; border-bottom: 1px solid #151515; }
    .w-col { text-align: center; font-family: 'monospace'; font-size: 19px; font-weight: 800; color: #FFF; }
    .vision-block { display: flex; justify-content: center; gap: 80px; padding: 10px 0 20px 0; border-bottom: 2px solid #111; }
    .v-item { text-align: center; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# Inicialização de Memória com o Cálculo (Máx + Mín / 2)
for t in COINS_CONFIG:
    if f'mp_{t}' not in st.session_state:
        val = get_alpha_midpoint(t)
        st.session_state[f'mp_{t}'] = val
        st.session_state[f'rv_{t}'] = val

placeholder = st.empty()

while True:
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        
        # RESET 18:00 BR (Segunda a Sexta) - Novo Cálculo Máx+Mín/2
        if now_br.weekday() < 5 and now_br.hour == 18 and now_br.minute == 0 and now_br.second < 5:
            for t in COINS_CONFIG:
                val = get_alpha_midpoint(t)
                st.session_state[f'mp_{t}'] = val
                st.session_state[f'rv_{t}'] = val
            st.rerun()

        with placeholder.container():
            st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div>', unsafe_allow_html=True)
            st.markdown('<div class="header-container"><div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div><div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div><div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div><div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div></div>', unsafe_allow_html=True)

            for t, info in COINS_CONFIG.items():
                price = yf.Ticker(t).fast_info['last_price']
                mp = st.session_state[f'mp_{t}']
                rv = st.session_state[f'rv_{t}']
                
                # Lógica Escada 1.35% / 1.22%
                var_escada = ((price / mp) - 1) * 100
                if var_escada >= 1.35: st.session_state[f'mp_{t}'] = mp * 1.0122
                elif var_escada <= -1.35: st.session_state[f'mp_{t}'] = mp * 0.9878
                
                var_reset = ((price / rv) - 1) * 100
                cor_v, seta_v = ("#00FF00", "▲") if var_reset >= 0 else ("#FF4444", "▼")
                abs_v = abs(var_escada)
                
                fundo_d = "background: rgba(255, 255, 0, 0.2);" if 0.59 <= abs_v <= 0.65 else ""
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
                        <div class="v-item"><div style="color:#888; font-size:9px;">RESETVISION (MÁX+MÍN/2)</div><div style="color:#FFF; font-size:16px; font-weight:bold;">{f"{rv:,.{info['dec']}f}"}</div></div>
                        <div class="v-item"><div style="color:#888; font-size:9px;">ÂNCORAVISION (ESCADA)</div><div style="color:#00e6ff; font-size:16px; font-weight:bold;">{f"{mp:,.{info['dec']}f}"}</div></div>
                    </div>
                """, unsafe_allow_html=True)
        time.sleep(1)
    except:
        time.sleep(5)
