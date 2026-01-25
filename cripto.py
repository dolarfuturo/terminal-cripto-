import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime
import pytz

# 1. CONFIGURAÇÃO DE TELA
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
    
    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 11px; width: 90%; margin: 0 auto; }
    .bg-estavel { background-color: #00CED1; color: #000; }
    .bg-decisao { background-color: #FFFF00; color: #000; }
    .bg-atencao { background-color: #FFA500; color: #000; }
    .target-blink { animation: blinker 0.8s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    
    .footer-clocks { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #000; color: #00FF00; 
                     text-align: center; padding: 10px; font-size: 14px; font-weight: bold; border-top: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. CÁLCULO DO EIXO (MÉDIA 11:30 - 18:00 BRASÍLIA)
def get_institutional_eixo():
    try:
        ticker = yf.Ticker("BTC-USD")
        hist = ticker.history(period="2d", interval="1m")
        br_tz = pytz.timezone('America/Sao_Paulo')
        hist.index = hist.index.tz_convert(br_tz)
        
        # Janela de 11:30 às 18:00
        df_janela = hist.between_time('11:30', '18:00')
        if not df_janela.empty:
            return (df_janela['High'].max() + df_janela['Low'].min()) / 2
        return 89795.0
    except:
        return 89795.0

# 3. MONITORAMENTO
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

EIXO_REAL = get_institutional_eixo()
placeholder = st.empty()

while True:
    try:
        btc = yf.Ticker("BTC-USD").fast_info
        price = btc['last_price']
        var_eixo = ((price / EIXO_REAL) - 1) * 100
        
        # Definição de Seta e Cor
        seta = "▲" if var_eixo >= 0 else "▼"
        cor_var = "#00FF00" if var_eixo >= 0 else "#FF0000"
        
        with placeholder.container():
            # Cabeçalho Limpo (Apenas Nomes)
            st.markdown("""
                <div class="header-container">
                    <div class="h-col">CÓDIGO</div>
                    <div class="h-col">PREÇO ATUAL</div>
                    <div class="h-col">EXAUSTÃO TOPO</div>
                    <div class="h-col">PRÓX. AO TOPO</div>
                    <div class="h-col">DECISÃO</div>
                    <div class="h-col">RESPIRO</div>
                    <div class="h-col">DECISÃO FUNDO</div>
                    <div class="h-col">EXAUSTÃO FUNDO</div>
                    <div class="h-col">SINALIZADOR</div>
                </div>
            """, unsafe_allow_html=True)

            def c(p): return EIXO_REAL * (1 + (p/100))
            
            # Lógica de Status
            abs_v = abs(var_eixo)
            s_txt, s_class = "ESTÁVEL", "bg-estavel"
            if abs_v >= 1.22: s_txt, s_class = "EXAUSTÃO", "target-blink"
            elif abs_v >= 0.83: s_txt, s_class = "PRÓX. TOPO", "bg-atencao"
            elif abs_v >= 0.61: s_txt, s_class = "DECISÃO", "bg-decisao"

            st.markdown(f"""
                <div class="row-container">
                    <div class="w-col" style="color:#D4AF37;">BTC/USDT</div>
                    <div class="w-col" style="color:#FFF;">{price:,.2f}<br>
                        <span style="font-size:14px; color:{cor_var};">{seta} {var_eixo:+.2f}%</span>
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

            # Exibição do Eixo em baixo da variação/hora (centralizado)
            st.markdown(f"<p style='color:#777; text-align:center; font-weight:bold;'>EIXO MESTRE (MÉDIA 11:30-18:00): {EIXO_REAL:,.2f}</p>", unsafe_allow_html=True)
            
            # Relógios no Rodapé
            br_now = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S')
            ny_now = datetime.now(pytz.timezone('America/New_York')).strftime('%H:%M:%S')
            st.markdown(f"""
                <div class="footer-clocks">
                    BRASÍLIA: {br_now} | NEW YORK: {ny_now} | RESET 00:00 UTC
                </div>
            """, unsafe_allow_html=True)
            
        time.sleep(2)
    except:
        time.sleep(5)
