import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

# CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# CSS DE ALTA PERFORMANCE - NITIDEZ TOTAL E LIVE STATUS
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 55px; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .subtitle-silver { color: #C0C0C0; font-size: 24px; text-align: center; margin-top: -10px; font-style: italic; letter-spacing: 6px; }
    
    /* NITIDEZ DOS NÚMEROS */
    .col-txt { color: #FFFFFF; font-weight: 800; font-size: 20px; flex: 1; text-align: center; }
    .col-orange { color: #FF8C00; font-weight: 900; font-size: 22px; flex: 1; text-align: center; }
    .col-num { color: #FFFFFF; font-weight: 700; font-size: 20px; flex: 1; text-align: center; }
    
    /* TABELA E LINHAS */
    .header-container { display: flex; align-items: center; padding: 15px 0; border-bottom: 3px solid #D4AF37; background-color: #0a0a0a; }
    .row-container { display: flex; align-items: center; padding: 18px 0; border-bottom: 1px solid #222; }

    /* PONTO LIVE PISCANTE */
    .live-point { height: 12px; width: 12px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; animation: blink-live 1s infinite; }
    @keyframes blink-live { 0% { opacity: 1; } 50% { opacity: 0.1; } 100% { opacity: 1; } }
    
    /* ALERTA EXAUSTÃO PISCANTE */
    .blink-red { background-color: #FF0000; color: white; font-weight: 900; padding: 12px; border-radius: 8px; animation: blinker 0.4s linear infinite; font-size: 16px; }
    .alert-orange { background-color: #FF8C00; color: white; font-weight: 900; padding: 12px; border-radius: 8px; font-size: 16px; }
    @keyframes blinker { 50% { opacity: 0.2; } }
    </style>
    """, unsafe_allow_html=True)

# CABEÇALHO
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-silver">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        # Horário de Brasília (UTC-3)
        horario_br = (datetime.utcnow() - timedelta(hours=3)).strftime('%d/%m/%Y | %H:%M:%S')
        
        # DADOS ORDENADOS POR VALOR (BTC -> ETH -> SOL -> ...)
        dados = [
            {"ativo": "BTC/USDT", "preco": 93450.10, "fech": 91200.00, "abert": 92100.50, "max": 101310.50, "min": 82890.45, "sinal": "ESTÁVEL"},
            {"ativo": "ETH/USDT", "preco": 3845.00, "fech": 3710.00, "abert": 3750.20, "max": 4125.22, "min": 3375.18, "sinal": "PREÇO JUSTO"},
            {"ativo": "SOL/USDT", "preco": 148.88, "fech": 142.10, "abert": 144.50, "max": 158.95, "min": 130.05, "sinal": "GATILHO (4%)"},
            {"ativo": "LINK/USDT", "preco": 14.25, "fech": 13.80, "abert": 14.00, "max": 15.40, "min": 12.60, "sinal": "ESTÁVEL"},
            {"ativo": "PEPE/USDT", "preco": 0.000022, "fech": 0.000019, "abert": 0.000020, "max": 0.000022, "min": 0.000018, "sinal": "EXAUSTÃO (10%)"},
        ]

        st.markdown("<br>", unsafe_allow_html=True)

        # TABELA PRINCIPAL
        st.markdown("""
            <div class="header-container">
                <div class="col-txt">ATIVO</div>
                <div class="col-txt">PREÇO</div>
                <div class="col-txt">FECH ANT</div>
                <div class="col-txt">ABERTURA</div>
                <div class="col-txt">MÁX (10%)</div>
                <div class="col-txt">MÍN (10%)</div>
                <div class="col-txt" style="flex:1.5;">SINAL ALERTA</div>
            </div>
            """, unsafe_allow_html=True)

        for item in dados:
            if "EXAUSTÃO" in item['sinal']:
                sinal_div = f'<div class="blink-red">{item["sinal"]}</div>'
            elif "GATILHO" in item['sinal']:
                sinal_div = f'<div class="alert-orange">{item["sinal"]}</div>'
            else:
                sinal_div = f'<span style="color:#444; font-weight:bold;">{item["sinal"]}</span>'

            # Formatação de decimais para PEPE
            fmt = ".2f" if item['preco'] > 1 else ".6f"

            st.markdown(f"""
                <div class="row-container">
                    <div class="col-txt">{item['ativo']}</div>
                    <div class="col-orange">{item['preco']:{fmt}}</div>
                    <div class="col-num">{item['fech']:{fmt}}</div>
                    <div class="col-num">{item['abert']:{fmt}}</div>
                    <div class="col-num" style="color:#FF4B4B">{item['max']:{fmt}}</div>
                    <div class="col-num" style="color:#00FF00">{item['min']:{fmt}}</div>
                    <div class="col-sinal" style="flex:1.5;">{sinal_div}</div>
                </div>
                """, unsafe_allow_html=True)

        # RODAPÉ LIVE STREAM
        st.markdown(f"""
            <br><br>
            <div style="text-align:center; color:#FFFFFF; font-family:sans-serif; font-weight:bold;">
                <span class="live-point"></span> LIVE STREAMING | HORÁRIO DE BRASÍLIA: {horario_br}
            </div>
            """, unsafe_allow_html=True)

    time.sleep(1)
