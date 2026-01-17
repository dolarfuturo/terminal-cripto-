import streamlit as st
import pandas as pd
import time
from datetime import datetime

# CONFIGURAÇÃO DE INTERFACE DE ELITE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# CSS PARA MANTER O LAYOUT (Fundo Preto, Letras Brancas, Preços Laranja)
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 48px; font-weight: bold; text-align: center; margin-bottom: 0px; }
    .subtitle-silver { color: #C0C0C0; font-size: 20px; text-align: center; margin-top: -10px; font-style: italic; letter-spacing: 3px; }
    
    /* Blocos Superiores */
    [data-testid="stMetricLabel"] p { color: #FFFFFF !important; font-weight: bold !important; font-size: 22px !important; }
    [data-testid="stMetricValue"] { color: #FFA500 !important; font-weight: bold !important; }
    div[data-testid="stMetric"] { 
        background-color: #000000 !important; 
        border: 1px solid #333333; 
        border-radius: 10px; 
        padding: 15px; 
    }
    
    /* Tabela All Black */
    .stDataFrame { background-color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# CABEÇALHO FIXO
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-silver">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

placeholder = st.empty()

# MOCK DE DADOS (Simulando a Conexão que faremos com a API)
while True:
    with placeholder.container():
        # Lógica Automática de Tempo
        agora_utc = datetime.utcnow().strftime('%H:%M:%S')
        
        col1, col2, col3 = st.columns(3)
        # Preços em Laranja, Nomes em Branco (via CSS acima)
        col1.metric("BTC", "$ 93,450.20", "+2.1%")
        col2.metric("VOLATILIDADE", "8.4%", "ALTA")
        col3.metric("ALERTAS", "3 SINAIS", "ATIVOS")

        st.markdown("<hr style='border: 0.5px solid #222'>", unsafe_allow_html=True)
        
        # TABELA DE EXECUÇÃO - LÓGICA WAP 00:00 UTC
        # Os valores de MÁX/MIN aqui são projetados (Wap + 10%)
        dados = {
            "ATIVO": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "PEPE/USDT", "LINK/USDT"],
            "PREÇO": ["93.450", "3.845", "245.80", "0.000022", "14.25"],
            "WAP ATUAL": ["91.200", "3.810", "232.10", "0.000020", "14.80"],
            "MÁX PROJETADA": ["100.320", "4.191", "255.31", "0.000024", "16.28"],
            "SINAL ALPHA": ["ESTÁVEL", "PREÇO JUSTO", "GATILHO VENDA", "EXAUSTÃO (BATER)", "GATILHO COMPRA"]
        }
        df = pd.DataFrame(dados)

        def color_sinal(val):
            if 'EXAUSTÃO' in val: return 'color: #FF0000; font-weight: bold;'
            if 'GATILHO VENDA' in val: return 'color: #FFA500; font-weight: bold;'
            if 'GATILHO COMPRA' in val: return 'color: #00FF00; font-weight: bold;'
            return 'color: #FFFFFF;'

        st.write(f"### 🦈 RADAR DE EXAUSTÃO (Sincronizado UTC: {agora_utc})")
        st.dataframe(
            df.style.map(color_sinal, subset=['SINAL ALPHA']),
            use_container_width=True,
            hide_index=True
        )

        st.caption("A Wap reseta automaticamente às 00:00 UTC. Monitorando estiramento de 4% e 10%.")
        
    time.sleep(1) # Atualização automática
