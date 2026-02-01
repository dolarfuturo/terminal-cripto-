import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - AJUSTE DE ESCALA PARA CABER AMBOS
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .stApp { background-color: #000000; }
    
    .title-container { text-align: center; padding-bottom: 20px; }
    .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; letter-spacing: 2px; }
    .subtitle-white { color: #FFFFFF; font-size: 16px; font-weight: 300; letter-spacing: 5.5px; text-transform: lowercase; margin-top: -10px; }
    
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    
    .row-container { display: flex; width: 100%; align-items: center; padding: 25px 0 10px 0; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; white-space: nowrap; }
    
    /* BLOCO DE VISÃO CENTRALIZADO IGUAL À FOTO */
    .vision-block { display:
