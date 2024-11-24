import os
import subprocess
import matplotlib.pyplot as plt

def tempo_medio(resultados):
    if len(resultados) == 0:
        return 0
    soma = sum(resultados)
    return soma / len(resultados)

def salvar_resultados_em_arquivo(valores_T, resultados, tempo_medio, nome_arquivo):
    with open(nome_arquivo, "w") as arquivo:
        for T, tempo in zip(valores_T, resultados):
            arquivo.write(f"{tempo:.6f}\n")
        arquivo.write("\n")
        arquivo.write(f"{tempo_medio:.6f}")
    print(f"Resultados salvos no arquivo: {nome_arquivo}")


inicio_T = 0
fim_T = 800
passo_T = 400

valores_T = list(range(inicio_T, fim_T + 1, passo_T))

arquivo_c = "paralelo.c"
executavel = "paralelo.exe"

print("Compilando o programa...")
subprocess.run(["gcc", "-fopenmp", arquivo_c, "-o", executavel], check=True)

quant_threads = [2, 4, 8, 16]

for threads in quant_threads:
    resultados = []
    saida_diretorio = f"saida_pararelo{threads}"
    os.makedirs(saida_diretorio, exist_ok=True)
    for T in valores_T:
        print(f"Executando o programa com T={T} e Threads={threads}...")
        resultado = subprocess.run([f"./{executavel}", str(T), str(quant_threads)], capture_output=True, text=True)

        if resultado.returncode != 0:
            print(f"Erro ao executar o programa com T={T} e Threads={threads}: {resultado.stderr}")
        else:
            try:
                tempo_execucao = float(resultado.stdout.strip())
                resultados.append(tempo_execucao)
                print(f"Execução concluída para T={T} e Threads={threads}. Tempo: {tempo_execucao} segundos")
            except ValueError:
                print(f"Erro ao interpretar o tempo para T={T} e Threads={threads}: {resultado.stdout.strip()}")

    
    t_medio = tempo_medio(resultados)
    print(f"Tempo médio: {t_medio}")

    plt.plot(valores_T, resultados, marker='o')
    plt.title(f"Análise de Tempo de Execução para {threads} threads")
    plt.xlabel("Número de interações")
    plt.ylabel("Tempo de Execução (segundos)")
    plt.grid(True)
    plt.savefig(f"analise_tempo_paralelo{threads}.png")
    # plt.show()
    salvar_resultados_em_arquivo(valores_T, resultados, t_medio, f"tempos_execucao_pararelo{threads}.txt")

    print("\n\n")

print("Todas as execuções foram concluídas.")
