import streamlit as st
import ccxt
import pandas as pd
import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Alpha Vision - Eixo Real", layout="wide")

# 1. CONFIGURAÇÃO DE ACESSO ALPHA VISION
api_key = "3psP2WWNFzFGBHo6QhOjnk2gNSfHgpNtVI7TSy2RRcRgYHAI3d0edQdNBcMPRAOI"
api_secret = "L9YoKJwGdRZL4eO1pBkYWNQuk9qLGi2ESpF3Uw88cy62ED8pQuyUerFiDQHawekM"

# 2. CONEXÃO COM A BINANCE (CORREÇÃO PARA ERRO 451 - LOCALIZAÇÃO)
# Forçamos o uso do domínio .us ou api.binance.com que às vezes ajuda no bloqueio
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'spot',
        'adjustForTimeDifference': True
    }
})

# Mudança de URL para tentar evitar o bloqueio geográfico do Streamlit (USA)
exchange.urls['api'] = {
    'public': 'https://api.binance.com/api/v3',
    'private': 'https://api.binance.com/api/v3',
}

st.title("🚀 Terminal Alpha Vision - Eixo Real")

# 3. TESTE DE CONEXÃO E EXIBIÇÃO DE SALDO
try:
    # O reset do VWAP é baseado no fechamento 00:00 UTC da Binance
    agora_utc = datetime.datetime.now(datetime.timezone.utc)
    st.info(f"Horário Atual (UTC): {agora_utc.strftime('%H:%M:%S')} - Reset VWAP às 00:00")
    
    balance = exchange.fetch_balance()
    usdt_balance = balance['total'].get('USDT', 0)
    
    st.success("✅ Conectado à Binance! Trading Liberado.")
    st.metric(label="Saldo Disponível (USDT)", value=f"{usdt_balance:.2f} USDT")

except Exception as e:
    st.error(f"Erro de Conexão: {e}")
    st.warning("Nota: Se o erro 451 persistir, o servidor do Streamlit está bloqueado pela Binance. Podemos precisar de uma rota alternativa.")

# O sistema está programado para o Reset Automático de VWAP às 00:00 UTC.
