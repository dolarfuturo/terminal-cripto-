import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. CONFIGURAÇÃO ALPHA VISION
st.set_page_config(page_title="ALPHA VISION BTC", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 38px; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 14px; text-align: center; letter-spacing: 5px; margin-bottom: 20px; }
    
    .header-container { display: flex; width: 100%; padding: 15px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; }
    .h-col { font-size: 12px; color: #FFFFFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 15px 0; border-bottom: 1px solid #151515; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 18px; font-weight: 800; }
    
    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 11px; width: 90%; margin: 0 auto; text-transform: uppercase; }
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-decisao { background-color: #FFFF00; color: #000; }
    .bg-atencao { background-color: #FFA500; color: #000; }
    .target-blink { animation: blinker 0.8s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    
    .footer-live { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #000; color: #00FF00; 
                     text-align: center; padding: 8px; font-size: 13px; font-weight: bold; border-top: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE INTELIGÊNCIA DO EIXO (SEG-SEX | 11:30-18:00 BR)
def get_institutional_eixo():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        
        # Se for Sábado (5) ou Domingo (6), ou Segunda antes das 18h, busca dados da Sexta
        if now_br.weekday() == 5: # Sábado
            target_date = now_br - timedelta(days=1)
        elif now_br.weekday() == 6: # Domingo
            target_date = now_br - timedelta(days=2)
        elif now_br.weekday() == 0 and now_br.hour < 18: # Segunda antes do fechamento
            target_date = now_br - timedelta(days=3)
        else:
            target_date = now_br

        ticker = yf.Ticker("BTC-USD")
        hist = ticker.history(start=target_date.strftime('%Y-%m-%d'), interval="1m")
        hist.index = hist.index.tz_convert(br_tz)
        
        # Filtra Janela 11:30 - 18:00
        df_janela = hist.between_time('11:30', '18:00')
        
        if not df_janela.empty:
            max_p = df_janela['High'].max()
            min_p = df_janela['Low'].min()
            return (max_p + min_p) / 2
        return 89795.0 # Fallback de segurança
    except:
        return 89795.0

# 3. MONITORAMENTO REAL-TIME
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

EIXO = get_institutional_eixo()
placeholder = st.empty()

while True:
    try:
        btc = yf.Ticker("BTC-USD").fast_info
        price = btc['last_price']
        var_eixo = ((price / EIXO) - 1) * 100
        
        seta = "▲" if price >= EIXO else "▼"
        cor_seta = "#00FF00" if price >= EIXO else "#FF0000"
        
        with placeholder.container():
            # Cabeçalho sem porcentagens, apenas nomes
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
                    <div class="h-col">SINALIZADOR</div>
                </div>
            """, unsafe_allow_html=True)

            def c(p): return EIXO * (1 + (p/100))
            
            # Lógica de Sinalizador
            abs_v = abs(var_eixo)
            s_txt, s_class = "ESTÁVEL", "bg-estavel"
            if abs_v >= 1.22: s_txt, s_class = "EXAUSTÃO", "target-blink"
            elif abs_v >= 0.83: s_txt, s_class = "PRÓX. TOPO", "bg-atencao"
            elif abs_v >= 0.61: s_txt, s_class = "DECISÃO", "bg-decisao"

            st.markdown(f"""
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37;">BTC/USDT</div>
                    <div class="w-col" style="color:#FFF;">{price:,.2f}<br>
                        <span style="color:{cor_seta}; font-size:15px;">{seta} {var_eixo:+.2f}%</span>
                    </div>
                    <div class="w-col" style="color:#FF4444;">{c(1.22):,.0f}</div>
                    <div class="w-col" style="color:#FFA500;">{c(0.83):,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{c(0.61):,.0f}</div>
                    <div class="w-col" style="color:#00CED1;">{c(0.40):,.0f}</div>
                    <div class="w-col" style="color:#FFFF00;">{c(-0.61):,.0f}</div>
                    <div class="w-col" style="color:#00FF00;">{c(-1.22):,.0f}</div>
                    <div class="w-col"><div class="status-box {s_class}">{s_txt}</div></div>
                </div>
            """, unsafe_allow_html=True)
            
            # Eixo fixo abaixo do preço
            st.markdown(f"<p style='color:#777; text-align:center; font-weight:bold; margin-top:10px;'>EIXO MESTRE ATIVO: {EIXO:,.2f}</p>", unsafe_allow_html=True)

            # Relógios e Reset
            br = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S')
            ny = datetime.now(pytz.timezone('America/New_York')).strftime('%H:%M:%S')
            st.markdown(f"""
                <div class="footer-live">
                    BRASÍLIA: {br} | NEW YORK: {ny} | RESET: 00:00 UTC
                </div>
            """, unsafe_allow_html=True)
            
        time.sleep(2)
    except:
        time.sleep(5)
