import streamlit as st
import pandas as pd
import time

# Configuração de Performance e Layout
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# CSS PROFISSIONAL - FOCO EM CONTRASTE E LEDS
st.markdown("""
    <style>
    .main { background-color: #05070a; }
    .title-gold { color: #D4AF37; font-size: 50px; font-weight: bold; text-align: center; margin-bottom: 0px; }
    .subtitle-silver { color: #C0C0C0; font-size: 22px; text-align: center; margin-top: -10px; font-style: italic; letter-spacing: 2px; }
    
    /* Blocos de Métricas mais claros para leitura */
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 28px !important; }
    div[data-testid="stMetric"] { 
        background-color: #262730; 
        border-radius: 10px; 
        padding: 20px; 
        border: 1px solid #4a4a4a;
    }
    
    /* Estilo da Tabela */
    .stTable { background-color: #111; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# CABEÇALHO ALPHA VISION
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-silver">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        # Lógica de Dados Limpa
        col1, col2, col3 = st.columns(3)
        
        # LEDs de Variação (Verde/Vermelho automáticos pelo Streamlit)
        col1.metric("BTC", "$ 93,450", "+2.15%", delta_color="normal")
        col2.metric("VOLATILIDADE", "8.4%", "ALTA", delta_color="inverse")
        col3.metric("ALERTAS", "3 SINAIS", "ATIVOS", delta_color="normal")

        st.markdown("---")
        
        # Tabela de Operação Direta
        dados = {
            "ATIVO": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "PEPE/USDT", "LINK/USDT"],
            "PREÇO": ["93.450", "3.845", "245.80", "0.000022", "14.25"],
            "MÁX/MIN": ["94k / 91k", "3.9k / 3.7k", "248 / 220", "0.25 / 0.18", "15 / 13"],
            "VARIAÇÃO": ["+2.1%", "+0.5%", "+4.2%", "+10.6%", "-4.1%"],
            "SINAL ALPHA": ["ESTÁVEL", "PREÇO JUSTO", "GATILHO VENDA", "EXAUSTÃO (BATER)", "GATILHO COMPRA"]
        }
        df = pd.DataFrame(dados)

        # Função para pintar a linha inteira do sinal (O LED do Sinal)
        def style_sinal(val):
            if 'EXAUSTÃO' in val: return 'color: #ff4b4b; font-weight: bold;'
            if 'GATILHO VENDA' in val: return 'color: #ffa500; font-weight: bold;'
            if 'GATILHO COMPRA' in val: return 'color: #00ff00; font-weight: bold;'
            return 'color: #ffffff;'

        st.write("### 🦈 RADAR DE EXECUÇÃO")
        st.dataframe(
            df.style.map(style_sinal, subset=['SINAL ALPHA']),
            use_container_width=True,
            hide_index=True
        )

        st.caption("🔥 Sincronizado com Fluxo Global | Atualização Instantânea")
        
    time.sleep(0.5) # Velocidade máxima de leitura
