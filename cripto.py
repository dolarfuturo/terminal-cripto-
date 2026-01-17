import ccxt
import time
import os

# Configuração da Visão de Tubarão
exchange = ccxt.binance()
moedas = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'PEPE/USDT']

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def calcular_alpha_vision():
    while True:
        limpar_tela()
        print(f"{'='*50}")
        print(f"       ALPHA VISION CRYPTO - VISÃO DE TUBARÃO")
        print(f"           Atualização Automática (Real-time)")
        print(f"{'='*50}\n")
        print(f"{'ATIVO':<10} | {'PREÇO':<10} | {'DESVIO %':<10} | {'SINAL ALPHA'}")
        print("-" * 60)

        for simbolo in moedas:
            try:
                # 1. Puxa os dados da corretora
                ticker = exchange.fetch_ticker(simbolo)
                preco_atual = ticker['last']
                
                # 2. Simulação da VWAP (Em um sistema real, puxamos o histórico OHLCV)
                # Para o exemplo, vamos usar o preço de abertura como âncora
                preco_abertura = ticker['open']
                desvio = ((preco_atual / preco_abertura) - 1) * 100

                # 3. Lógica dos Alertas do Mister
                if abs(desvio) >= 10.0:
                    sinal = "!! EXAUSTÃO (BATER) !!"
                elif abs(desvio) >= 4.0:
                    sinal = "!! GATILHO (ALERTA) !!"
                else:
                    sinal = "Preço Justo"

                print(f"{simbolo:<10} | {preco_atual:<10.2f} | {desvio:>8.2f}% | {sinal}")

            except Exception as e:
                print(f"Erro ao ler {simbolo}: {e}")

        print(f"\n{'='*50}")
        print("Buscando próxima atualização em 5 segundos...")
        time.sleep(5) # Atualiza sozinho a cada 5 segundos

# Iniciar o Terminal
if __name__ == "__main__":
    calcular_alpha_vision()
