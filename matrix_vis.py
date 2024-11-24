import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

iteracoes_diferentes = []
for i in range(0, 100001, 400):
    paralelo = pd.read_csv('saida_paralelo/' + str(i) + '.csv')
    sequencial = pd.read_csv('saida_sequencial/' + str(i) + '.csv')
    if(not(paralelo.equals(sequencial))or not(sequencial.equals(paralelo))):
        iteracoes_diferentes.append(i)
if len(iteracoes_diferentes) > 0:
    print("Diferença nas iteracoes: ")
    for i in iteracoes_diferentes:
        print(str(i) + ', ')
else:
    print("O sequencial e o paralelo deram o mesmo resultado para todas as iterações")

for i in range(0, 100001, 400):
    arquivo = "saida_paralelo/" + str(i) + ".csv"
    image = "saida_paralelo/images/" + str(i) + ".png"
    df = pd.read_csv(arquivo)
    fig, ax = plt.subplots(figsize=(6,6))
    sns.heatmap(df, ax=ax, cbar=False)
    ax.set_axis_off()
    plt.savefig(image, dpi=300, bbox_inches='tight')
    plt.close()
    del df

for i in range(0, 100001, 400):
    arquivo = "saida_sequencial/" + str(i) + ".csv"
    image = "saida_sequencial/images/" + str(i) + ".png"
    df = pd.read_csv(arquivo)
    fig, ax = plt.subplots(figsize=(6,6))
    sns.heatmap(df, ax=ax, cbar=False, cmap='coolwarm')
    ax.set_axis_off()
    plt.savefig(image, dpi=300, bbox_inches='tight')
    plt.close()
    del df