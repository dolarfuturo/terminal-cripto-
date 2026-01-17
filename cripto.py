import streamlit as st
import pandas as pd
import time
import base64
from datetime import datetime, timedelta
from binance.client import Client

# 1. CONFIGURAÇÃO DE INTERFACE E API
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")
client = Client() 

# 2. CSS TERMINAL PROFISSIONAL
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    .title-gold { 
        color: #D4AF37; font-size: 42px; font-weight: 700; text-align: center; margin-bottom: 0px;
        text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.6); 
    }
    .subtitle-vision { color: #C0C0C0; font-size: 18px; text-align: center; margin-top: -5px; letter-spacing: 8px; }
    
    .header-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; margin-top: 20px; position: sticky; top: 0; z-index: 99; }
    .col-head { font-size: 9px; flex: 1; text-align: center; font-weight: 800; text-transform: uppercase; }
    
    .head-yellow { color: #FFFF00; }
    .head-orange { color: #FFA500; }
    .head-red { color: #FF0000; }
    .head-green { color: #00FF00; }

    .row-container { display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 13px; flex: 1.2; text-align: left; padding-left: 10px; font-weight: 700; }
    .col-price { color: #FF8C00; font-weight: 800; font-size: 14px; flex: 1.3; text-align: center; }
    
    .status-box { padding: 4px; border-radius: 4px; font-weight: 800; font-size: 10px; width: 90%; margin: auto; text-align: center; color: white; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-exaustao { background-color: #FF0000; animation: blinker 0.6s linear infinite; box-shadow: 0px 0px 10px #FF0000; } 
    
    @keyframes blinker { 50% { opacity: 0.3; } }
    .live-text { color: #00FF00; font-weight: 700; font-size: 13px; }
    .live-point { height: 9px; width: 9px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink-live 1s infinite; }
    </style>
    """, unsafe_allow_html=True)

# 3. FUNÇÃO DE ALERTA SONORO
def play_alert():
    # Som de bip curto em base64 para evitar arquivos externos
    audio_str = "data:audio/wav;base64,UklGRl9vT19XQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YV9vT19" # Exemplo simplificado
    st.markdown(f'<audio autoplay><source src="{audio_str}" type="audio/wav"></audio>', unsafe_allow_html=True)

def get_binance_data():
    tickers = client.get_ticker()
    usdt_pairs = [t for t in tickers if t['symbol'].endswith('USDT')]
    top_100 = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)[:100]
    return top_100

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        data = get_binance_data()
        alert_triggered = False
        
        with placeholder.container():
            agora_br = datetime.utcnow() - timedelta(hours=3)
            
            st.markdown("""
                <div class="header-container">
                    <div class="col-head" style="flex:1.2; color:#BBB;">ATIVO</div>
                    <div class="col-head" style="flex:1.3; color:#BBB;">PREÇO (VAR%)</div>
                    <div class="col-head head-yellow">PONTO DECISÃO</div>
                    <div class="col-head head-orange">PRÓX TOPO CUIDADO</div>
                    <div class="col-head head-red">TETO EXAUSTÃO</div>
                    <div class="col-head head-yellow">SUPORTE DECISÃO</div>
                    <div class="col-head head-orange">PRÓX FUNDO CUIDADO</div>
                    <div class="col-head head-green">CHÃO EXAUSTÃO</div>
                    <div class="col-head" style="color:#BBB;">SINAL</div>
                </div>
                """, unsafe_allow_html=True)

            for ticker in data:
                symbol = ticker['symbol']
                price = float(ticker['lastPrice'])
                vwap = float(ticker['weightedAvgPrice'])
                change_pct = float(ticker['priceChangePercent'])
                
                seta = '<span style="color:#00FF00;">▲</span>' if price >= vwap else '<span style="color:#FF0000;">▼</span>'
                color_var = "#00FF00" if change_pct >= 0 else "#FF0000"

                v4, v8, v10 = price*1.04, price*1.08, price*1.10
                c4, c8, c10 = price*0.96, price*0.92, price*0.90
                
                prec = 8 if price < 1 else 2
                
                status = "ESTÁVEL"; status_class = "bg-estavel"
                # Alerta se bater +-10% de variação ou chegar perto dos pontos de exaustão
                if abs(change_pct) >= 10:
                    status = "EXAUSTÃO"; status_class = "bg-exaustao"
                    alert_triggered = True

                st.markdown(f"""
                    <div class="row-container">
                        <div class="col-ativo">{symbol}</div>
                        <div class="col-price">{price:.{prec}f}{seta}<span style="color:{color_var}; font-size:10px;">({change_pct:+.2f}%)</span></div>
                        <div style="flex:1; text-align:center; color:#FFFF00;">{v4:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFA500;">{v8:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FF0000;">{v10:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFFF00;">{c4:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFA500;">{c8:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#00FF00;">{c10:.{prec}f}</div>
                        <div style="flex:1;"><div class="status-box {status_class}">{status}</div></div>
                    </div>
                    """, unsafe_allow_html=True)

            if alert_triggered:
                play_alert()

            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 15px 20px; border-top: 1px solid #222;">
                    <div style="color:#333; font-size:11px;">{agora_br.strftime('%H:%M:%S')} BRT | VWAP RESET: 00:00 UTC (BINANCE)</div>
                    <div class="live-text"><span class="live-point"></span> LIVE STREAMING</div>
                </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        time.sleep(5)
    time.sleep(1)
