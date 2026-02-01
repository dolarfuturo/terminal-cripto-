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

def get_calculation_date():
    br_tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(br_tz)
    # Se for Sábado(5) ou Domingo(6), ou Segunda(0) antes das 18h, a base é a Sexta anterior
    if now.weekday() == 5: return now - timedelta(days=1)
    if now.weekday() == 6: return now - timedelta(days=2)
    if now.weekday() == 0 and now.hour < 18: return now - timedelta(days=3)
    # Se for dia de semana antes das 18h, usa o dia anterior
    if now.hour < 18: return now - timedelta(days=1)
    return now

def get_alpha_midpoint(ticker):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        target_date = get_calculation_date()
        
        # Baixa dados do dia alvo
        start_fetch = target_date.strftime('%Y-%m-%d')
        end_fetch = (target_date + timedelta(days=1)).strftime('%Y-%m-%d')
        
        df = yf.download(ticker, start=start_fetch, end=end_fetch, interval="1m", progress=False)
        if df.empty: return yf.Ticker(ticker).fast_info['last_price']
        
        df.index = df.index.tz_convert(br_tz)
        df_window = df.between_time('11:30', '18:00')
        
        if not df_window.empty:
            return (float(df_window['High'].max()) + float(df_window['Low'].min())) / 2
        return yf.Ticker(ticker).fast_info['last_price']
    except:
        return 0

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

# Inicialização de Memória
for t in COINS_CONFIG:
    if f'rv_{t}' not in st.session_state:
        val = get_alpha_midpoint(t)
        st.session_state[f'rv_{t}'] = val
        st.session_state[f'mp_{t}'] = val

placeholder = st.empty()

while True:
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        
        # RESET 18:00 BR (Segunda a Sexta)
        if now_br.weekday() < 5 and now_br.hour == 18 and now_br.minute == 0 and now_br.second < 5:
            for t in COINS_CONFIG:
                val = get_alpha_midpoint(t)
                st.session_state[f'rv_{t}'] = val
                st.session_state[f'mp_{t}'] = val
            st.rerun()

        with placeholder.container():
            st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div>', unsafe_allow_html=True)
            st.markdown('<div class="header-container"><div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div><div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div><div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div><div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div></div>', unsafe_allow_html=True)

            for t, info in COINS_CONFIG.items():
                price = yf.Ticker(t).fast_info['last_price']
                mp = st.session_state[f'mp_{t}']
                rv = st.session_state[f'rv_{t}']
                
                # --- CONFIGURAÇÃO DE ESCALA (BTC/ETH nos 1,22% | OUTRAS 12,2%) ---
                if t in ["BTC-USD", "ETH-USD"]:
                    g_ex, g_mov, g_dec, g_res = 1.35, 1.0122, 1.0061, 1.0040
                    label_regua = "1.22%"
                else:
                    g_ex, g_mov, g_dec, g_res = 13.5, 1.122, 1.061, 1.040
                    label_regua = "12.2%"
                
                var_escada = ((price / mp) - 1) * 100
                
                if var_escada >= g_ex: 
                    st.session_state[f'mp_{t}'] = mp * g_mov
                elif var_escada <= -g_ex: 
                    st.session_state[f'mp_{t}'] = mp * (2 - g_mov)
                
                var_reset = ((price / rv) - 1) * 100
                cor_v, seta_v = ("#00FF00", "▲") if var_reset >= 0 else ("#FF4444", "▼")
                
                abs_v = abs(var_escada)
                fundo_d = "background: rgba(255, 255, 0, 0.2);" if (g_ex*0.44 <= abs_v <= g_ex*0.48) else ""
                blink_t = "animation: blink 0.4s infinite;" if (g_ex*0.88 <= var_escada < g_ex) else ""
                blink_f = "animation: blink 0.4s infinite;" if (-g_ex < var_escada <= -g_ex*0.88) else ""

                st.markdown(f"""
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{info['label']}</div>
                        <div class="w-col">
                            <div style="font-weight: bold;">{f"{price:,.{info['dec']}f}"}</div>
                            <div style="color:{cor_v}; font-size:11px;">{seta_v} {var_reset:+.2f}%</div>
                        </div>
                        <div class="w-col" style="color:#FF4444; {blink_t}">{f"{(mp * (1 + (g_ex/100))):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#FFA500;">{f"{(mp * g_mov):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="{fundo_d} color:#FFFF00;">{f"{(mp * g_dec):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#00CED1;">{f"{(mp * g_res):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#FFA500;">{f"{(mp * (2 - g_mov)):,.{info['dec']}f}"}</div>
                        <div class="w-col" style="color:#00FF00; {blink_f}">{f"{(mp * (1 - (g_ex/100))):,.{info['dec']}f}"}</div>
                    </div>
                    <div class="vision-block">
                        <div class="v-item"><div style="color:#888; font-size:9px;">RESETVISION</div><div style="color:#FFF; font-size:16px; font-weight:bold;">{f"{rv:,.{info['dec']}f}"}</div></div>
                        <div class="v-item"><div style="color:#888; font-size:9px;">ÂNCORAVISION ({label_regua})</div><div style="color:#00e6ff; font-size:16px; font-weight:bold;">{f"{mp:,.{info['dec']}f}"}</div></div>
                    </div>
                """, unsafe_allow_html=True)
        time.sleep(1)
    except:
        time.sleep(5)
