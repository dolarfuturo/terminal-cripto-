import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 32px; font-weight: 900; text-align: center; padding: 10px; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; }
    .h-col { font-size: 11px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 20px 0; border-bottom: 1px solid #151515; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 24px; font-weight: 800; color: #FFF; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #D4AF37; text-align: center; padding: 8px; font-size: 14px; border-top: 1px solid #333; font-weight: bold; }
    .reset-alert { background-color: #D4AF37; color: #000; text-align: center; font-weight: 900; padding: 5px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CICLO DIÁRIO (RESET 18H)
def get_daily_alpha_eixo():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        
        if now_br.hour < 18:
            if now_br.weekday() == 0: target_date = now_br - timedelta(days=3)
            else: target_date = now_br - timedelta(days=1)
        else:
            target_date = now_br

        if now_br.weekday() == 5: target_date = now_br - timedelta(days=1)
        if now_br.weekday() == 6: target_date = now_br - timedelta(days=2)

        df = yf.download("BTC-USD", start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_janela = df.between_time('11:30', '18:00')
        
        if not df_janela.empty:
            return (float(df_janela['High'].max()) + float(df_janela['Low'].min())) / 2
        return 89792.50
    except:
        return 89792.50

# 3. DASHBOARD
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)

if 'eixo_atual' not in st.session_state:
    st.session_state.eixo_atual = get_daily_alpha_eixo()

placeholder = st.empty()

while True:
    try:
        br_now = datetime.now(pytz.timezone('America/Sao_Paulo'))
        
        # Reset automático no minuto 18:00
        if br_now.hour == 18 and br_now.minute == 0 and br_now.second < 5:
            st.session_state.eixo_atual = get_daily_alpha_eixo()

        ticker = yf.Ticker("BTC-USD")
        price = ticker.fast_info['last_price']
        
        eixo = st.session_state.eixo_atual
        var = ((price / eixo) - 1) * 100
        cor_var = "#00FF00" if var >= 0 else "#FF0000"
        
        with placeholder.container():
            # Tarja de Atualização (Só aparece às 18:00)
            if br_now.hour == 18 and br_now.minute == 0:
                st.markdown('<div class="reset-alert">NOVO EIXO CALCULADO - JANELA 11:30/18:00 SINCRONIZADA</div>', unsafe_allow_html=True)

            st.markdown(f"""
                <div class="header-container">
                    <div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div>
                    <div class="h-col">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                    <div class="h-col">DECISÃO</div><div class="h-col">RESPIRO</div>
                    <div class="h-col">DECISÃO F.</div><div class="h-col">EXAUSTÃO F.</div>
                </div>
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37;">BTC/USDT</div>
                    <div class="w-col">{price:,.2f}<br><span style="color:{cor_var}; font-size:16px;">{var:+.2f}%</span></div>
                    <div class="w-col" style="color:#FF4444;">{eixo*1.0122:,.0f}</div>
                    <div class="w-col" style="color:#FFA500;">{eixo*1.0083:,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{eixo*1.0061:,.0f}</div>
                    <div class="w-col" style="color:#00CED1;">{eixo*1.0040:,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{eixo*0.9939:,.0f}</div>
                    <div class="w-col" style="color:#00FF00;">{eixo*0.9878:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Rodapé limpo apenas com o preço do Eixo
            st.markdown(f'<div class="footer">EIXO MESTRE: {eixo:,.2f} &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp; {br_now.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
            
        time.sleep(1)
    except:
        time.sleep(5)
