import streamlit as st
import pandas as pd
import time
from datetime import datetime

# CONFIGURAÇÃO DE INTERFACE DE ALTA PERFORMANCE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# CSS PARA LAYOUT BLACK & LEDS PISCANTES
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 48px; font-weight: bold; text-align: center; margin-bottom: 0px; }
    .subtitle-silver { color: #C0C0C0; font-size: 20px; text-align: center; margin-top: -10px; font-style: italic; letter-spacing: 3px; }
    
    /* Blocos Superiores com Preço Laranja */
    [data-testid="stMetricLabel"] p { color: #FFFFFF !important; font-weight: bold !important; font-size: 22px !important; }
    [data-testid="stMetricValue"] { color: #FFA500 !important; font-weight: bold !important; }
    div[data-testid="stMetric"] { 
        background-color: #000000 !important; 
        border: 1px solid #333333; 
        border-radius: 10px; 
        padding: 15px; 
    }
    
    /* Efeito Piscante para Exaustão */
    @keyframes blinker {  
        50% { opacity: 0.2; }
    }
    .blink-exaustao {
        background-color: #FF0000 !important;
        color: white !important;
        font-weight: bold !important;
        animation: blinker 0.6s linear infinite;
        text-align: center;
        border-radius: 5px;
    }
    .gatilho-aviso {
        background-color: #CC7A00 !important;
        color: white !important;
        font-weight: bold !important;
        text-align: center;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# CABEÇALHO
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-silver">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        agora_utc = datetime.utcnow().strftime('%H:%M:%S')
        
        col1, col2, col3 = st.columns(3)
        col1.metric("BTC", "$ 93,450.20", "+2.1%")
        col2.metric("VOLATILIDADE", "8.4%", "ALTA")
        col3.metric("ALERTAS", "SINAL ATIVO", "EXAUSTÃO")

        st.markdown("<hr style='border: 1px solid #222'>", unsafe_allow_html=True)
        
        # TABELA FOCO TOTAL: PREÇO, ALVOS E SINAIS
        dados = {
            "ATIVO": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "PEPE/USDT", "LINK/USDT"],
            "PREÇO ATUAL": ["93.450", "3.845", "245.80", "0.000022", "14.25"],
            "ALVO MÍNIMO (COMPRA)": ["82.080", "3.429", "208.89", "0.000018", "13.32"],
            "ALVO MÁXIMO (VENDA)": ["100.320", "4.191", "255.31", "0.000024", "16.28"],
            "SINAL DE ALERTA": ["ESTÁVEL", "PREÇO JUSTO", "GATILHO (4%)", "EXAUSTÃO (10%)", "PREÇO JUSTO"]
        }
        
        # Para simular o "piscar" na tabela, usamos HTML dentro do dataframe
        def formatar_sinal(sinal):
            if "EXAUSTÃO" in sinal:
                return f'<div class="blink-exaustao">{sinal}</div>'
            elif "GATILHO" in sinal:
                return f'<div class="gatilho-aviso">{sinal}</div>'
            return sinal

        df = pd.DataFrame(dados)
        df_html = df.to_html(escape=False, index=False)
        df_html = df_html.replace('<table>', '<table style="width:100%; color:white; background-color:black; border-collapse: collapse;">')
        
        # Estilização da tabela via HTML para permitir o sinal piscante
        st.write("### 🦈 RADAR DE EXECUÇÃO")
        st.markdown(
            df.style.apply(lambda x: ["background-color: black" for i in x], axis=1).to_html(), 
            unsafe_allow_html=True
        )
        
        # Versão simplificada para garantir o sinal chamativo
        for i, row in df.iterrows():
            col_a, col_b, col_c, col_d, col_e = st.columns([1, 1, 1.2, 1.2, 1.5])
            col_a.write(f"**{row['ATIVO']}**")
            col_b.write(f"**{row['PREÇO ATUAL']}**")
            col_c.write(f"<span style='color:#00FF00'>{row['ALVO MÍNIMO (COMPRA)']}</span>", unsafe_allow_html=True)
            col_d.write(f"<span style='color:#FF4B4B'>{row['ALVO MÁXIMO (VENDA)']}</span>", unsafe_allow_html=True)
            
            if "EXAUSTÃO" in row['SINAL DE ALERTA']:
                col_e.markdown(f'<div class="blink-exaustao">{row["SINAL DE ALERTA"]}</div>', unsafe_allow_html=True)
            elif "GATILHO" in row['SINAL DE ALERTA']:
                col_e.markdown(f'<div class="gatilho-aviso">{row["SINAL DE ALERTA"]}</div>', unsafe_allow_html=True)
            else:
                col_e.write(row['SINAL DE ALERTA'])

        st.caption(f"Atualização Instantânea UTC: {agora_utc} | Alvos baseados na Wap do dia.")
        
    time.sleep(0.5)
