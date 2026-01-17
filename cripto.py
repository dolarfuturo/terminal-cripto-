import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# 2. CSS ESTILO TERMINAL QUANTI (TERMUX / BLOOMBERG)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    .title-gold { color: #D4AF37; font-size: 45px; font-weight: 700; text-align: center; margin-bottom: 0px; letter-spacing: 2px; }
    .subtitle-vision { color: #C0C0C0; font-size: 20px; text-align: center; margin-top: -5px; font-weight: 400; letter-spacing: 8px; text-transform: uppercase; }
    
    /* CABEÇALHO DISCRETO */
    .header-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #050505; margin-top: 25px; }
    .col-head { color: #666; font-weight: 400; font-size: 13px; flex: 1; text-align: center; text-transform: uppercase; }

    /* LINHAS ESTILO TERMINAL */
    .row-container { display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 15px; flex: 1; text-align: center; font-weight: 700; }
    .col-orange { color: #FF8C00; font-weight: 700; font-size: 16px; flex: 1; text-align: center; }
    .col-num { color: #CCC; font-size: 15px; flex: 1; text-align: center; }
    
    /* MÁXIMA E MÍNIMA */
    .col-max { color: #FF4B4B; font-weight: 700; font-size: 16px; flex: 1; text-align: center; }
    .col-min { color: #00FF00; font-weight: 700; font-size: 16px; flex: 1; text-align: center; }

    /* SINAIS COLORIDOS E PREENCHIDOS */
    .status-box { padding: 6px; border-radius: 4px; font-weight: 700; font-size: 12px; width: 90%; margin: auto; text-align: center; color: white; }
    .bg-estavel { background-color: #008080; } /* Azul Turquesa */
    .bg-gatilho { background-color: #FF8C00; } /* Laranja */
    .bg-exaustao { background-color: #FF0000; animation: blinker 0.5s linear infinite; } /* Vermelho Piscante */
    
    @keyframes blinker { 50% { opacity: 0.3; } }

    /* LIVE STATUS VERDE NEON */
    .live-text { color: #00FF00; font-weight: 700; font-size: 13px; }
    .live-point { height: 9px; width: 9px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink-live 1s infinite; }
    @keyframes blink-live { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    
    .timestamp { color: #333; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

# 3. CABEÇALHO DO TERMINAL
st.markdown('<div class="title-gold">ALPHA VISION</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

placeholder = st.empty()

# 4. LOOP DE EXECUÇÃO
while True:
    with placeholder.container():
        agora = datetime.utcnow() - timedelta(hours=3)
        horario_br = agora.strftime('%H:%M:%S')
        data_br = agora.strftime('%d/%m/%Y')
        
        # Simulação de Lista Única de 100 Ativos Reais (Mock)
        ativos_lista = [
            {"ativo": "BTC/USDT", "p": 93450.12, "f": 91200.0, "a": 92100.0, "mx": 101310.0, "mi": 82890.0, "s": "ESTÁVEL"},
            {"ativo": "ETH/USDT", "p": 3845.50, "f": 3710.0, "a": 3750.0, "mx": 4125.0, "mi": 3375.0, "s": "ESTÁVEL"},
            {"ativo": "SOL/USDT", "p": 148.88, "f": 142.1, "a": 144.5, "mx": 158.9, "mi": 130.0, "s": "GATILHO 4%"},
            {"ativo": "XRP/USDT", "p": 1.12, "f": 1.05, "a": 1.08, "mx": 1.23, "mi": 0.97, "s": "ESTÁVEL"},
            {"ativo": "BNB/USDT", "p": 612.40, "f": 590.0, "a": 600.0, "mx": 660.0, "mi": 540.0, "s": "ESTÁVEL"},
            {"ativo": "PEPE/USDT", "p": 0.000022, "f": 0.000019, "a": 0.000020, "mx": 0.000022, "mi": 0.000018, "s": "EXAUSTÃO 10%"},
        ]
        # Completa a lista até 100 para teste de scroll
        moedas_100 = ativos_lista + [{"ativo": f"TOKEN_{i}/USDT", "p": 1.0, "f": 0.9, "a": 0.95, "mx": 1.1, "mi": 0.8, "s": "ESTÁVEL"} for i in range(94)]

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
            # Lógica de cor do sinal
            status_class = "bg-estavel"
            if "GATILHO" in item['s']:
                status_class = "bg-gatilho"
            elif "EXAUSTÃO" in item['s']:
                status_class = "bg-exaustao"

            fmt = ".2f" if item['p'] > 1 else ".6f"

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

        # 5. RODAPÉ ESTILO TERMINAL
        st.markdown(f"""
            <br>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; border-top: 1px solid #222;">
                <div class="timestamp">{data_br} | {horario_br} BRT</div>
                <div class="live-text"><span class="live-point"></span> LIVE STREAMING</div>
                <div class="timestamp">ALPHA VISION V1.0 - QUANT SYSTEM</div>
            </div>
            """, unsafe_allow_html=True)

    time.sleep(1)
