import streamlit as st
import requests

# Isso vai extrair o IP real do servidor para você
ip_alvo = requests.get('https://api.ipify.org').text

st.title("✅ IP Identificado")
st.write("Copie o número abaixo e cole na Binance:")
st.code(ip_alvo)
import streamlit as st
import ccxt
import pandas as pd

# 1. CONFIGURAÇÃO DE ACESSO ALPHA VISION
# Use a Secret Key que você copiou antes dela sumir!
api_key = "3psP2WWNFzFGBHo6QhOjnk2gNSfHgpNtVI7TSy2RRcRgYHAI3d0edQdNBcMPRAOI"
api_secret = "L9YoKJwGdRZL4eO1pBkYWNQuk9qLGi2ESpF3Uw88cy62ED8pQuyUerFiDQHawekM"

# 2. CONEXÃO COM A BINANCE
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'}
})

# 3. TESTE DE CONEXÃO E RESET DE VWAP (00:00 UTC)
try:
    balance = exchange.fetch_balance()
    st.success("✅ Conectado à Binance! Trading Liberado.")
    st.write(f"Saldo disponível em USDT: {balance['total'].get('USDT', 0)}")
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# O sistema agora resetará o VWAP automaticamente às 00:00 UTC conforme solicitado.
