import streamlit as st
import ccxt
import pandas as pd

# 1. Configuração de Identidade
st.set_page_config(page_title="Alpha Vision Crypto", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 20px; }
    .title-main { color: #00ffcc; font-size: 35px; font-weight: bold; }
    .subtitle { color: #8b949e; font-size: 18px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title-main">ALPHA VISION CRYPTO</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Visão de Tubarão: Operacional Institucional</p>', unsafe_allow_html=True)

# 2. Motor de Cálculo (A Regra dos 100 períodos de 1h)
def buscar_oportunidades():
    try:
        exchange = ccxt.binance()
        moedas = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT']
        resultados = []
        
        for m in moedas:
            # Busca os 100 candles de 1h planejados
            bars = exchange.fetch_ohlcv(m, timeframe='1h', limit=100)
            df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
            
            # Cálculo da VWAP Institucional
            vwap = ( ((df['h'] + df['l'] + df['c']) / 3) * df['v']).sum() / df['v'].sum()
            preco_atual = df['c'].iloc[-1]
            desvio = ((preco_atual / vwap) - 1) * 100
            
            status = "⚖️ Neutro"
            if desvio > 1.5: status = "🔥 Exaustão Compra"
            elif desvio < -1.5: status = "❄️ Exaustão Venda"
            
            resultados.append({
                "Ativo": m.replace('/USDT', ''),
                "Preço": f"{preco_atual:,.2f}",
                "Alvo": f"{vwap:,.2f}",
                "Status": status
            })
        return resultados
    except Exception as e:
        return None

# 3. Exibição Direta dos Números
dados = buscar_oportunidades()

if dados:
    # Exibe os preços em colunas grandes (Cards)
    cols = st.columns(len(dados))
    for i, item in enumerate(dados):
        with cols[i]:
            st.metric(label=item['Ativo'], value=f"$ {item['Preço']}", delta=item['Status'], delta_color="off")
            st.write(f"🎯 **Alvo: {item['Alvo']}**")
    
    st.write("---")
    st.subheader("🚀 Scanner de Oportunidades")
    st.dataframe(pd.DataFrame(dados), use_container_width=True)
else:
    st.error("Erro ao conectar. Por favor, clique no botão abaixo para tentar novamente.")

if st.button('⚡ ATUALIZAR SCANNER'):
    st.rerun()

# Sidebar de Identidade
st.sidebar.markdown("### ALPHA VISION v1.0")
st.sidebar.info("Cálculos baseados em volume institucional (VWAP 100p).")
