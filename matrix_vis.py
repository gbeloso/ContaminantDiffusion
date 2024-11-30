import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração de diretórios
diretorio_paralelo = "saida_paralelo{}"
diretorio_sequencial = "saida_sequencial"

iteracoes_diferentes = {}

# Iterar sobre diferentes configurações de threads
for threads in [2, 4, 8, 16]:
    iteracoes_diferentes[threads] = []
    for i in range(0, 501, 10):
        try:
            # Ajustando os caminhos
            arquivo_paralelo = f"{diretorio_paralelo.format(threads)}/{i}.csv"
            arquivo_sequencial = f"{diretorio_sequencial}/{i}.csv"

            # Lendo os arquivos
            paralelo = pd.read_csv(arquivo_paralelo, header=None)
            sequencial = pd.read_csv(arquivo_sequencial, header=None)

            # Comparando os resultados
            if not paralelo.equals(sequencial):
                iteracoes_diferentes[threads].append(i)

        except FileNotFoundError as e:
            print(f"Arquivo não encontrado: {e}")

# Exibindo diferenças para cada configuração de threads
for threads, iteracoes in iteracoes_diferentes.items():
    if len(iteracoes) > 0:
        print(f"Diferença nas iterações para {threads} threads: ")
        print(", ".join(map(str, iteracoes)))
    else:
        print(f"O sequencial e o paralelo ({threads} threads) deram o mesmo resultado para todas as iterações.")

# Gerando visualizações para resultados paralelos
for threads in [2, 4, 8, 16]:
    diretorio_atual = diretorio_paralelo.format(threads)
    os.makedirs(f"{diretorio_atual}/images", exist_ok=True)  # Criar pasta para imagens
    for i in range(0, 501, 10):
        try:
            arquivo = f"{diretorio_atual}/{i}.csv"
            image = f"{diretorio_atual}/images/{i}.png"

            # Gerando mapa de calor
            df = pd.read_csv(arquivo, header=None)
            fig, ax = plt.subplots(figsize=(6, 6))
            sns.heatmap(df, ax=ax, cbar=False, cmap="coolwarm")
            ax.set_axis_off()
            plt.savefig(image, dpi=300, bbox_inches="tight")
            plt.close()
            del df
        except FileNotFoundError as e:
            print(f"Arquivo não encontrado para threads={threads}, iteração={i}: {e}")

# Gerando visualizações para resultados sequenciais
os.makedirs(f"{diretorio_sequencial}/images", exist_ok=True)
for i in range(0, 501, 10):
    try:
        arquivo = f"{diretorio_sequencial}/{i}.csv"
        image = f"{diretorio_sequencial}/images/{i}.png"

        # Gerando mapa de calor
        df = pd.read_csv(arquivo, header=None)
        fig, ax = plt.subplots(figsize=(6, 6))
        sns.heatmap(df, ax=ax, cbar=False, cmap="coolwarm")
        ax.set_axis_off()
        plt.savefig(image, dpi=300, bbox_inches="tight")
        plt.close()
        del df
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado para iteração={i}: {e}")
