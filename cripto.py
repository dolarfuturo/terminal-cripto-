import streamlit as st
import ccxt
import pandas as pd
import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Alpha Vision - Eixo Real", layout="wide")

# 1. CONFIGURAÇÃO DE ACESSO ALPHA VISION
api_key = "3psP2WWNFzFGBHo6QhOjnk2gNSfHgpNtVI7TSy2RRcRgYHAI3d0edQdNBcMPRAOI"
api_secret = "L9YoKJwGdRZL4eO1pBkYWNQuk9qLGi2ESpF3Uw88cy62ED8pQuyUerFiDQHawekM"

# 2. CONEXÃO COM A BINANCE
# Adicionado ajuste de tempo para evitar erros de sincronização
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'spot',
        'adjustForTimeDifference': True
    }
})

# TENTATIVA DE CONTORNAR O ERRO 451 (BLOQUEIO REGIONAL)
# Forçamos a conexão através do endpoint alternativo da Binance
exchange.urls['api']['public'] = 'https://api1.binance.com/api/v3'
exchange.urls['api']['private'] = 'https://api1.binance.com/api/v3'

st.title("🚀 Terminal Alpha Vision - Eixo Real")

# 3. TESTE DE CONEXÃO E EXIBIÇÃO DE SALDO
try:
    # Controle do Reset das 00:00 UTC conforme solicitado
    agora_utc = datetime.datetime.now(datetime.timezone.utc)
    st.info(f"Horário Atual (UTC): {agora_utc.strftime('%H:%M:%S')} - Reset VWAP às 00:00")
    
    # Busca o saldo da conta
    balance = exchange.fetch_balance()
    usdt_total = balance['total'].get('USDT', 0)
    
    st.success("✅ Conectado à Binance! Eixo Real Operacional.")
    st.metric(label="Saldo disponível em USDT", value=f"{usdt_total:,.2f}")

except Exception as e:
    st.error(f"Erro na conexão: {e}")
    if "451" in str(e):
        st.warning("⚠️ O servidor do Streamlit (EUA) ainda está sendo bloqueado pela Binance. Tente recarregar a página.")

# O sistema resetará o VWAP automaticamente às 00:00 UTC.
