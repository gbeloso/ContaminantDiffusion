import matplotlib.pyplot as plt
num_threads = [1, 2, 4, 8, 16]
media_valores = []

for i in num_threads:
    if i == 1:
        with open("./tempos_execucao_sequencial.txt", "r") as arquivo:
            for linha in arquivo:
                valores_sequencial = linha.strip().split(",")
            media_valores.append(float(valores_sequencial[-1]))
    else:
        with open(f"./tempos_execucao_paralelo{i}.txt", "r") as arquivo:
            for linha in arquivo:
                valores_paralelo = linha.strip().split(",")
            media_valores.append(float(valores_paralelo[-1]))

# print(media_valores)

T1 = media_valores[0]
speedup = [T1 / t for t in media_valores]

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1) 
plt.plot(num_threads, speedup, marker='o', label='Speedup Real')
plt.plot(num_threads, num_threads, linestyle='--', color='red', label='Speedup Linear (Ideal)')
for i, txt in enumerate(speedup):
    plt.text(num_threads[i], speedup[i], f"{txt:.2f}", ha='center', va='bottom')
plt.xlabel('Número de Threads')
plt.ylabel('Speedup')
plt.title('Gráfico de Speedup')
plt.legend()
plt.grid(True)
plt.savefig(f"speedup{num_threads}.png")
# plt.show()

efficiency = [s / t for s,t in zip(speedup, num_threads)]

plt.plot(num_threads, efficiency, marker='o', label='Eficiência Real')
plt.plot(num_threads, [1] * len(num_threads), linestyle='--', color='red', label='Eficiência Linear')

for i, txt in enumerate(efficiency):
    plt.text(num_threads[i], efficiency[i], f"{txt:.2f}", ha='center', va='bottom')
    
plt.xlabel('Número de Threads')
plt.ylabel('Eficiência')
plt.title('Gráfico de Eficiência')
plt.legend()
plt.grid(True)
plt.savefig(f"eficiencia{num_threads}.png")
# plt.show()