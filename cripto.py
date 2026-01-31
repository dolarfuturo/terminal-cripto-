import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. CONFIGURAÇÃO ALPHA
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-gold { color: #D4AF37; font-size: 30px; font-weight: 900; text-align: center; padding: 10px; }
    .header-container { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background: #080808; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 15px 0; border-bottom: 1px solid #151515; }
    .h-col, .w-col { flex: 1; text-align: center; color: #FFF; font-family: 'monospace'; }
    .h-col { font-size: 10px; text-transform: uppercase; font-weight: 800; }
    .w-col { font-size: 20px; font-weight: 800; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 12px; border-top: 1px solid #333; display: flex; justify-content: space-around; z-index: 1000; }
    .dot { height: 8px; width: 8px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 5px
