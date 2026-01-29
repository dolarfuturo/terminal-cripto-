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
    
    /* Ajuste Preciso do Subtítulo (H até Y) */
    .subtitle-white { 
        color: #FFFFFF; 
        font-size: 16px; 
        font-weight: 300; 
        letter-spacing: 5.5px; /* Calibrado para largura média H-Y */
        margin-top: 2px;
        text-transform: lowercase;
    }
    
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 25px 0; border-bottom: 1px solid #151515; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; white-space: nowrap; }
    
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 13px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 35px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO
def get_midpoint_v13():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        if now_br.weekday() >= 5 or (now_br.weekday() == 0 and now_br.hour < 18):
            return 89792
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download("BTC-USD", start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_window = df.between_time('11:30', '18:00')
        if not df_window.empty:
            return int((float(df_window['High'].max()) + float(df_window['Low'].min())) / 2)
        return 89792
    except:
        return 89792

# 3. INTERFACE REAL-TIME
st.markdown("""
    <div class="title-container">
        <div class="title-gold">ALPHA VISION CRYPTO</div>
        <div class="subtitle-white">visão de tubarão</div>
    </div>
    """, unsafe_allow_html=True)

if 'mp_current' not in st.session_state:
    st.session_state.mp_current = get_midpoint_v13()

placeholder = st.empty()

while True:
    try:
        br_tz, ny_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York')
        now_br, now_ny = datetime.now(br_tz), datetime.now(ny_tz)
        
        # Auto-Reset Binance (18:00 BR)
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
            st.session_state.mp_current = get_midpoint_v13()

        ticker = yf.Ticker("BTC-USD")
        price = ticker.fast_info['last_price']
        mp = st.session_state.mp_current
        var = ((price / mp) - 1) * 100
                   # --- LÓGICA DE ESCADA: AJUSTE AUTOMÁTICO DO PATAMAR ---
        if var >= 1.22:
            st.session_state.mp_current = int(mp * 1.0122)
            st.toast("⚡ ROMPIMENTO: NOVO EIXO!", icon="📈")
            st.rerun() 
            
        elif var <= -1.22:
            st.session_state.mp_current = int(mp * 0.9878)
            st.toast("⚠️ QUEDA: EIXO RECALIBRADO!", icon="📉")
            st.rerun()


                                        # --- LÓGICA DE DECISÃO ALPHA (FILTRO 1.35%) ---
        abs_var = abs(var)
        limite_rompimento = 1.35
        
        if 'mp_anterior' not in st.session_state:
            st.session_state.mp_anterior = mp

        # 1. VALIDAÇÃO DE ROMPIMENTO (O "JÁ ERA")
        if var >= limite_rompimento:
            st.session_state.mp_anterior = mp
            st.session_state.mp_current = int(mp * 1.0135) 
            st.toast("🚀 TENDÊNCIA CONFIRMADA: Eixo subiu (1.35%)", icon="📈")
            st.rerun()

        elif var <= -limite_rompimento:
            st.session_state.mp_anterior = mp
            st.session_state.mp_current = int(mp * 0.9865)
            st.toast("⚠️ QUEDA CONFIRMADA: Novo andar validado (1.35%).", icon="📉")
            st.rerun()

       # --- 2. CÁLCULO DOS PREÇOS ALVO ---
        mp = st.session_state.mp_current
        exaustao_t = mp * 1.0122
        prox_topo  = mp * 1.0084
        decisao    = mp * 1.0061
        respiro    = mp * 0.9946
        prox_f     = mp * 0.9904
        exaustao_f = mp * 0.9878

        # --- 3. VOLTA PARA BASE (Elasticidade) ---
        if st.session_state.mp_current > st.session_state.mp_anterior and price < st.session_state.mp_anterior:
            st.session_state.mp_current = st.session_state.mp_anterior
            st.rerun()
        elif st.session_state.mp_current < st.session_state.mp_anterior and price > st.session_state.mp_anterior:
            st.session_state.mp_current = st.session_state.mp_anterior
            st.rerun()

        # --- 4. LÓGICA DE CORES E SINALIZAÇÃO ---
        cor_var = "#00FF00" if var >= 0 else "#FF0000"
        animacao = ""
        seta = "▲" if var >= 0 else "▼"
        
        if 0.59 <= abs_var <= 0.64:
            cor_var = "#FFFF00" 
        elif 1.20 <= abs_var <= 1.25:
            animacao = "animation: blink 0.4s infinite;"

        # --- 5. INTERFACE VISUAL (BLOCOS ALVO) ---
        with placeholder.container():
            st.markdown(f"""
                <style>
                @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.1; }} 100% {{ opacity: 1; }} }}
                .h-col, .v-col {{ flex: 1; text-align: center; font-family: sans-serif; background-color: #000; }}
                </style>
                <div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #333;">
                    <div class="h-col" style="color: #888; font-size: 10px;">CÓDIGO</div>
                    <div class="h-col" style="color: #888; font-size: 10px;">PREÇO ATUAL</div>
                    <div class="h-col" style="color: {cor_var if var > 0 else '#888'}; {animacao if var > 0 else ''}; font-size: 10px;">EXAUSTÃO T.</div>
                    <div class="h-col" style="color: #888; font-size: 10px;">PRÓX. TOPO</div>
                    <div class="h-col" style="color: {cor_var if 0.59 <= abs_var <= 0.64 else '#888'}; font-size: 10px;">DECISÃO</div>
                    <div class="h-col" style="color: #888; font-size: 10px;">RESPIRO</div>
                    <div class="h-col" style="color: #888; font-size: 10px;">PRÓX. AO F.</div>
                    <div class="h-col" style="color: {cor_var if var < 0 else '#888'}; {animacao if var < 0 else ''}; font-size: 10px;">EXAUSTÃO F.</div>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 20px 10px;">
                    <div class="v-col" style="color: #FFD700; font-size: 18px;">BTC/USDT</div>
                    <div class="v-col" style="font-size: 24px;">{price:,.0f}<br><span style="font-size: 14px; color: {cor_var};">{seta} {var:.2f}%</span></div>
                    <div class="v-col" style="color: {cor_var if var > 0 else '#FF4B4B'}; {animacao if var > 0 else ''}; font-size: 24px;">{exaustao_t:,.0f}</div>
                    <div class="v-col" style="font-size: 24px;">{prox_topo:,.0f}</div>
                    <div class="v-col" style="color: {cor_var if 0.59 <= abs_var <= 0.64 else '#FFF'}; font-size: 24px;">{decisao:,.0f}</div>
                    <div class="v-col" style="font-size: 24px;">{respiro:,.0f}</div>
                    <div class="v-col" style="font-size: 24px;">{prox_f:,.0f}</div>
                    <div class="v-col" style="color: {cor_var if var < 0 else '#00FF00'}; {animacao if var < 0 else ''}; font-size: 24px;">{exaustao_f:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Erro na atualização: {e}")
