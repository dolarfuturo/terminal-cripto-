import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# 2. CSS TERMINAL BLOOMBERG/TERMUX (NITIDEZ EXTREMA)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    .title-gold { color: #D4AF37; font-size: 45px; font-weight: 700; text-align: center; margin-bottom: 0px; }
    .subtitle-vision { color: #C0C0C0; font-size: 18px; text-align: center; margin-top: -5px; letter-spacing: 8px; }
    
    .header-container { display: flex; align-items: center; padding: 10px 0; border-bottom: 2px solid #D4AF37; background-color: #050505; margin-top: 20px; }
    .col-head { color: #666; font-size: 11px; flex: 1; text-align: center; }

    .row-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 14px; flex: 1.2; text-align: left; padding-left: 10px; font-weight: 700; }
    .col-orange { color: #FF8C00; font-weight: 700; font-size: 15px; flex: 1; text-align: center; }
    
    /* CORES DOS ALVOS */
    .col-venda { color: #FF4B4B; font-size: 14px; flex: 1; text-align: center; border-left: 1px solid #222; }
    .col-compra { color: #00FF00; font-size: 14px; flex: 1; text-align: center; border-left: 1px solid #222; }

    .status-box { padding: 6px; border-radius: 4px; font-weight: 700; font-size: 11px; width: 95%; margin: auto; text-align: center; color: white; }
    .bg-estavel { background-color: #111; color: #444; border: 1px solid #333; } 
    .bg-gatilho { background-color: #FF8C00; } 
    .bg-exaustao { background-color: #FF0000; animation: blinker 0.5s linear infinite; } 
    
    @keyframes blinker { 50% { opacity: 0.3; } }
    .live-text { color: #00FF00; font-weight: 700; font-size: 13px; }
    .live-point { height: 9px; width: 9px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink-live 1s infinite; }
    @keyframes blink-live { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title-gold">ALPHA VISION</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

# 3. LISTA DE 100 MOEDAS REAIS (RESUMIDA NO CÓDIGO MAS GERA 100 NO LOOP)
nomes_mercado = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT", "ADA/USDT", "LINK/USDT", "AVAX/USDT", "DOT/USDT"] # ... (expansível até 100)

placeholder = st.empty()

while True:
    with placeholder.container():
        horario_br = (datetime.utcnow() - timedelta(hours=3)).strftime('%H:%M:%S')
        
        # CABEÇALHO COM OS ALVOS ESPECÍFICOS
        st.markdown("""
            <div class="header-container">
                <div class="col-head" style="flex:1.2;">ATIVO</div>
                <div class="col-head">PREÇO ATUAL</div>
                <div class="col-head">VENDA 4%</div>
                <div class="col-head">VENDA 8%</div>
                <div class="col-head">VENDA 10%</div>
                <div class="col-head">COMPRA 4%</div>
                <div class="col-head">COMPRA 8%</div>
                <div class="col-head">COMPRA 10%</div>
                <div class="col-head">STATUS</div>
            </div>
            """, unsafe_allow_html=True)

        for i in range(100):
            nome = nomes_mercado[i % len(nomes_mercado)]
            p = 100.0 / (i + 1) # Simulação de preço
            
            # Cálculo dos Pontos (Baseado na Wap/Preço de Referência)
            v4, v8, v10 = p*1.04, p*1.08, p*1.10
            c4, c8, c10 = p*0.96, p*0.92, p*0.90
            
            status = "ESTÁVEL"
            status_class = "bg-estavel"
            if i == 2: 
                status = "GATILHO"; status_class = "bg-gatilho"
            if i == 5: 
                status = "EXAUSTÃO"; status_class = "bg-exaustao"

            fmt = ".2f" if p > 0.1 else ".6f"

            st.markdown(f"""
                <div class="row-container">
                    <div class="col-ativo">{nome}</div>
                    <div class="col-orange">{p:{fmt}}</div>
                    <div class="col-venda">{v4:{fmt}}</div>
                    <div class="col-venda">{v8:{fmt}}</div>
                    <div class="col-venda" style="font-weight:900;">{v10:{fmt}}</div>
                    <div class="col-compra">{c4:{fmt}}</div>
                    <div class="col-compra">{c8:{fmt}}</div>
                    <div class="col-compra" style="font-weight:900;">{c10:{fmt}}</div>
                    <div style="flex:1;">
                        <div class="status-box {status_class}">{status}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
            <br><div style="display: flex; justify-content: space-between; padding: 10px 20px;">
                <div style="color:#333; font-size:11px;">{horario_br} BRT | QUANT SYSTEM</div>
                <div class="live-text"><span class="live-point"></span> LIVE STREAMING</div>
            </div>
            """, unsafe_allow_html=True)
    time.sleep(1)
