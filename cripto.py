import streamlit as st
import requests

# Isso vai extrair o IP real do servidor para você
ip_alvo = requests.get('https://api.ipify.org').text

st.title("✅ IP Identificado")
st.write("Copie o número abaixo e cole na Binance:")
st.code(ip_alvo)
