import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# 2. CSS ESTILO TERMINAL QUANTI (NITIDEZ TOTAL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    .title-gold { color: #D4AF37; font-size: 45px; font-weight: 700; text-align: center; margin-bottom: 0px; letter-spacing: 2px; }
    .subtitle-vision { color: #C0C0C0; font-size: 20px; text-align: center; margin-top: -5px; font-weight: 400; letter-spacing: 8px; text-transform: uppercase; }
    
    .header-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #050505; margin-top: 25px; }
    .col-head { color: #666; font-weight: 400; font-size: 13px; flex: 1; text-align: center; text-transform: uppercase; }

    .row-container { display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 15px; flex: 1; text-align: center; font-weight: 700; }
    .col-orange { color: #FF8C00; font-weight: 700; font-size: 16px; flex: 1; text-align: center; }
    .col-num { color: #CCC; font-size: 15px; flex: 1; text-align: center; }
    .col-max { color: #FF4B4B; font-weight: 700; font-size: 16px; flex: 1; text-align: center; }
    .col-min { color: #00FF00; font-weight: 700; font-size: 16px; flex: 1; text-align: center; }

    .status-box { padding: 8px; border-radius: 4px; font-weight: 700; font-size: 13px; width: 90%; margin: auto; text-align: center; color: white; text-transform: uppercase; }
    .bg-estavel { background-color: #008080; } 
    .bg-gatilho { background-color: #FF8C00; } 
    .bg-exaustao { background-color: #FF0000; animation: blinker 0.5s linear infinite; } 
    
    @keyframes blinker { 50% { opacity: 0.3; } }

    .live-text { color: #00FF00; font-weight: 700; font-size: 13px; }
    .live-point { height: 9px; width: 9px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink-live 1s infinite; }
    @keyframes blink-live { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    
    .timestamp { color: #333; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title-gold">ALPHA VISION</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        agora = datetime.utcnow() - timedelta(hours=3)
        horario_br = agora.strftime('%H:%M:%S')
        data_br = agora.strftime('%d/%m/%Y')
        
        # LISTA REAL DE ATIVOS (ORDEM POR MARKET CAP)
        nomes_reais = [
            "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT", "ADA/USDT", "TRX/USDT", 
            "LINK/USDT", "AVAX/USDT", "SHIB/USDT", "DOT/USDT", "BCH/USDT", "NEAR/USDT", "MATIC/USDT", "LTC/USDT",
            "PEPE/USDT", "UNI/USDT", "APT/USDT", "SUI/USDT", "RENDER/USDT", "HBAR/USDT", "ARB/USDT", "FIL/USDT"
        ]
        
        # Gerando 100 itens com nomes reais e complementos
        moedas_100 = []
        for i in range(100):
            nome = nomes_reais[i] if i < len(nomes_reais) else f"ASSET_{i}/USDT"
            
            # Simulando alguns gatilhos para teste visual
            status = "ESTÁVEL"
            if i == 2: status = "GATILHO"
            if i == 16: status = "EXAUSTÃO"
            
            moedas_100.append({
                "ativo": nome, "p": 100.0 / (i+1), "f": 98.0 / (i+1), "a": 99.0 / (i+1), 
                "mx": 110.0 / (i+1), "mi": 90.0 / (i+1), "s": status
            })

        st.markdown("""
            <div class="header-container">
                <div class="col-head">ATIVO</div>
                <div class="col-head">PREÇO</div>
                <div class="col-head">FECH ANT</div>
                <div class="col-head">ABERTURA</div>
                <div class="col-head">MÁXIMA</div>
                <div class="col-head">MÍNIMA</div>
                <div class="col-head" style="flex:1.5;">SINAL ALERTA</div>
            </div>
            """, unsafe_allow_html=True)

        for item in moedas_100:
            status_class = "bg-estavel"
            if "GATILHO" in item['s']: status_class = "bg-gatilho"
            elif "EXAUSTÃO" in item['s']: status_class = "bg-exaustao"

            fmt = ".2f" if item['p'] > 0.1 else ".6f"

            st.markdown(f"""
                <div class="row-container">
                    <div class="col-ativo">{item['ativo']}</div>
                    <div class="col-orange">{item['p']:{fmt}}</div>
                    <div class="col-num">{item['f']:{fmt}}</div>
                    <div class="col-num">{item['a']:{fmt}}</div>
                    <div class="col-max">{item['mx']:{fmt}}</div>
                    <div class="col-min">{item['mi']:{fmt}}</div>
                    <div class="col-sinal" style="flex:1.5;">
                        <div class="status-box {status_class}">{item['s']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
            <br>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; border-top: 1px solid #222;">
                <div class="timestamp">{data_br} | {horario_br} BRT</div>
                <div class="live-text"><span class="live-point"></span> LIVE STREAMING</div>
                <div class="timestamp">ALPHA VISION V1.0 - QUANT SYSTEM</div>
            </div>
            """, unsafe_allow_html=True)

    time.sleep(1)
