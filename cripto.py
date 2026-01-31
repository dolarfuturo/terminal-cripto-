import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - VISUAL REFINADO
st.set_page_config(page_title="ALPHA VISION MULTI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-container { text-align: center; padding: 15px; }
    .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; }
    .subtitle-white { color: #FFFFFF; font-size: 16px; font-weight: 300; letter-spacing: 5.5px; margin-top: 2px; text-transform: lowercase; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 25px 0; border-bottom: 1px solid #151515; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; white-space: nowrap; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 10px; font-size: 12px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 20px; z-index: 1000; }
    .dot { height: 8px; width: 8px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; box-shadow: 0 0 10px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO ATUALIZADO
def get_midpoint_multi(symbol):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download(symbol, start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not df.empty:
            return (float(df['High'].max()) + float(df['Low'].min())) / 2
        return 0
    except:
        return 0

# Configuração de ativos e seus alvos (Multiplicadores)
ativos_config = {
    "BTC-USD": {"tipo": "heavy", "escada": 1.0122, "gatilho": 1.35, "alvos": [1.0122, 1.0083, 1.0061, 1.0040, 0.9939, 0.9878]},
    "ETH-USD": {"tipo": "heavy", "escada": 1.0122, "gatilho": 1.35, "alvos": [1.0122, 1.0083, 1.0061, 1.0040, 0.9939, 0.9878]},
    "BNB-USD": {"tipo": "alt", "escada": 1.12, "gatilho": 13.0, "alvos": [1.12, 1.08, 1.06, 1.04, 0.94, 0.88]},
    "SOL-USD": {"tipo": "alt", "escada": 1.12, "gatilho": 13.0, "alvos": [1.12, 1.08, 1.06, 1.04, 0.94, 0.88]},
    "XRP-USD": {"tipo": "alt", "escada": 1.12, "gatilho": 13.0, "alvos": [1.12, 1.08, 1.06, 1.04, 0.94, 0.88]},
    "DOGE-USD": {"tipo": "alt", "escada": 1.12, "gatilho": 13.0, "alvos": [1.12, 1.08, 1.06, 1.04, 0.94, 0.88]}
}

# Inicialização do Estado
if 'data' not in st.session_state:
    st.session_state.data = {}
    for symbol in ativos_config:
        val = get_midpoint_multi(symbol)
        st.session_state.data[symbol] = {'mp': val, 'rv': val}

# INTERFACE
st.markdown('<div class="title-container"><div class="title-gold">ALPHA VISION MULTI</div><div class="subtitle-white">visão de tubarão</div></div>', unsafe_allow_html=True)

# Criação das abas para não poluir o visual
tabs = st.tabs(list(ativos_config.keys()))

placeholder = st.empty()

while True:
    br_tz = pytz.timezone('America/Sao_Paulo')
    now_br = datetime.now(br_tz)

    # Reset Meia Noite Binance (18h BRT) conforme solicitado
    if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 5:
        for symbol in ativos_config:
            val = get_midpoint_multi(symbol)
            st.session_state.data[symbol] = {'mp': val, 'rv': val}
        st.rerun()

    for i, (symbol, config) in enumerate(ativos_config.items()):
        with tabs[i]:
            try:
                ticker = yf.Ticker(symbol)
                price = ticker.fast_info['last_price']
                
                mp = st.session_state.data[symbol]['mp']
                rv = st.session_state.data[symbol]['rv']
                
                var = ((price / mp) - 1) * 100
                
                # Lógica de Escada Dinâmica
                if var >= config['gatilho']:
                    st.session_state.data[symbol]['mp'] = mp * config['escada']
                elif var <= -config['gatilho']:
                    st.session_state.data[symbol]['mp'] = mp * (2 - config['escada'])

                # Renderização do Layout Original
                var_reset = ((price / rv) - 1) * 100
                cor_v = "#00FF00" if var_reset >= 0 else "#FF4444"
                seta_v = "▲" if var_reset >= 0 else "▼"
                
                alvos = config['alvos']
                
                st.markdown(f"""
                    <div class="header-container">
                        <div class="h-col">ATIVO</div><div class="h-col">PREÇO ATUAL</div>
                        <div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                        <div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div>
                        <div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div>
                    </div>
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37;">{symbol.replace('-USD','/USDT')}</div>
                        <div class="w-col">
                            <div>{price:,.2f}</div>
                            <div style="color:{cor_v}; font-size:11px;">{seta_v} {var_reset:+.2f}%</div>
                        </div>
                        <div class="w-col" style="color:#FF4444;">{int(mp * alvos[0]):,}</div>
                        <div class="w-col" style="color:#FFA500;">{int(mp * alvos[1]):,}</div>
                        <div class="w-col">{int(mp * alvos[2]):,}</div>
                        <div class="w-col" style="color:#00CED1;">{int(mp * alvos[3]):,}</div>
                        <div class="w-col" style="color:#FFA500;">{int(mp * alvos[4]):,}</div>
                        <div class="w-col" style="color:#00FF00;">{int(mp * alvos[5]):,}</div>
                    </div>
                    <div style="display: flex; justify-content: center; gap: 80px; margin-top: 15px;">
                        <div style="text-align: center;">
                            <div style="color: #888; font-size: 10px;">RESETVISION (24H)</div>
                            <div style="color: #ffffff; font-size: 19px;">{int(rv):,}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: #888; font-size: 10px;">ÂNCORAVISION (MÓVEL)</div>
                            <div style="color: #00e6ff; font-size: 19px;">{int(mp):,}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            except:
                st.write(f"Erro ao carregar {symbol}")

    st.markdown(f"""<div class="footer"><div><span class="dot"></span> LIVE: {datetime.now().strftime('%H:%M:%S')}</div></div>""", unsafe_allow_html=True)
    time.sleep(2)
