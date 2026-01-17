import streamlit as st
import ccxt
import pandas as pd
import time

# Configuração de Identidade Visual
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

def buscar_dados_vitoria():
    try:
        exchange = ccxt.binance()
        # Moedas principais para o operador
        moedas = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT']
        lista_final = []
        
        for m in moedas:
            # Cálculo de 100 períodos de 1h
            bars = exchange.fetch_ohlcv(m, timeframe='1h', limit=100)
            df = pd.DataFrame(bars, columns=['t', 'o', 'h', 'l', 'c', 'v'])
            
            # Matemática da VWAP
            vwap = ( ((df['h'] + df['l'] + df['c']) / 3) * df['v']).sum() / df['v'].sum()
            preco = df['c'].iloc[-1]
            desvio = ((preco / vwap) - 1) * 100
            
            status = "⚖️ Estável"
            if desvio > 1.5: status = "🔥 Venda (Exaustão)"
            elif desvio < -1.5: status = "❄️ Compra (Exaustão)"
            
            lista_final.append({
                "ATIVO": m.replace('/USDT', ''),
                "PREÇO ATUAL": f"$ {preco:,.2f}",
                "ALVO (VWAP)": f"$ {vwap:,.2f}",
                "STATUS": status
            })
        return lista_final
    except:
        return None

# Execução Direta
dados = buscar_dados_vitoria()

if dados:
    st.write("---")
    cols = st.columns(4)
    for i, item in enumerate(dados):
        with cols[i]:
            st.metric(label=item['ATIVO'], value=item['PREÇO ATUAL'], delta=item['STATUS'], delta_color="normal")
            st.caption(f"🎯 Alvo: {item['ALVO (VWAP)']}")
    
    st.write("---")
    st.subheader("🚀 Dados Prontos para Operação")
    st.table(pd.DataFrame(dados))
else:
    st.warning("Sincronizando com a Binance... Aguarde 5 segundos.")
    time.sleep(5)
    st.rerun()

if st.button('⚡ ATUALIZAR AGORA'):
    st.rerun()

st.sidebar.markdown("### ALPHA VISION v1.0")
st.sidebar.write("Visão Institucional Ativa.")
