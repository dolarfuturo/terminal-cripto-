import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime, timedelta

# CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# CSS ESTILO TERMINAL (TERMUX / BLOOMBERG)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    .title-gold { color: #D4AF37; font-size: 45px; font-weight: 700; text-align: center; font-family: 'JetBrains Mono', monospace; }
    .subtitle-silver { color: #888; font-size: 18px; text-align: center; margin-top: -10px; letter-spacing: 4px; }
    
    /* CABEÇALHO MAIS DISCRETO */
    .header-container { display: flex; align-items: center; padding: 10px 0; border-bottom: 2px solid #D4AF37; background-color: #050505; }
    .col-head { color: #AAA; font-weight: 400; font-size: 14px; flex: 1; text-align: center; text-transform: uppercase; }

    /* LINHAS ESTILO TERMINAL */
    .row-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 16px; flex: 1; text-align: center; }
    .col-orange { color: #FF8C00; font-weight: 700; font-size: 17px; flex: 1; text-align: center; }
    .col-num { color: #CCC; font-size: 16px; flex: 1; text-align: center; }
    
    /* PONTOS DE AJUSTE (MÁXIMA E MÍNIMA) */
    .col-max { color: #FF4B4B; font-weight: 700; font-size: 17px; flex: 1; text-align: center; }
    .col-min { color: #00FF00; font-weight: 700; font-size: 17px; flex: 1; text-align: center; }

    /* LIVE STREAM VERDE */
    .live-text { color: #00FF00; font-weight: 700; font-size: 14px; letter-spacing: 1px; }
    .live-point { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink-live 1s infinite; }
    @keyframes blink-live { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    
    /* DATA E HORA DISCRETOS */
    .timestamp { color: #444; font-size: 12px; font-weight: 400; }

    /* SINAIS */
    @keyframes blinker { 50% { opacity: 0.3; } }
    .blink-red { background-color: #FF0000; color: white; font-weight: 700; padding: 6px; border-radius: 4px; animation: blinker 0.5s linear infinite; font-size: 13px; width: 90%; margin: auto; }
    .alert-orange { background-color: #FF8C00; color: white; font-weight: 700; padding: 6px; border-radius: 4px; font-size: 13px; width: 90%; margin: auto; }
    </style>
    """, unsafe_allow_html=True)

# Lógica para buscar as 100 moedas da Binance (Simplificada para o Layout)
def get_top_100():
    try:
        # Aqui o sistema buscaria o ticker da Binance de todos os pares USDT
        # Para o layout, vamos focar na estrutura
        return [
            {"ativo": "BTC/USDT", "preco": 93450.10, "fech": 91200.00, "abert": 92100.50, "max": 101310.50, "min": 82890.45, "sinal": "ESTÁVEL"},
            {"ativo": "ETH/USDT", "preco": 3845.00, "fech": 3710.00, "abert": 3750.20, "max": 4125.22, "min": 3375.18, "sinal": "ESTÁVEL"},
            {"ativo": "SOL/USDT", "preco": 148.88, "fech": 142.10, "abert": 144.50, "max": 158.95, "min": 130.05, "sinal": "GATILHO"},
        ] * 33 # Simulando 100 itens

placeholder = st.empty()

while True:
    with placeholder.container():
        horario_br = (datetime.utcnow() - timedelta(hours=3)).strftime('%H:%M:%S')
        data_br = (datetime.utcnow() - timedelta(hours=3)).strftime('%d/%m/%Y')
        
        st.markdown('<div class="title-gold">ALPHA VISION</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle-silver">QUANTITATIVE TERMINAL</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # CABEÇALHO LIMPO
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

        lista_moedas = get_top_100()

        for item in lista_moedas:
            sinal_div = f'<span style="color:#222;">---</span>'
            if "GATILHO" in item['sinal']:
                sinal_div = f'<div class="alert-orange">GATILHO 4%</div>'
            elif "EXAUSTÃO" in item['sinal']:
                sinal_div = f'<div class="blink-red">EXAUSTÃO 10%</div>'

            fmt = ".2f" if item['preco'] > 1 else ".6f"

            st.markdown(f"""
                <div class="row-container">
                    <div class="col-ativo">{item['ativo']}</div>
                    <div class="col-orange">{item['preco']:{fmt}}</div>
                    <div class="col-num">{item['fech']:{fmt}}</div>
                    <div class="col-num">{item['abert']:{fmt}}</div>
                    <div class="col-max">{item['max']:{fmt}}</div>
                    <div class="col-min">{item['min']:{fmt}}</div>
                    <div class="col-sinal" style="flex:1.5; text-align:center;">{sinal_div}</div>
                </div>
                """, unsafe_allow_html=True)

        # RODAPÉ DISCRETO ESTILO TERMINAL
        st.markdown(f"""
            <br>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 20px;">
                <div class="timestamp">{data_br} | {horario_br} BRT</div>
                <div class="live-text"><span class="live-point"></span> LIVE STREAMING</div>
                <div class="timestamp">STABLE CONNECTION</div>
            </div>
            """, unsafe_allow_html=True)

    time.sleep(1)
