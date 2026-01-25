import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - LAYOUT AMPLO PARA NÃO EMBOLAR
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 32px; font-weight: 900; text-align: center; padding: 15px; }
    
    /* Container principal para dar espaço entre as colunas */
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-around; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; width: 12%; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 25px 0; border-bottom: 1px solid #151515; justify-content: space-around; }
    .w-col { width: 12%; text-align: center; font-family: 'monospace'; font-size: 20px; font-weight: 800; color: #FFF; white-space: nowrap; }
    
    /* Rodapé com Ponto Verde */
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 12px; font-size: 13px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 30px; z-index: 1000; }
    .dot { height: 12px; width: 12px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    
    .reset-alert { background-color: #D4AF37; color: #000; text-align: center; font-weight: 900; padding: 8px; font-size: 14px; margin-bottom: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO
def get_alpha_eixo_v7():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        if now_br.weekday() >= 5 or (now_br.weekday() == 0 and now_br.hour < 18):
            return 89792.500
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download("BTC-USD", start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_janela = df.between_time('11:30', '18:00')
        if not df_janela.empty:
            return (float(df_janela['High'].max()) + float(df_janela['Low'].min())) / 2
        return 89792.500
    except:
        return 89792.500

# 3. DASHBOARD
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)

if 'eixo_mestre' not in st.session_state:
    st.session_state.eixo_mestre = get_alpha_eixo_v7()

placeholder = st.empty()

while True:
    try:
        br_tz, ny_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York')
        now_br, now_ny = datetime.now(br_tz), datetime.now(ny_tz)
        
        # Reset 18:00
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
            st.session_state.eixo_mestre = get_alpha_eixo_v7()

        ticker = yf.Ticker("BTC-USD")
        price = ticker.fast_info['last_price']
        eixo = st.session_state.eixo_mestre
        var = ((price / eixo) - 1) * 100
        cor_var = "#00FF00" if var >= 0 else "#FF0000"
        
        with placeholder.container():
            # Sinal de Alerta Visual
            if now_br.hour == 18 and now_br.minute == 0:
                st.markdown('<div class="reset-alert">⚠️ EIXO ATUALIZADO (FECHAMENTO 18:00 BR)</div>', unsafe_allow_html=True)

            st.markdown(f"""
                <div class="header-container">
                    <div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div>
                    <div class="h-col">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                    <div class="h-col">DECISÃO</div><div class="h-col">RESPIRO</div>
                    <div class="h-col">DECISÃO F.</div><div class="h-col">EXAUSTÃO F.</div>
                </div>
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37;">BTC/USDT</div>
                    <div class="w-col">{price:,.3f}<br><span style="color:{cor_var}; font-size:15px;">{var:+.2f}%</span></div>
                    <div class="w-col" style="color:#FF4444;">{(eixo*1.0122):,.3f}</div>
                    <div class="w-col" style="color:#FFA500;">{(eixo*1.0083):,.3f}</div>
                    <div class="w-col" style="color:#FFFF00;">{(eixo*1.0061):,.3f}</div>
                    <div class="w-col" style="color:#00CED1;">{(eixo*1.0040):,.3f}</div>
                    <div class="w-col" style="color:#FFFF00;">{(eixo*0.9939):,.3f}</div>
                    <div class="w-col" style="color:#00FF00;">{(eixo*0.9878):,.3f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="footer">
                    <div><span class="dot"></span> LIVESTREAM ATIVO</div>
                    <div>EIXO MESTRE: <span style="color:#D4AF37;">{eixo:,.3f}</span></div>
                    <div>SÃO PAULO: {now_br.strftime('%H:%M:%S')}</div>
                    <div>NEW YORK: {now_ny.strftime('%H:%M:%S')}</div>
                </div>
            """, unsafe_allow_html=True)
            
        time.sleep(1)
    except:
        time.sleep(5)
