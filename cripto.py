import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

# Estilos CSS mantidos (omitidos aqui para brevidade, permanecem os mesmos do seu original)
st.markdown("""<style>...</style>""", unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO ADAPTADO
def get_midpoint_multi(ticker_symbol):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        # Fallback values caso falhe
        fallbacks = {"BTC-USD": 82632, "ETH-USD": 2500, "BNB-USD": 600, "SOL-USD": 150, "XRP-USD": 0.60, "DOGE-USD": 0.15}
        
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download(ticker_symbol, start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not df.empty:
            df.index = df.index.tz_convert(br_tz)
            df_window = df.between_time('11:30', '18:00')
            if not df_window.empty:
                return float((df_window['High'].max() + df_window['Low'].min()) / 2)
        return fallbacks.get(ticker_symbol, 0)
    except:
        return fallbacks.get(ticker_symbol, 0)

# 3. CONFIGURAÇÃO DE ATIVOS
assets = {
    "BTC/USDT": "BTC-USD",
    "ETH/USDT": "ETH-USD",
    "BNB/USDT": "BNB-USD",
    "SOL/USDT": "SOL-USD",
    "XRP/USDT": "XRP-USD",
    "DOGE/USDT": "DOGE-USD"
}

# Inicialização do Estado Global
if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
    for label, symbol in assets.items():
        base_val = get_midpoint_multi(symbol)
        st.session_state.market_data[label] = {
            "mp_current": base_val,
            "rv_fixed": base_val,
            "symbol": symbol
        }

# 4. INTERFACE E LOOP
st.markdown("""<div class="title-container"><div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div></div>""", unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        
        # Auto-Reset 18:00 BR
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
            for label in assets.keys():
                new_val = get_midpoint_multi(st.session_state.market_data[label]["symbol"])
                st.session_state.market_data[label]["mp_current"] = new_val
                st.session_state.market_data[label]["rv_fixed"] = new_val
            st.rerun()

        with placeholder.container():
            # Header do Terminal
            st.markdown("""<div class="header-container">
                <div class="h-col">CÓDIGO</div><div class="h-col">PREÇO</div>
                <div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                <div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div>
                <div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div></div>""", unsafe_allow_html=True)

            for label, data in st.session_state.market_data.items():
                ticker = yf.Ticker(data["symbol"])
                price = ticker.fast_info['last_price']
                mp = data["mp_current"]
                rv = data["rv_fixed"]
                
                var = ((price / mp) - 1) * 100
                var_reset = ((price / rv) - 1) * 100

                # Lógica de Escada Individual
                if var >= 1.35:
                    st.session_state.market_data[label]["mp_current"] *= 1.0122
                elif var <= -1.35:
                    st.session_state.market_data[label]["mp_current"] *= 0.9878

                cor_v = "#00FF00" if var_reset >= 0 else "#FF4444"
                seta_v = "▲" if var_reset >= 0 else "▼"
                
                # Renderização da Linha por Ativo
                st.markdown(f"""
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37;">{label}</div>
                    <div class="w-col">
                        <div style="line-height: 1.1;">{price:,.2f}</div>
                        <div style="color:{cor_v}; font-size:11px;">{seta_v} {var_reset:+.2f}%</div>
                    </div>
                    <div class="w-col" style="color:#FF4444;">{int(mp*1.0122):,}</div>
                    <div class="w-col" style="color:#FFA500;">{int(mp*1.0083):,}</div>
                    <div class="w-col" style="color:#FFFF00;">{int(mp*1.0061):,}</div>
                    <div class="col" style="color:#00CED1;">{int(mp*1.0040):,}</div>
                    <div class="w-col" style="color:#00FF00;">{int(mp*0.9878):,}</div>
                </div>
                """, unsafe_allow_html=True)

            # Footer com relógios (mesma lógica original)
            st.markdown(f"""<div class="footer"><div>LIVESTREAM ATIVO</div><div>BRASÍLIA: {now_br.strftime('%H:%M:%S')}</div></div>""", unsafe_allow_html=True)
            
        time.sleep(1)
    except Exception as e:
        time.sleep(5)
