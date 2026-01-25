import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime, timedelta
import pytz

# 1. CONFIGURAÇÃO DE TELA E ESTILO
st.set_page_config(page_title="ALPHA VISION", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 35px; font-weight: 900; text-align: center; padding: 20px 0; }
    .header-container { display: flex; width: 100%; padding: 15px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; }
    .h-col { font-size: 11px; color: #FFFFFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 18px 0; border-bottom: 1px solid #151515; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 18px; font-weight: 800; color: #FFF; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #000; color: #00FF00; text-align: center; padding: 10px; font-size: 13px; border-top: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO (Sexta-feira 11:30 - 18:00 BR)
def get_eixo_tradingview():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        # Busca a sexta-feira anterior se for fim de semana
        days_to_sub = (now_br.weekday() - 4) % 7
        if days_to_sub == 0 and now_br.hour < 18: days_to_sub = 7
        target_date = now_br - timedelta(days=days_to_sub)
        
        s_dt = br_tz.localize(datetime(target_date.year, target_date.month, target_date.day, 11, 30))
        e_dt = br_tz.localize(datetime(target_date.year, target_date.month, target_date.day, 18, 0))
        
        # API Binance Futures (Mais próximo do TradingView)
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1m&startTime={int(s_dt.timestamp()*1000)}&endTime={int(e_dt.timestamp()*1000)}"
        data = requests.get(url).json()
        df = pd.DataFrame(data, columns=['t','o','h','l','c','v','ct','qv','nt','tb','tq','i'])
        mx = df['h'].astype(float).max()
        mn = df['l'].astype(float).min()
        return (mx + mn) / 2
    except:
        return 89795.0

# 3. INTERFACE OPERACIONAL
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)

# Opção de ajuste manual caso o automático discorde do seu TradingView
EIXO_BASE = st.sidebar.number_input("Ajuste Manual do Eixo", value=get_eixo_tradingview(), step=1.0)

placeholder = st.empty()

while True:
    try:
        # Preço Atual em Tempo Real
        r = requests.get("https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT").json()
        price = float(r['price'])
        
        var = ((price / EIXO_BASE) - 1) * 100
        cor_var = "#00FF00" if var >= 0 else "#FF0000"
        seta = "▲" if var >= 0 else "▼"
        
        with placeholder.container():
            # Cabeçalho Limpo (Apenas Nomes)
            st.markdown("""
                <div class="header-container">
                    <div class="h-col">CÓDIGO</div>
                    <div class="h-col">PREÇO ATUAL</div>
                    <div class="h-col">EXAUSTÃO TOPO</div>
                    <div class="h-col">PRÓX. TOPO</div>
                    <div class="h-col">DECISÃO</div>
                    <div class="h-col">RESPIRO</div>
                    <div class="h-col">DECISÃO FUNDO</div>
                    <div class="h-col">EXAUSTÃO FUNDO</div>
                </div>
            """, unsafe_allow_html=True)

            # Função de cálculo da planilha
            def calc(p): return EIXO_BASE * (1 + (p/100))

            st.markdown(f"""
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37;">BTC/USDT</div>
                    <div class="w-col">{price:,.2f}<br>
                        <span style="color:{cor_var}; font-size:15px;">{seta} {var:+.2f}%</span>
                    </div>
                    <div class="w-col" style="color:#FF4444;">{calc(1.22):,.0f}</div>
                    <div class="w-col" style="color:#FFA500;">{calc(0.83):,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{calc(0.61):,.0f}</div>
                    <div class="w-col" style="color:#00CED1;">{calc(0.40):,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{calc(-0.61):,.0f}</div>
                    <div class="w-col" style="color:#00FF00;">{calc(-1.22):,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<p style='text-align:center; color:#555; font-weight:bold; margin-top:15px;'>EIXO ATUAL: {EIXO_BASE:,.2f}</p>", unsafe_allow_html=True)
            
            br = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S')
            st.markdown(f'<div class="footer">DADOS: BINANCE PERPETUAL | BRASÍLIA: {br} | JANELA REF: 11:30-18:00</div>', unsafe_allow_html=True)
            
        time.sleep(1)
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
        time.sleep(5)
