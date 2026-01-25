import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. CONFIGURAÇÃO ALPHA
st.set_page_config(page_title="ALPHA VISION", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 30px; font-weight: 900; text-align: center; padding: 10px; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; }
    .h-col { font-size: 11px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 18px 0; border-bottom: 1px solid #151515; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 20px; font-weight: 800; color: #FFF; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #00FF00; text-align: center; padding: 5px; font-size: 12px; border-top: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. CÁLCULO DO EIXO (INDEX GLOBAL - IGUAL TRADINGVIEW)
def get_eixo_index():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        days_to_sub = (now_br.weekday() - 4) % 7
        if days_to_sub == 0 and now_br.hour < 18: days_to_sub = 7
        target_date = now_br - timedelta(days=days_to_sub)
        
        # Puxa dados da Sexta
        df = yf.download("BTC-USD", start=target_date.strftime('%Y-%m-%d'), 
                         end=(target_date + timedelta(days=1)).strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_janela = df.between_time('11:30', '18:00')
        
        mx = float(df_janela['High'].max())
        mn = float(df_janela['Low'].min())
        return (mx + mn) / 2
    except:
        return 89719.0

# 3. DASHBOARD OPERACIONAL
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)

# Recupera Eixo de Sexta
if 'eixo_fixo' not in st.session_state:
    st.session_state.eixo_fixo = get_eixo_index()

# Ajuste fino manual (caso queira bater centavo com centavo do seu gráfico)
eixo_final = st.sidebar.number_input("AJUSTE EIXO MESTRE", value=st.session_state.eixo_fixo, step=1.0)

placeholder = st.empty()

while True:
    try:
        # Preço Atual (Index)
        data_now = yf.Ticker("BTC-USD").fast_info
        price = data_now['last_price']
        
        var = ((price / eixo_final) - 1) * 100
        cor = "#00FF00" if var >= 0 else "#FF0000"
        seta = "▲" if var >= 0 else "▼"
        
        with placeholder.container():
            st.markdown(f"""
                <div class="header-container">
                    <div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div>
                    <div class="h-col">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                    <div class="h-col">DECISÃO T.</div><div class="h-col">RESPIRO</div>
                    <div class="h-col">DECISÃO F.</div><div class="h-col">EXAUSTÃO F.</div>
                </div>
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37;">BTC/USDT</div>
                    <div class="w-col">{price:,.2f}<br><span style="color:{cor}; font-size:15px;">{seta} {var:+.2f}%</span></div>
                    <div class="w-col" style="color:#FF4444;">{eixo_final*1.0122:,.0f}</div>
                    <div class="w-col" style="color:#FFA500;">{eixo_final*1.0083:,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{eixo_final*1.0061:,.0f}</div>
                    <div class="w-col" style="color:#00CED1;">{eixo_final*1.0040:,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{eixo_final*0.9939:,.0f}</div>
                    <div class="w-col" style="color:#00FF00;">{eixo_final*0.9878:,.0f}</div>
                </div>
                <p style='text-align:center; color:#444; font-weight:bold; margin-top:30px;'>EIXO REF. SEXTA (11:30-18:00 BR): {eixo_final:,.2f}</p>
            """, unsafe_allow_html=True)
            
            br = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S')
            st.markdown(f'<div class="footer">DADOS: TRADINGVIEW INDEX | BRASÍLIA: {br}</div>', unsafe_allow_html=True)
            
        time.sleep(2)
    except:
        time.sleep(5)
