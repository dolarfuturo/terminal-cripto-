import streamlit as st
import ccxt
import pandas as pd

# Configuração Visual Alpha Vision
st.set_page_config(page_title="Alpha Vision Crypto", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; }
    .title-main { color: #00ffcc; font-size: 42px; font-weight: bold; margin-bottom: 0px; }
    .subtitle { color: #8b949e; font-size: 18px; font-style: italic; margin-top: -10px; }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho Identidade
st.markdown('<p class="title-main">ALPHA VISION CRYPTO</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Visão de Tubarão: Operacional Institucional</p>', unsafe_allow_html=True)
st.write("---")

# Motor de Cálculo: VWAP Institucional
def motor_de_calculo(simbolo):
    try:
        exchange = ccxt.binance()
        # Busca 100 períodos de 1h conforme planejado
        bars = exchange.fetch_ohlcv(simbolo, timeframe='1h', limit=100)
        df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
        
        # Cálculo da Média Ponderada (VWAP)
        vwap_inst = ( ((df['h'] + df['l'] + df['c']) / 3) * df['v']).sum() / df['v'].sum()
        preco_atual = df['c'].iloc[-1]
        desvio = ((preco_atual / vwap_inst) - 1) * 100

        # Regra de Negócio para o Operador
        if desvio > 1.8:
            status, acao = "🔥 EXAUSTÃO COMPRA", "VENDER / SHORT"
        elif desvio < -1.8:
            status, acao = "❄️ EXAUSTÃO VENDA", "COMPRAR / LONG"
        else:
            status, acao = "⚖️ MERCADO NEUTRO", "AGUARDAR"

        return {
            "ATIVO": simbolo.split('/')[0],
            "PREÇO": round(preco_atual, 2),
            "ALVO (VWAP)": round(vwap_inst, 2),
            "STATUS": status,
            "AÇÃO": acao
        }
    except:
        return None

# Interface de Operação
moedas = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT']
resumos = []

cols = st.columns(4)
for i, m in enumerate(moedas):
    dado = motor_de_calculo(m)
    if dado:
        resumos.append(dado)
        with cols[i]:
            st.metric(dado['ATIVO'], f"$ {dado['PREÇO']:,}")
            st.write(f"**{dado['STATUS']}**")
            st.caption(f"🎯 Alvo: {dado['ALVO (VWAP)']}")

st.write("---")
st.subheader("🚀 Scanner de Oportunidades")
if resumos:
    st.table(pd.DataFrame(resumos))

# Botão de Comando do Operador
if st.button('⚡ ATUALIZAR SCANNER (VISÃO DE TUBARÃO)'):
    st.rerun()

st.sidebar.markdown("### ALPHA VISION v1.0")
st.sidebar.info("Cálculos baseados em volume institucional (VWAP 100p).")
