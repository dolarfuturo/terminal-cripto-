import streamlit as st
import yfinance as yf
import time

# Configuração de Estilo "Visão de Tubarão"
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stApp { background-color: #000000; }
    .title { color: #D4AF37; text-align: center; font-family: 'serif'; font-weight: bold; margin-bottom: 0px; }
    .subtitle { color: #FFFFFF; text-align: center; letter-spacing: 5px; font-size: 12px; margin-bottom: 30px; }
    
    table { width: 100%; border-collapse: collapse; color: white; background-color: #000; }
    th { color: #D4AF37 !important; background-color: #111 !important; padding: 10px; border: 1px solid #333; font-size: 12px; text-align: center; }
    td { padding: 12px; border: 1px solid #222; text-align: center; font-family: 'monospace'; font-size: 14px; }
    
    .up { color: #00ff00; font-weight: bold; }
    .down { color: #ff0000; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho Dourado
st.markdown("<h1 class='title'>ALPHA VISION CRYPTO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>VISÃO DE TUBARÃO</p>", unsafe_allow_html=True)

# Lista de Ativos e Eixo Mestre (Imagem 1000027192)
ativos = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "DOGE-USD", "ADA-USD"]
EIXO_BTC = 89795.0

def get_table_data():
    rows = ""
    for ticker in ativos:
        try:
            # Puxa preço real do Yahoo Finance
            data = yf.Ticker(ticker).fast_info
            price = data['last_price']
            change = ((price / data['previous_close']) - 1) * 100
            
            color = "up" if change >= 0 else "down"
            arrow = "▲" if change >= 0 else "▼"
            
            # Referência para cálculo (Eixo para BTC, Preço para os outros)
            ref = EIXO_BTC if ticker == "BTC-USD" else price
            def val(p): return f"{ref * (1 + (p/100)):,.2f}"

            rows += f"""
            <tr>
                <td style='color:#D4AF37; font-weight:bold;'>{ticker.replace("-USD", "/USDT")}</td>
                <td class='{color}'>{price:,.2f}<br><small>{arrow} {change:.2f}%</small></td>
                <td>{val(1.22)}</td>
                <td>{val(0.83)}</td>
                <td>{val(0.61)}</td>
                <td>{val(0.40)}</td>
                <td>{val(-0.40)}</td>
                <td>{val(-0.61)}</td>
                <td>{val(-0.83)}</td>
                <td>{val(-1.22)}</td>
            </tr>
            """
        except:
            continue
    return rows

# Construção da Tabela com os nomes da sua planilha
tabela_html = f"""
<table>
    <thead>
        <tr>
            <th>CÓDIGO</th>
            <th>PREÇO ATUAL</th>
            <th>EXAUSTÃO TOPO<br>(1.22%)</th>
            <th>PRÓX. TOPO<br>(0.83%)</th>
            <th>DECISÃO<br>(0.61%)</th>
            <th>RESPIRO<br>(0.40%)</th>
            <th>RESPIRO FUNDO<br>(-0.40%)</th>
            <th>DECISÃO FUNDO<br>(-0.61%)</th>
            <th>PRÓX. FUNDO<br>(-0.83%)</th>
            <th>EXAUSTÃO FUNDO<br>(-1.22%)</th>
        </tr>
    </thead>
    <tbody>
        {get_table_data()}
    </tbody>
</table>
"""

# O SEGREDO ESTÁ AQUI: Renderiza o HTML em vez de mostrar o texto
st.markdown(tabela_html, unsafe_allow_html=True)

# Rodapé com Horário de Brasília
st.markdown(f"<p style='color:#444; text-align:center; font-size:10px; margin-top:20px;'>Atualizado em: {time.strftime('%H:%M:%S')} | Reset 00:00 UTC</p>", unsafe_allow_html=True)

# Motor de atualização (A cada 5 segundos para não ser bloqueado)
time.sleep(5)
st.rerun()
