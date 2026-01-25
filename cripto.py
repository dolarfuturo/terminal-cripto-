import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime, timedelta
import pytz

# 1. ESTILO ALPHA
st.set_page_config(page_title="ALPHA VISION", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 35px; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; }
    .h-col { font-size: 11px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 12px 0; border-bottom: 1px solid #111; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 17px; font-weight: 800; color: #FFF; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #00FF00; text-align: center; padding: 5px; font-size: 12px; border-top: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. BUSCA MÁX/MÍN DA SEXTA (FUTUROS BINANCE - MAIS PRÓXIMO DO TRADINGVIEW)
def get_alpha_eixo():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        
        # Lógica para pegar a última sexta-feira
        days_to_sub = (now_br.weekday() - 4) % 7
        if days_to_sub == 0 and now_br.hour < 18: days_to_sub = 7
        target_date = now_br - timedelta(days=days_to_sub)
        
        # Timestamps 11:30 e 18:00
        s_dt = br_tz.localize(datetime(target_date.year, target_date.month, target_date.day, 11, 30))
        e_dt = br_tz.localize(datetime(target_date.year, target_date.month, target_date.day, 18, 0))
        
        # Puxa dados de 1m para precisão máxima no pavio
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1m&startTime={int(s_dt.timestamp()*1000)}&endTime={int(e_dt.timestamp()*1000)}"
        data = requests.get(url).json()
        
        df = pd.DataFrame(data, columns=['t','o','h','l','c','v','ct','qv','nt','tb','tq','i'])
        mx = df['h'].astype(float).max()
        mn = df['l'].astype(float).min()
        return (mx + mn) / 2, mx, mn
    except:
        return 89795.0, 0, 0

# 3. INTERFACE
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)

EIXO, MAX_S, MIN_S = get_alpha_eixo()
placeholder = st.empty()

while True:
    try:
        # Preço Atual Futuros (Mais rápido e bate com TV)
        price = float(requests.get("https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT").json()['price'])
        var = ((price / EIXO) - 1) * 100
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
                    <div class="w-col">{price:,.2f}<br><span style="color:{cor}; font-size:14px;">{seta} {var:+.2f}%</span></div>
                    <div class="w-col" style="color:#FF4444;">{EIXO*1.0122:,.0f}</div>
                    <div class="w-col" style="color:#FFA500;">{EIXO*1.0083:,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{EIXO*1.0061:,.0f}</div>
                    <div class="w-col" style="color:#00CED1;">{EIXO*1.0040:,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{EIXO*0.9939:,.0f}</div>
                    <div class="w-col" style="color:#00FF00;">{EIXO*0.9878:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.write(f"**CONFERÊNCIA TRADINGVIEW (SEXTA):** MÁX: {MAX_S:,.2f} | MÍN: {MIN_S:,.2f} | **EIXO: {EIXO:,.2f}**")
            
            hr = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S')
            st.markdown(f'<div class="footer">BINANCE FUTURES DATA | BRASÍLIA: {hr} | EIXO FIXO DE SEXTA-FEIRA</div>', unsafe_allow_html=True)
            
        time.sleep(2)
    except:
        time.sleep(5)
