import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - VISUAL REFINADO
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")
COINS_CONFIG = {
    "BTC-USD":  {"label": "BTC/USDT",  "fb": 82000, "dec": 0},
    "ETH-USD":  {"label": "ETH/USDT",  "fb": 2400,  "dec": 0},
    "SOL-USD":  {"label": "SOL/USDT",  "fb": 160,   "dec": 2},
    "BNB-USD":  {"label": "BNB/USDT",  "fb": 600,   "dec": 2},
    "XRP-USD":  {"label": "XRP/USDT",  "fb": 2.50,  "dec": 4},
    "DOGE-USD": {"label": "DOGE/USDT", "fb": 0.35,  "dec": 4}
}
# --- COPIE DAQUI ---
def get_midpoint_v13(ticker, fallback):
    try:
        import yfinance as yf
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        if not data.empty:
            return float(data['Close'].iloc[0])
        return float(fallback)
    except:
        return float(fallback)

for ticker in COINS_CONFIG:
    if f'mp_{ticker}' not in st.session_state:
        val = get_midpoint_v13(ticker, COINS_CONFIG[ticker]['fb'])
        st.session_state[f'mp_{ticker}'] = val
        st.session_state[f'rv_{ticker}'] = val
# --- ATÉ AQUI ---

 

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
            /* Configuração das Colunas Principais */
        .header-container, .row-container {
            display: grid;
            grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr;
            width: 100%;
            padding: 10px 0;
            border-bottom: 1px solid #222;
            align-items: center;
            text-align: center;
        }
        .h-col { font-size: 10px; color: #888; font-weight: bold; text-transform: uppercase; }
        .w-col { font-size: 18px; font-weight: bold; color: #FFF; }

        /* ESTE BLOCO CENTRALIZA O RESET E ÂNCORA */
                .vision-block {
            display: flex;
            justify-content: center; /* Centraliza no meio da tela */
            gap: 100px;              /* Aumenta o espaço entre Reset e Âncora */
            width: 100%;
            padding: 10px 0 25px 0;
            margin-top: -15px;
            border-bottom: 1px solid #222;
        }
        .v-item { 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
        }
        .v-label { font-size: 11px; color: #666; font-weight: bold; }
        .v-val { font-size: 18px; font-weight: 900; } /* Aumentei o tamanho do número */
       }
        .v-item { 
            display: flex; 
            flex-direction: column; 
            align-items: center;     /* Centraliza o texto interno */
        }
        .v-label { font-size: 9px; color: #666; font-weight: bold; margin-bottom: 2px; }
        .v-val { font-size: 14px; font-weight: 900; }

                        padding: 5px 0 15px 0;
            margin-top: -10px;
            border-bottom: 2px solid #111;
        }
        .v-item { display: flex; flex-direction: column; align-items: center; }
        .v-label { font-size: 9px; color: #555; font-weight: bold; }
        .v-val { font-size: 13px; font-weight: bold; }

    
    .row-container { display: flex; width: 100%; align-items: center; padding: 25px 0; border-bottom: 1px solid #151515; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; white-space: nowrap; }
    
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 13px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 35px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO E RESET (BINANCE 00:00 UTC)
placeholder = st.empty()

while True:
    # Reset Automático às 00:00 UTC
    agora_utc = datetime.now(pytz.utc)
    if agora_utc.hour == 0 and agora_utc.minute == 0 and agora_utc.second < 5:
        for t in COINS_CONFIG:
            st.session_state[f'mp_{t}'] = yf.Ticker(t).fast_info['last_price']
            st.session_state[f'rv_{t}'] = st.session_state[f'mp_{t}']
        st.rerun()

    placeholder.empty()
    with placeholder.container():
        st.markdown("""
            <div class="header-container">
                <div class="h-col">CÓDIGO</div>
                <div class="h-col">PREÇO ATUAL</div>
                <div class="h-col" style="color: #FF4444;">EXAUSTÃO T.</div>
                <div class="h-col">PRÓX. TOPO</div>
                <div class="h-col" style="color: #FFFF00;">DECISÃO</div>
                <div class="h-col">RESPIRO</div>
                <div class="h-col">PRÓX. AO F.</div>
                <div class="h-col" style="color: #00FF00;">EXAUSTÃO F.</div>
            </div>
        """, unsafe_allow_html=True)

        for ticker, info in COINS_CONFIG.items():
            price = yf.Ticker(ticker).fast_info['last_price']
            mp = st.session_state[f'mp_{ticker}']
            rv = st.session_state[f'rv_{ticker}']
            var_reset = ((price / rv) - 1) * 100
            cor_v, seta_v = ("#00FF00", "▲") if var_reset >= 0 else ("#FF4444", "▼")

            st.markdown(f"""
                <div class="row-container">
                    <div class="w-col" style="font-size: 20px;">{info['label']}</div>
                    <div class="w-col">
                        <div style="font-size: 22px; font-weight: bold;">{f"{price:,.{info['dec']}f}"}</div>
                        <div style="font-size: 13px; color: {cor_v};">{seta_v} {var_reset:.2f}%</div>
                    </div>
                    <div class="w-col" style="color: #FF4444;">{f"{(mp * 1.0135):,.{info['dec']}f}"}</div>
                    <div class="w-col">{f"{(mp * 1.0122):,.{info['dec']}f}"}</div>
                    <div class="w-col" style="color: #FFFF00;">{f"{(mp * 1.0062):,.{info['dec']}f}"}</div>
                    <div class="w-col">{f"{(mp * 0.9938):,.{info['dec']}f}"}</div>
                    <div class="w-col">{f"{(mp * 0.9878):,.{info['dec']}f}"}</div>
                    <div class="w-col" style="color: #00FF00;">{f"{(mp * 0.9865):,.{info['dec']}f}"}</div>
                </div>
                <div style="display: flex; justify-content: center; gap: 100px; padding: 10px 0 25px 0; border-bottom: 2px solid #111; width: 100%;">
                    <div style="text-align: center;">
                        <div style="font-size: 10px; color: #666;">RESETVISION</div>
                        <div style="font-size: 16px; font-weight: bold; color: #FFF;">{f"{rv:,.{info['dec']}f}"}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 10px; color: #666;">ÂNCORAVISION</div>
                        <div style="font-size: 16px; font-weight: bold; color: #00FFFF;">{f"{mp:,.{info['dec']}f}"}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    time.sleep(1)
