import streamlit as st
import pandas as pd
import time

# Configuração de Página para Modo Dark Total
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# CSS PARA FUNDO PRETO E CORES PERSONALIZADAS
st.markdown("""
    <style>
    /* Fundo Totalmente Preto */
    .stApp { background-color: #000000; }
    
    /* Título e Subtítulo */
    .title-gold { color: #D4AF37; font-size: 52px; font-weight: bold; text-align: center; margin-bottom: 0px; }
    .subtitle-silver { color: #C0C0C0; font-size: 24px; text-align: center; margin-top: -10px; font-style: italic; letter-spacing: 2px; }

    /* Ajuste dos Blocos de Métricas */
    [data-testid="stMetricLabel"] p { 
        color: #FFFFFF !important; 
        font-weight: bold !important; 
        font-size: 20px !important; 
    }
    [data-testid="stMetricValue"] { 
        color: #FFA500 !important; /* PREÇOS EM LARANJA */
        font-weight: bold !important;
    }
    div[data-testid="stMetric"] {
        background-color: #000000 !important;
        border: 2px solid #333333;
        border-radius: 10px;
        padding: 15px;
    }

    /* Tabela com fundo preto */
    .stDataFrame, div[data-testid="stTable"] {
        background-color: #000000 !important;
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
        # Blocos Superiores com as cores solicitadas
        col1, col2, col3 = st.columns(3)
        col1.metric("BTC", "$ 93,450", "+2.15%")
        col2.metric("VOLATILIDADE", "8.4%", "ALTA")
        col3.metric("ALERTAS", "3 SINAIS", "ATIVOS")

        st.markdown("<hr style='border: 1px solid #333'>", unsafe_allow_html=True)
        
        # Dados da Tabela
        dados = {
            "ATIVO": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "PEPE/USDT", "LINK/USDT"],
            "PREÇO": ["93.450", "3.845", "245.80", "0.000022", "14.25"],
            "MÁX/MIN DIA": ["94k / 91k", "3.9k / 3.7k", "248 / 220", "0.25 / 0.18", "15 / 13"],
            "VARIAÇÃO": ["+2.1%", "+0.5%", "+4.2%", "+10.6%", "-4.1%"],
            "SINAL ALPHA": ["ESTÁVEL", "PREÇO JUSTO", "GATILHO VENDA", "EXAUSTÃO (BATER)", "GATILHO COMPRA"]
        }
        df = pd.DataFrame(dados)

        # Estilização dos Sinais
        def style_rows(val):
            if 'EXAUSTÃO' in val: return 'color: #FF0000; font-weight: bold;'
            if 'GATILHO VENDA' in val: return 'color: #FFA500; font-weight: bold;'
            if 'GATILHO COMPRA' in val: return 'color: #00FF00; font-weight: bold;'
            return 'color: #FFFFFF;'

        st.write("### 🦈 RADAR DE EXECUÇÃO")
        st.dataframe(
            df.style.map(style_rows, subset=['SINAL ALPHA']),
            use_container_width=True,
            hide_index=True
        )

        st.caption("Sincronizado com a rede de dados Alpha Vision.")
        
    time.sleep(1)
