import ccxt
import time
from datetime import datetime

def rodar_alpha_vision_automatico():
    exchange = ccxt.binance()
    
    # 1. Reset Automático na Virada do Dia (UTC)
    dia_atual = datetime.utcnow().day
    
    while True:
        agora = datetime.utcnow()
        
        # Se mudou o dia, o sistema reseta a base da Wap
        if agora.day != dia_atual:
            print("--- VIRADA DE DIA DETECTADA: RESETANDO ALPHA VISION ---")
            dia_atual = agora.day
            # Aqui o código limpa os cálculos antigos e recomeça
        
        # 2. Busca Dados e Calcula os Desvios (4% e 10%)
        # [A lógica que construímos de fundo preto e alertas roda aqui]
        
        # 3. Velocidade Máxima
        time.sleep(0.5) 

# Este é o cérebro que nunca dorme.
