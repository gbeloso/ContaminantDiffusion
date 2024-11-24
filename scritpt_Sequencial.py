import os
import subprocess
import matplotlib.pyplot as plt

def tempo_medio(resultados):
    if len(resultados) == 0:
        return 0
    soma = sum(resultados)
    return soma / len(resultados)

def salvar_resultados_em_arquivo(valores_T, resultados, tempo_medio, nome_arquivo="tempos_execucao_sequencial.txt"):
    with open(nome_arquivo, "w") as arquivo:
        for T, tempo in zip(valores_T, resultados):
            arquivo.write(f"{tempo:.6f}\n")
        arquivo.write("\n")
        arquivo.write(f"{tempo_medio:.6f}")
    print(f"Resultados salvos no arquivo: {nome_arquivo}")


inicio_T = 0
fim_T = 400
passo_T = 100

valores_T = list(range(inicio_T, fim_T + 1, passo_T))

arquivo_c = "sequencial.c"
executavel = "sequencial.exe"

print("Compilando o programa...")
subprocess.run(["gcc", "-fopenmp", arquivo_c, "-o", executavel], check=True)

saida_diretorio = "saida_sequencial"
os.makedirs(saida_diretorio, exist_ok=True)

resultados = []
for T in valores_T:
    print(f"Executando o programa com T={T}...")
    resultado = subprocess.run([f"./{executavel}", str(T)], capture_output=True, text=True)

    if resultado.returncode != 0:
        print(f"Erro ao executar o programa com T={T}: {resultado.stderr}")
    else:
        try:
            tempo_execucao = float(resultado.stdout.strip())
            resultados.append(tempo_execucao)
            print(f"Execução concluída para T={T}. Tempo: {tempo_execucao} segundos")
        except ValueError:
            print(f"Erro ao interpretar o tempo para T={T}: {resultado.stdout.strip()}")

tempo_medio = tempo_medio(resultados)
print(f"Tempo médio: {tempo_medio}")

plt.plot(valores_T, resultados, marker='o')
plt.title("Análise de Tempo de Execução")
plt.xlabel("Número de interações")
plt.ylabel("Tempo de Execução (segundos)")
plt.grid(True)
plt.savefig("analise_tempo_sequencial.png")
# plt.show()

salvar_resultados_em_arquivo(valores_T, resultados, tempo_medio)

print("Todas as execuções foram concluídas.")
