import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - TOP 20 ATIVOS
st.set_page_config(page_title="ALPHA VISION PRO", layout="wide", initial_sidebar_state="collapsed")

COINS_CONFIG = {
    "BTC-USD": {"label": "BTC/USDT", "dec": 0},
    "ETH-USD": {"label": "ETH/USDT", "dec": 0},
    "SOL-USD": {"label": "SOL/USDT", "dec": 2},
    "BNB-USD": {"label": "BNB/USDT", "dec": 2},
    "XRP-USD": {"label": "XRP/USDT", "dec": 4},
    "DOGE-USD": {"label": "DOGE/USDT", "dec": 4},
    "ADA-USD": {"label": "ADA/USDT", "dec": 4},
    "AVAX-USD": {"label": "AVAX/USDT", "dec": 2},
    "DOT-USD": {"label": "DOT/USDT", "dec": 2},
    "LINK-USD": {"label": "LINK/USDT", "dec": 2},
    "MATIC-USD": {"label": "POL/USDT", "dec": 4},
    "TRX-USD": {"label": "TRX/USDT", "dec": 4},
    "LTC-USD": {"label": "LTC/USDT", "dec": 2},
    "BCH-USD": {"label": "BCH/USDT", "dec": 2},
    "SHIB-USD": {"label": "SHIB/USDT", "dec": 6},
    "NEAR-USD": {"label": "NEAR/USDT", "dec": 3},
    "APT-USD": {"label": "APT/USDT", "dec": 2},
    "UNI-USD": {"label": "UNI/USDT", "dec": 2},
    "STX-USD": {"label": "STX/USDT", "dec": 3},
    "ARB-USD": {"label": "ARB/USDT", "dec": 4}
}

# FUNÇÃO DE CÁLCULO RESET (MÁX + MÍN / 2) - 11:30 às 18:00 BR
def get_alpha_midpoint(ticker):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(br_tz)
        
        # Determina o dia de referência para o Reset
        if now.weekday() >= 5: # Fim de semana -> Pega Sexta
            target_date = now - timedelta(days=(now.weekday() - 4))
        elif now.weekday() == 0 and now.hour < 18: # Segunda antes das 18h -> Pega Sexta
            target_date = now - timedelta(days=3)
        else: # Terça a Sexta -> Pega dia anterior ou hoje (se pós 18h)
            target_date = now if now.hour >= 18 else now - timedelta(days=1)
            
        start_s = target_date.strftime('%Y-%m-%d')
        end_s = (target_date + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Download 1m para precisão máxima
        df = yf.download(ticker, start=start_s, end=end_s, interval="1m", progress=False)
        if df.empty: return yf.Ticker(ticker).fast_info['last_price']
        
        df.index = df.index.tz_convert(br_tz)
        # Filtro rígido do horário de Brasília
        df_window = df.between_time('11:30', '18:00')
        
        if not df_window.empty:
            high = float(df_window['High'].max())
            low = float(df_window['Low'].min())
            return (high + low) / 2
        return yf.Ticker(ticker).fast_info['last_price']
    except: return 0

# CSS VISUAL ORIGINAL
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; text-align: center; letter-spacing: 2px; }
    .subtitle-white { color: #FFFFFF; font-size: 16px; text-align: center; letter-spacing: 5.5px; text-transform: lowercase; margin-bottom: 20px; }
    .header-container { display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 10px; color: #FFF; text-align: center; font-weight: 800; }
    .row-container { display: grid; grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr; width: 100%; align-items: center; padding: 15px 0; border-bottom: 1px solid #151515; }
    .w-col { text-align: center; font-family: 'monospace'; font-size: 18px; font-weight: 800; color: #FFF; }
    .vision-block { display: flex; justify-content: center; gap: 80px; padding: 10px 0 20px 0; border-bottom: 2px solid #111; }
    .v-item { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO
for t in COINS_CONFIG:
    if f'rv_{t}' not in st.session_state:
        val = get_alpha_midpoint(t)
        st.session_state[f'rv_{t}'] = val
        st.session_state[f'mp_{t}'] = val

placeholder = st.empty()

# 3. MOTOR REAL-TIME
while True:
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        
        # Reset Oficial 18:00 BR
        if now_br.weekday() < 5 and now_br.hour == 18 and now_br.minute == 0 and now_br.second < 5:
            for t in COINS_CONFIG:
                val = get_alpha_midpoint(t)
                st.session_state[f'rv_{t}'] = val
                st.session_state[f'mp_{t}'] = val
            st.rerun()

        with placeholder.container():
            st.markdown('<div class="title-gold">ALPHA VISION PRO</div><div class="subtitle-white">visão de tubarão</div>', unsafe_allow_html=True)
            st.markdown('<div class="header-container"><div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div><div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div><div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div><div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div></div>', unsafe_allow_html=True)

            for t, info in COINS_CONFIG.items():
                price = yf.Ticker(t).fast_info['last_price']
                mp = st.session_state[f'mp_{t}']
                rv = st.session_state[f'rv_{t}']
                
                # RÉGUA BTC/ETH 1.22% | ALTS 12.2%
                if t in ["BTC-USD", "ETH-USD"]:
                    g_ex, g_mov, g_dec, g_res = 1.35, 1.0122, 1.0061, 1.0040
                else:
                    g_ex, g_mov, g_dec, g_res = 13.5, 1.122, 1.061, 1.040
                
                var_escada = ((price / mp) - 1) * 100
                if var_escada >= g_ex: st.session_state[f'mp_{t}'] = mp * g_mov
                elif var_escada <= -g_ex: st.session_state[f'mp_{t}'] = mp * (2 - g_mov)
                
                var_reset = ((price / rv) - 1) * 100
                cor_v = "#00FF00" if var_reset >= 0 else "#FF4444"

                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{info['label']}</div>
                        <div class="w-col">
                            <div>{f"{price
