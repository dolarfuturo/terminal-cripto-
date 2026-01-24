import pandas as pd
from datetime import time

def calcular_eixo_institucional(df):
    """
    df deve conter colunas: ['timestamp', 'high', 'low', 'close']
    Horário de Brasília (UTC-3)
    """
    # 1. Definir a janela de captura (11:30 às 18:00)
    start_time = time(11, 30)
    end_time = time(18, 0)

    # Filtrar dados do dia dentro da janela americana
    session_data = df[(df['timestamp'].dt.time >= start_time) & 
                      (df['timestamp'].dt.time < end_time)]

    if not session_data.empty:
        # 2. Capturar Extremos e calcular a Média (Eixo)
        max_ny = session_data['high'].max()
        min_ny = session_data['low'].min()
        eixo_travado = (max_ny + min_ny) / 2

        # 3. Gerar a Grade de Alvos para os Clientes
        alvos = {
            "Eixo Mestre": eixo_travado,
            "Pullback (0.40%)": {
                "Long": eixo_travado * 0.996,
                "Short": eixo_travado * 1.004
            },
            "Parcial (0.61%)": {
                "Long": eixo_travado * 1.0061,
                "Short": eixo_travado * 0.9939
            },
            "Alerta de Topo (0.80%)": {
                "Long": eixo_travado * 1.008,
                "Short": eixo_travado * 0.992
            },
            "Alvo Final (1.22%)": {
                "Long": eixo_travado * 1.0122,
                "Short": eixo_travado * 0.9878
            }
        }
        return alvos
