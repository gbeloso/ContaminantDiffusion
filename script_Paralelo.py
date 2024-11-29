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
fim_T = 500
passo_T = 100

valores_T = list(range(inicio_T, fim_T + 1, passo_T))

arquivo_c = "paralelo.c"
executavel = "paralelo.exe"

print("Compilando o programa paralelo...")
subprocess.run(["gcc", "-fopenmp", arquivo_c, "-o", executavel], check=True)

quant_threads = [2, 4, 8, 16]

# Para coletar dados para o gráfico combinado
todas_threads_resultados = {}

# Lendo os dados sequenciais previamente gerados
sequencial_resultados = []
sequencial_arquivo = "tempos_execucao_sequencial.txt"
if os.path.exists(sequencial_arquivo):
    with open(sequencial_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        sequencial_resultados = [float(linha.strip()) for linha in linhas[:-2]]  # Ignorar a média
    print("Dados do sequencial carregados com sucesso.")
else:
    print(f"Arquivo {sequencial_arquivo} não encontrado. O gráfico combinado será gerado sem os dados sequenciais.")

# Gerando gráficos para cada configuração de threads
for threads in quant_threads:
    resultados = []
    saida_diretorio = f"saida_pararelo{threads}"
    os.makedirs(saida_diretorio, exist_ok=True)
    for T in valores_T:
        print(f"Executando o programa com T={T} e Threads={threads}...")
        resultado = subprocess.run([f"./{executavel}", str(T), str(threads)], capture_output=True, text=True)

        if resultado.returncode != 0:
            print(f"Erro ao executar o programa com T={T} e Threads={threads}: {resultado.stderr}")
        else:
            try:
                # Filtrar a saída para obter apenas a última linha que contém o tempo
                linhas_saida = resultado.stdout.strip().split("\n")
                tempo_execucao = float(linhas_saida[-1])  # Última linha contém o tempo
                resultados.append(tempo_execucao)
                print(f"Execução concluída para T={T} e Threads={threads}. Tempo: {tempo_execucao} segundos")
            except ValueError:
                print(f"Erro ao interpretar o tempo para T={T} e Threads={threads}: {resultado.stdout.strip()}")

    t_medio = tempo_medio(resultados)
    print(f"Tempo médio para {threads} threads: {t_medio}")

    if resultados:  # Garantir que existem resultados para plotar
        todas_threads_resultados[threads] = resultados  # Salvar resultados para o gráfico combinado

        # Criar gráfico individual para cada quantidade de threads
        plt.figure()
        plt.plot(valores_T[:len(resultados)], resultados, marker='o', label=f"{threads} threads")
        plt.title(f"Análise de Tempo de Execução para {threads} threads")
        plt.xlabel("Número de interações")
        plt.ylabel("Tempo de Execução (segundos)")
        plt.grid(True)
        plt.legend()  # Adicionar legenda
        plt.savefig(f"analise_tempo_paralelo{threads}.png")
        # plt.show()

        salvar_resultados_em_arquivo(valores_T[:len(resultados)], resultados, t_medio, f"tempos_execucao_pararelo{threads}.txt")
    else:
        print(f"Nenhum resultado válido foi obtido para {threads} threads.")

    print("\n\n")

# Criar um gráfico combinado para todas as threads e sequencial
plt.figure()

# Adicionar os dados sequenciais ao gráfico combinado
if sequencial_resultados:
    plt.plot(valores_T[:len(sequencial_resultados)], sequencial_resultados, marker='o', label="Sequencial")

# Adicionar os dados paralelos ao gráfico combinado
for threads, resultados in todas_threads_resultados.items():
    plt.plot(valores_T[:len(resultados)], resultados, marker='o', label=f"{threads} threads")

plt.title("Análise de Tempo de Execução Combinada")
plt.xlabel("Número de interações")
plt.ylabel("Tempo de Execução (segundos)")
plt.grid(True)
plt.legend()  # Adicionar legenda indicando a quantidade de threads
plt.savefig("analise_tempo_combinada.png")
# plt.show()

print("Todas as execuções foram concluídas.")
