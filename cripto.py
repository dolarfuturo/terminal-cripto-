import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime, timedelta
import pytz

# 1. CONFIGURAÇÃO VISUAL
st.set_page_config(page_title="ALPHA VISION BTC", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 32px; font-weight: 900; text-align: center; padding: 10px 0; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; }
    .h-col { font-size: 11px; color: #FFFFFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 15px 0; border-bottom: 1px solid #151515; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 19px; font-weight: 800; color: #FFF; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #000; color: #00FF00; text-align: center; padding: 5px; font-size: 12px; border-top: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. CÁLCULO DO EIXO (DADOS DE CONTRATOS PERPÉTUOS - TRADINGVIEW)
@st.cache_data(ttl=600)
def get_tradingview_eixo():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        
        # Lógica para travar na Sexta-Feira
        days_to_sub = (now_br.weekday() - 4) % 7
        if days_to_sub == 0 and now_br.hour < 18: days_to_sub = 7
        target_date = now_br - timedelta(days=days_to_sub)
        
        # Janela 11:30 - 18:00
        s_dt = br_tz.localize(datetime(target_date.year, target_date.month, target_date.day, 11, 30))
        e_dt = br_tz.localize(datetime(target_date.year, target_date.month, target_date.day, 18, 0))
        
        # Chama API de Futuros (BTCUSDT Perpetual)
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1m&startTime={int(s_dt.timestamp()*1000)}&endTime={int(e_dt.timestamp()*1000)}"
        resp = requests.get(url, timeout=10).json()
        
        df = pd.DataFrame(resp, columns=['t','o','h','l','c','v','ct','qv','nt','tb','tq','i'])
        mx = df['h'].astype(float).max()
        mn = df['l'].astype(float).min()
        return (mx + mn) / 2
    except:
        return 89719.50 # Fallback baseado no fechamento de sexta

# 3. DASHBOARD
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)

EIXO_TV = get_tradingview_eixo()
placeholder = st.empty()

while True:
    try:
        # Preço Real-Time (Binance Futures)
        r = requests.get("https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT", timeout=2).json()
        price = float(r['price'])
        
        var = ((price / EIXO_TV) - 1) * 100
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
                    <div class="w-col" style="color:#FF4444;">{EIXO_TV*1.0122:,.0f}</div>
                    <div class="w-col" style="color:#FFA500;">{EIXO_TV*1.0083:,.0f}</div>
                    <div class="h-col" style="color:#FFFF00; font-size:18px; font-weight:800; flex:1; text-align:center;">{EIXO_TV*1.0061:,.0f}</div>
                    <div class="w-col" style="color:#00CED1;">{EIXO_TV*1.0040:,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{EIXO_TV*0.9939:,.0f}</div>
                    <div class="w-col" style="color:#00FF00;">{EIXO_TV*0.9878:,.0f}</div>
                </div>
                <p style='text-align:center; color:#777; font-weight:bold; margin-top:25px;'>EIXO TRADINGVIEW (SEXTA): {EIXO_TV:,.2f}</p>
            """, unsafe_allow_html=True)
            
            br = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S')
            st.markdown(f'<div class="footer">DADOS: BINANCE FUTURES (TV) | BRASÍLIA: {br}</div>', unsafe_allow_html=True)
            
        time.sleep(1)
    except:
        time.sleep(2)
