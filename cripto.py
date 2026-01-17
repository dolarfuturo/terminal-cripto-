import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# 2. CSS TERMINAL COM BRILHO E PRECISÃO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    /* TÍTULO COM BRILHO */
    .title-gold { 
        color: #D4AF37; font-size: 42px; font-weight: 700; text-align: center; margin-bottom: 0px;
        text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.6); 
    }
    .subtitle-vision { color: #C0C0C0; font-size: 18px; text-align: center; margin-top: -5px; letter-spacing: 8px; }
    
    /* CABEÇALHO COM DESTAQUE NAS CORES DOS PONTOS */
    .header-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; margin-top: 20px; }
    .col-head { font-size: 10px; flex: 1; text-align: center; font-weight: 800; text-transform: uppercase; }
    
    /* CORES DO CABEÇALHO (REF 4, 8, 10%) */
    .head-white { color: #BBB; }
    .head-yellow { color: #FFFF00; text-shadow: 0px 0px 5px rgba(255, 255, 0, 0.5); }
    .head-orange { color: #FFA500; text-shadow: 0px 0px 5px rgba(255, 165, 0, 0.5); }
    .head-red { color: #FF0000; text-shadow: 0px 0px 5px rgba(255, 0, 0, 0.5); }
    .head-green { color: #00FF00; text-shadow: 0px 0px 5px rgba(0, 255, 0, 0.5); }

    .row-container { display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 14px; flex: 1.2; text-align: left; padding-left: 10px; font-weight: 700; }
    
    /* PREÇO COM SETA */
    .col-price { color: #FF8C00; font-weight: 800; font-size: 15px; flex: 1; text-align: center; }
    .up-arrow { color: #00FF00; font-size: 12px; margin-left: 4px; }
    .down-arrow { color: #FF0000; font-size: 12px; margin-left: 4px; }

    /* PONTOS CALCULADOS SEM ARREDONDAMENTO */
    .ponto-val { font-size: 13px; flex: 1; text-align: center; font-weight: 600; }

    /* STATUS LATERAL CONFIGURADO */
    .status-box { padding: 6px; border-radius: 4px; font-weight: 800; font-size: 11px; width: 95%; margin: auto; text-align: center; color: white; }
    .bg-estavel { background-color: #00CED1; color: #000; } /* Azul Clarinho Turquesa */
    .bg-decisao { background-color: #FFFF00; color: #000; } /* Amarelo */
    .bg-cuidado { background-color: #FFA500; color: #000; } /* Laranja */
    .bg-exaustao { background-color: #FF0000; animation: blinker 0.6s linear infinite; } /* Vermelho */
    
    @keyframes blinker { 50% { opacity: 0.3; } }
    .live-text { color: #00FF00; font-weight: 700; font-size: 13px; }
    .live-point { height: 9px; width: 9px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink-live 1s infinite; }
    @keyframes blink-live { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

placeholder = st.empty()

# Lista de 100 Ativos Reais
nomes_mercado = [
    "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT", "ADA/USDT", "LINK/USDT", "AVAX/USDT", "PEPE/USDT",
    "SHIB/USDT", "DOT/USDT", "BCH/USDT", "NEAR/USDT", "MATIC/USDT", "LTC/USDT", "UNI/USDT", "APT/USDT", "SUI/USDT", "RENDER/USDT"
] * 5 

while True:
    with placeholder.container():
        horario_br = (datetime.utcnow() - timedelta(hours=3)).strftime('%H:%M:%S')
        
        # CABEÇALHO SINALIZADO POR CORES
        st.markdown("""
            <div class="header-container">
                <div class="col-head head-white" style="flex:1.2;">ATIVO</div>
                <div class="col-head head-white">PREÇO ATUAL</div>
                <div class="col-head head-yellow">PONTO DECISÃO (4%)</div>
                <div class="col-head head-orange">PRÓX TOPO (8%)</div>
                <div class="col-head head-red">TETO EXAUSTÃO (10%)</div>
                <div class="col-head head-yellow">SUPORTE DECISÃO (4%)</div>
                <div class="col-head head-orange">PRÓX FUNDO (8%)</div>
                <div class="col-head head-green">CHÃO EXAUSTÃO (10%)</div>
                <div class="col-head head-white">SINAL</div>
            </div>
            """, unsafe_allow_html=True)

        for i, nome in enumerate(nomes_mercado):
            # Preços simulados mantendo decimais originais
            p = 93450.12345678 / (i + 1) if "BTC" in nome else 1.23456789 / (i+1)
            
            # Cálculo de Pontos
            v4, v8, v10 = p*1.04, p*1.08, p*1.10
            c4, c8, c10 = p*0.96, p*0.92, p*0.90
            
            # Seta de tendência aleatória para o Live
            seta = '<span class="up-arrow">▲</span>' if random.random() > 0.5 else '<span class="down-arrow">▼</span>'
            
            # Lógica de Alerta por Cores
            status = "ESTÁVEL"; status_class = "bg-estavel"
            if i == 2: status = "DECISÃO"; status_class = "bg-decisao"
            if i == 5: status = "CUIDADO"; status_class = "bg-cuidado"
            if i == 9: status = "EXAUSTÃO"; status_class = "bg-exaustao"

            # Precisão decimal dinâmica para não confundir operadores
            prec = 8 if p < 1 else 2

            st.markdown(f"""
                <div class="row-container">
                    <div class="col-ativo">{nome}</div>
                    <div class="col-price">{p:.{prec}f}{seta}</div>
                    <div class="ponto-val" style="color:#FFFF00;">{v4:.{prec}f}</div>
                    <div class="ponto-val" style="color:#FFA500;">{v8:.{prec}f}</div>
                    <div class="ponto-val" style="color:#FF0000;">{v10:.{prec}f}</div>
                    <div class="ponto-val" style="color:#FFFF00;">{c4:.{prec}f}</div>
                    <div class="ponto-val" style="color:#FFA500;">{c8:.{prec}f}</div>
                    <div class="ponto-val" style="color:#00FF00;">{c10:.{prec}f}</div>
                    <div style="flex:1;">
                        <div class="status-box {status_class}">{status}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
            <br><div style="display: flex; justify-content: space-between; padding: 10px 20px;">
                <div style="color:#333; font-size:11px;">{horario_br} BRT | ALPHA QUANT SYSTEM</div>
                <div class="live-text"><span class="live-point"></span> LIVE STREAMING</div>
            </div>
            """, unsafe_allow_html=True)
    time.sleep(1)
