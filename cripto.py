import streamlit as st
import pandas as pd
import time
import ccxt
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# Inicializa exchange via CCXT (Mais estável para nuvem)
exchange = ccxt.binance()

# 2. CSS ESTILO TERMINAL ALPHA VISION
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 40px; font-weight: 700; text-align: center; text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.6); }
    .header-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .col-head { font-size: 9px; flex: 1; text-align: center; font-weight: 800; text-transform: uppercase; }
    .row-container { display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 13px; flex: 1.2; font-weight: 700; padding-left: 10px; }
    .col-price { color: #FF8C00; font-weight: 800; font-size: 14px; flex: 1.5; text-align: center; }
    .status-box { padding: 4px; border-radius: 4px; font-weight: 800; font-size: 10px; width: 90%; margin: auto; text-align: center; color: white; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-exaustao { background-color: #FF0000; animation: blinker 0.6s linear infinite; } 
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

def play_alert():
    audio_html = '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>'
    st.components.v1.html(audio_html, height=0)

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
placeholder = st.empty()

while True:
    try:
        # Busca dados de mercado
        tickers = exchange.fetch_tickers()
        # Filtra Top 50 USDT por volume
        data = [t for t in tickers.values() if t['symbol'].endswith('/USDT')]
        top_data = sorted(data, key=lambda x: x['quoteVolume'], reverse=True)[:50]
        
        trigger_sound = False
        
        with placeholder.container():
            st.markdown("""
                <div class="header-container">
                    <div class="col-head" style="flex:1.2; color:#BBB;">ATIVO</div>
                    <div class="col-head" style="flex:1.5; color:#BBB;">PREÇO (VAR%)</div>
                    <div class="col-head" style="color:#FFFF00;">PONTO DECISÃO</div>
                    <div class="col-head" style="color:#FFA500;">PRÓX TOPO CUIDADO</div>
                    <div class="col-head" style="color:#FF0000;">TETO EXAUSTÃO</div>
                    <div class="col-head" style="color:#FFFF00;">SUPORTE DECISÃO</div>
                    <div class="col-head" style="color:#FFA500;">PRÓX FUNDO CUIDADO</div>
                    <div class="col-head" style="color:#00FF00;">CHÃO EXAUSTÃO</div>
                    <div class="col-head" style="color:#BBB;">SINAL</div>
                </div>
                """, unsafe_allow_html=True)

            for t in top_data:
                sym = t['symbol'].replace('/USDT', '')
                price = t['last']
                vwap = t['vwap'] if t['vwap'] else price # Usa preço atual se VWAP não disponível
                change = t['percentage']
                
                seta = '<span style="color:#00FF00;">▲</span>' if price >= vwap else '<span style="color:#FF0000;">▼</span>'
                color_var = "#00FF00" if change >= 0 else "#FF0000"
                prec = 8 if price < 1 else 2
                
                # Alvos
                v4, v8, v10 = price*1.04, price*1.08, price*1.10
                c4, c8, c10 = price*0.96, price*0.92, price*0.90
                
                status = "ESTÁVEL"; s_class = "bg-estavel"
                if abs(change) >= 10: 
                    status = "EXAUSTÃO"; s_class = "bg-exaustao"
                    trigger_sound = True

                st.markdown(f"""
                    <div class="row-container">
                        <div class="col-ativo">{sym}/USDT</div>
                        <div class="col-price">{price:.{prec}f}{seta}<span style="color:{color_var}; font-size:10px;">({change:+.2f}%)</span></div>
                        <div style="flex:1; text-align:center; color:#FFFF00; font-size:12px;">{v4:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFA500; font-size:12px;">{v8:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FF0000; font-size:12px;">{v10:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFFF00; font-size:12px;">{c4:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFA500; font-size:12px;">{c8:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#00FF00; font-size:12px;">{c10:.{prec}f}</div>
                        <div style="flex:1;"><div class="status-box {s_class}">{status}</div></div>
                    </div>
                """, unsafe_allow_html=True)
            
            if trigger_sound: play_alert()
                
        time.sleep(5) # Delay maior para evitar block
    except Exception as e:
        st.error(f"Sincronizando com a rede...")
        time.sleep(10)

