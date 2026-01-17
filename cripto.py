import streamlit as st
import ccxt
import pandas as pd
import time

# Configuração da Página
st.set_page_config(page_title="Alpha Vision Crypto", layout="wide")

# Estilização CSS para visual "Premium"
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .title-main { color: #00ffcc; font-size: 40px; font-weight: bold; margin-bottom: 0px; }
    .subtitle { color: #808495; font-size: 20px; font-style: italic; margin-top: -10px; margin-bottom: 30px; }
    .stMetric { background-color: #1a1c24; border-radius: 10px; padding: 15px; border: 1px solid #2d2e35; }
    </style>
    """, unsafe_allow_html=True)

# Identidade Visual no Topo
st.markdown('<p class="title-main">ALPHA VISION CRYPTO</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Visão de Tubarão</p>', unsafe_allow_html=True)

# Função para buscar dados com Tratamento de Erro (Anti-Erro Vermelho)
def buscar_dados():
    try:
        exchange = ccxt.binance()
        # Lista das moedas que você quer monitorar
        simbolos = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'ADA/USDT']
        tickers = exchange.fetch_tickers(simbolos)
        
        dados_limpos = []
        for simbolo in simbolos:
            if simbolo in tickers:
                t = tickers[simbolo]
                dados_limpos.append({
                    'Ativo': simbolo.split('/')[0],
                    'Preço': t['last'],
                    'Variação %': t['percentage'],
                    'Volume': t['baseVolume']
                })
        return dados_limpos
    except Exception as e:
        return None # Retorna nada se houver falha na conexão

# Lógica de Exibição
dados = buscar_dados()

if dados:
    # Cria as colunas de destaque (KPIs)
    cols = st.columns(len(dados))
    for idx, item in enumerate(dados):
        cor_delta = "normal" if item['Variação %'] >= 0 else "inverse"
        cols[idx].metric(
            label=f" {item['Ativo']}", 
            value=f"$ {item['Preço']:,}", 
            delta=f"{item['Variação %']:.2f}%",
            delta_color=cor_delta
        )
    
    st.write("---")
    st.subheader("📊 Monitor de Fluxo e Exaustão")
    df = pd.DataFrame(dados)
    st.dataframe(df, use_container_width=True)
    
    if st.button('🔄 Sincronizar Agora'):
        st.rerun()
else:
    # Mensagem elegante em vez do erro vermelho
    st.warning("⚠️ Sincronizando com a Exchange... Por favor, aguarde 5 segundos ou clique no botão abaixo.")
    if st.button('Tentar Novamente'):
        st.rerun()

st.sidebar.info("Acesso Restrito: Alpha Vision Crypto v1.0")
