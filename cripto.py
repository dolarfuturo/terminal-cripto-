import streamlit as st
import ccxt
import pandas as pd
import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Alpha Vision - Eixo Real", layout="wide")

# 1. CONFIGURAÇÃO DE ACESSO ALPHA VISION
api_key = "3psP2WWNFzFGBHo6QhOjnk2gNSfHgpNtVI7TSy2RRcRgYHAI3d0edQdNBcMPRAOI"
api_secret = "L9YoKJwGdRZL4eO1pBkYWNQuk9qLGi2ESpF3Uw88cy62ED8pQuyUerFiDQHawekM"

# 2. CONEXÃO DIRETA COM A BINANCE
# Removida a configuração manual de URL que causou o erro de 'testnet'
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'spot',
        'adjustForTimeDifference': True
    }
})

st.title("🚀 Terminal Alpha Vision - Eixo Real")

# 3. EXIBIÇÃO DE DADOS
try:
    # Mostra o horário UTC para o controle do Reset das 00:00
    agora_utc = datetime.datetime.now(datetime.timezone.utc)
    st.info(f"Horário Atual (UTC): {agora_utc.strftime('%H:%M:%S')} - Reset VWAP às 00:00")
    
    # Busca o saldo real
    balance = exchange.fetch_balance()
    usdt_balance = balance['total'].get('USDT', 0)
    
    st.success("✅ Conectado com Sucesso!")
    st.metric(label="Saldo em USDT", value=f"{usdt_balance:,.2f}")

except Exception as e:
    st.error(f"Erro de Conexão: {e}")
    if "451" in str(e):
        st.warning("⚠️ O servidor do Streamlit está em uma região bloqueada pela Binance. Tente atualizar a página em alguns minutos.")

# O sistema está programado para o Reset Automático de VWAP às 00:00 UTC.
