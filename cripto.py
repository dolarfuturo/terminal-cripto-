import streamlit as st
import requests

st.title("Configurador de Eixo Real")
try:
    ip = requests.get('https://api.ipify.org').text
    st.success(f"O IP do seu servidor é: {ip}")
    st.info("Copie o número acima e cole na Binance no campo 'IPs Confiáveis'.")
except:
    st.error("Erro ao identificar IP. Verifique sua conexão.")
