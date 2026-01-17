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
    
    .title-gold { color: #D4AF37; font-size: 40px; font-weight: 700; text-align: center; font-family: 'JetBrains Mono', monospace; letter-spacing: 2px; }
    .subtitle-silver { color: #555; font-size: 16px; text-align: center; margin-top: -10px; letter-spacing: 5px; text-transform: uppercase; }
    
    /* CABEÇALHO DISCRETO */
    .header-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #050505; margin-top: 20px; }
    .col-head { color: #777; font-weight: 400; font-size: 13px; flex: 1; text-align: center; }

    /* LINHAS ESTILO TERMINAL */
    .row-container { display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #DDD; font-size: 15px; flex: 1; text-align: center; }
    .col-orange { color: #FF8C00; font-weight: 700; font-size: 16px; flex: 1; text-align: center; }
    .col-num { color: #BBB; font-size: 15px; flex: 1; text-align: center; }
    
    /* MÁXIMA E MÍNIMA */
    .col-max { color: #FF4B4B; font-weight: 700; font-size: 16px; flex: 1; text-align: center; }
    .col-min { color: #00FF00; font-weight: 700; font-size: 16px; flex: 1; text-align: center; }

    /* LIVE STATUS VERDE NEON */
    .live-text { color: #00FF00; font-weight: 700; font-size: 13px; }
    .live-point { height: 9px; width: 9px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink-live 1s infinite; }
    @keyframes blink-live { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    
    /* DATA/HORA DISCRETOS */
    .timestamp { color: #333; font-size: 11px; }

    /* SINAIS DE ALERTA */
    @keyframes blinker { 50% { opacity: 0.3; } }
    .blink-red { background-color: #FF0000; color: white; font-weight: 700; padding: 5px; border-radius: 3px; animation: blinker 0.5s linear infinite; font-size: 12px; width: 85%; margin: auto; text-align: center;}
    .alert-orange { background-color: #FF8C00; color: white; font-weight: 700; padding: 5px; border-radius: 3px; font-size: 12px; width: 85%; margin: auto; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# 3. CABEÇALHO DO TERMINAL
st.markdown('<div class="title-gold">ALPHA VISION</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-silver">Quantitative Execution Terminal</div>', unsafe_allow_html=True)

placeholder = st.empty()

# 4. LOOP DE EXECUÇÃO
while True:
    with placeholder.container():
        # Ajuste de tempo
        agora = datetime.utcnow() - timedelta(hours=3)
        horario_br = agora.strftime('%H:%M:%S')
        data_br = agora.strftime('%d/%m/%Y')
        
        # Simulação das 100 moedas ordenadas (Aqui a lógica buscará da API)
        # Exemplo: BTC em 1º, ETH em 2º...
        moedas = [
            {"ativo": "BTC/USDT", "p": 93450.12, "f": 91200.0, "a": 92100.0, "mx": 101310.0, "mi": 82890.0, "s": "ESTÁVEL"},
            {"ativo": "ETH/USDT", "p": 3845.50, "f": 3710.0, "a": 3750.0, "mx": 4125.0, "mi": 3375.0, "s": "ESTÁVEL"},
            {"ativo": "SOL/USDT", "p": 148.88, "f": 142.1, "a": 144.5, "mx": 158.9, "mi": 130.0, "s": "GATILHO"},
        ] * 34 # Multiplicador para gerar a lista de ~100 itens

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

        for i, item in enumerate(moedas[:100]):
            sinal_html = '<span style="color:#111;">---</span>'
            if "GATILHO" in item['s']:
                sinal_html = '<div class="alert-orange">GATILHO 4%</div>'
            elif "EXAUSTÃO" in item['s']:
                sinal_html = '<div class="blink-red">EXAUSTÃO 10%</div>'

            fmt = ".2f" if item['p'] > 1 else ".6f"

            st.markdown(f"""
                <div class="row-container">
                    <div class="col-ativo">{item['ativo']}</div>
                    <div class="col-orange">{item['p']:{fmt}}</div>
                    <div class="col-num">{item['f']:{fmt}}</div>
                    <div class="col-num">{item['a']:{fmt}}</div>
                    <div class="col-max">{item['mx']:{fmt}}</div>
                    <div class="col-min">{item['mi']:{fmt}}</div>
                    <div class="col-sinal" style="flex:1.5;">{sinal_html}</div>
                </div>
                """, unsafe_allow_html=True)

        # 5. RODAPÉ ESTILO TERMINAL LIMPO
        st.markdown(f"""
            <br>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; border-top: 1px solid #222;">
                <div class="timestamp">{data_br} | {horario_br} BRT</div>
                <div class="live-text"><span class="live-point"></span> LIVE STREAMING</div>
                <div class="timestamp">TERMINAL ALPHA V1.0</div>
            </div>
            """, unsafe_allow_html=True)

    time.sleep(1)
