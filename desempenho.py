import os
import matplotlib.pyplot as plt

num_threads = [1, 2, 4, 8, 16]
media_valores = []

# Iterar sobre os números de threads
for i in num_threads:
    try:
        if i == 1:
            # Leitura do arquivo sequencial
            caminho_arquivo = "./tempos_execucao_sequencial.txt"
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "r") as arquivo:
                    linhas = arquivo.readlines()
                    # A última linha contém a média
                    media_valores.append(float(linhas[-1].strip()))
            else:
                print(f"Arquivo {caminho_arquivo} não encontrado.")
                media_valores.append(None)
        else:
            # Leitura dos arquivos paralelos
            caminho_arquivo = f"./tempos_execucao_paralelo{i}.txt"
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "r") as arquivo:
                    linhas = arquivo.readlines()
                    # A última linha contém a média
                    media_valores.append(float(linhas[-1].strip()))
            else:
                print(f"Arquivo {caminho_arquivo} não encontrado.")
                media_valores.append(None)
    except Exception as e:
        print(f"Erro ao processar o arquivo para {i} threads: {e}")
        media_valores.append(None)

# Remover valores nulos
num_threads_validos = [n for n, m in zip(num_threads, media_valores) if m is not None]
media_valores_validos = [m for m in media_valores if m is not None]

# Calcular Speedup
if len(media_valores_validos) > 0:
    T1 = media_valores_validos[0]
    speedup = [T1 / t for t in media_valores_validos]

    # Plotar Speedup
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(num_threads_validos, speedup, marker='o', label='Speedup Real')
    plt.plot(num_threads_validos, num_threads_validos, linestyle='--', color='red', label='Speedup Linear (Ideal)')
    for i, txt in enumerate(speedup):
        plt.text(num_threads_validos[i], speedup[i], f"{txt:.2f}", ha='center', va='bottom')
    plt.xlabel('Número de Threads')
    plt.ylabel('Speedup')
    plt.title('Gráfico de Speedup')
    plt.legend()
    plt.grid(True)
    plt.savefig("speedup.png")

    # Calcular Eficiência
    efficiency = [s / t for s, t in zip(speedup, num_threads_validos)]

    # Plotar Eficiência
    plt.subplot(1, 2, 2)
    plt.plot(num_threads_validos, efficiency, marker='o', label='Eficiência Real')
    plt.plot(num_threads_validos, [1] * len(num_threads_validos), linestyle='--', color='red', label='Eficiência Linear')
    for i, txt in enumerate(efficiency):
        plt.text(num_threads_validos[i], efficiency[i], f"{txt:.2f}", ha='center', va='bottom')
    plt.xlabel('Número de Threads')
    plt.ylabel('Eficiência')
    plt.title('Gráfico de Eficiência')
    plt.legend()
    plt.grid(True)
    plt.savefig("eficiencia.png")

    # Exibir os gráficos
    plt.show()
else:
    print("Nenhum dado válido encontrado para gerar gráficos.")
