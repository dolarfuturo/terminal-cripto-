import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
from binance.client import Client

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# Inicializa o cliente da Binance
client = Client()

# 2. CSS TERMINAL COM BRILHO E ALERTAS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    .title-gold { 
        color: #D4AF37; font-size: 42px; font-weight: 700; text-align: center;
        text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.6); 
    }
    
    .header-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .col-head { font-size: 9px; flex: 1; text-align: center; font-weight: 800; text-transform: uppercase; }
    
    .head-yellow { color: #FFFF00; }
    .head-orange { color: #FFA500; }
    .head-red { color: #FF0000; }
    .head-green { color: #00FF00; }

    .row-container { display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 13px; flex: 1.2; font-weight: 700; padding-left: 10px; }
    .col-price { color: #FF8C00; font-weight: 800; font-size: 14px; flex: 1.5; text-align: center; }
    
    .status-box { padding: 6px; border-radius: 4px; font-weight: 800; font-size: 10px; width: 95%; margin: auto; text-align: center; color: white; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-exaustao { background-color: #FF0000; animation: blinker 0.6s linear infinite; box-shadow: 0px 0px 10px #FF0000; } 
    
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# 3. FUNÇÃO DE ÁUDIO (BEEP DE ALERTA)
def play_alert():
    audio_html = """
        <audio autoplay>
            <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
        </audio>
    """
    st.components.v1.html(audio_html, height=0)

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        # Busca Top 100 moedas por volume
        tickers = client.get_ticker()
        data = sorted([t for t in tickers if t['symbol'].endswith('USDT')], 
                      key=lambda x: float(x['quoteVolume']), reverse=True)[:100]
        
        trigger_sound = False
        
        with placeholder.container():
            st.markdown("""
                <div class="header-container">
                    <div class="col-head" style="flex:1.2; color:#BBB;">ATIVO</div>
                    <div class="col-head" style="flex:1.5; color:#BBB;">PREÇO (VAR%)</div>
                    <div class="col-head head-yellow">PONTO DECISÃO</div>
                    <div class="col-head head-orange">PRÓX TOPO CUIDADO</div>
                    <div class="col-head head-red">TETO EXAUSTÃO</div>
                    <div class="col-head head-yellow">SUPORTE DECISÃO</div>
                    <div class="col-head head-orange">PRÓX FUNDO CUIDADO</div>
                    <div class="col-head head-green">CHÃO EXAUSTÃO</div>
                    <div class="col-head" style="color:#BBB;">SINAL</div>
                </div>
                """, unsafe_allow_html=True)

            for t in data:
                price = float(t['lastPrice'])
                wap = float(t['weightedAvgPrice']) # WAP (Média ponderada)
                change = float(t['priceChangePercent'])
                
                # Seta baseada na WAP
                seta = '<span style="color:#00FF00;">▲</span>' if price >= wap else '<span style="color:#FF0000;">▼</span>'
                color_var = "#00FF00" if change >= 0 else "#FF0000"
                
                # Alvos
                v4, v8, v10 = price*1.04, price*1.08, price*1.10
                c4, c8, c10 = price*0.96, price*0.92, price*0.90
                
                prec = 8 if price < 1 else 2
                
                status = "ESTÁVEL"; s_class = "bg-estavel"
                if abs(change) >= 10: 
                    status = "EXAUSTÃO"; s_class = "bg-exaustao"
                    trigger_sound = True

                st.markdown(f"""
                    <div class="row-container">
                        <div class="col-ativo">{t['symbol']}</div>
                        <div class="col-price">
                            {price:.{prec}f}{seta} 
                            <span style="color:{color_var}; font-size:10px;">({change:+.2f}%)</span>
                        </div>
                        <div style="flex:1; text-align:center; color:#FFFF00;">{v4:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFA500;">{v8:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FF0000;">{v10:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFFF00;">{c4:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFA500;">{c8:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#00FF00;">{c10:.{prec}f}</div>
                        <div style="flex:1;"><div class="status-box {s_class}">{status}</div></div>
                    </div>
                """, unsafe_allow_html=True)
            
            if trigger_sound:
                play_alert()
                
        time.sleep(2)
    except Exception as e:
        time.sleep(5)
