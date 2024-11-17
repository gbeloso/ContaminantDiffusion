# include <stdio.h>
# include <stdlib.h>

# define N 100 // Tamanho da grade
# define D 0.1 // Coeficiente de difusão
# define DELTA_T 0.01
# define DELTA_X 1.0

void diff_eq(double C[N][N], double C_new[N][N], int T) {
    for (int t = 0; t < T; t++) {
        for (int i = 1; i < N - 1; i++) {
            for (int j = 1; j < N - 1; j++) {
                C_new[i][j] = C[i][j] + D * DELTA_T * ((C[i+1][j] + C[i-1][j] + C[i][j+1] + C[i][j-1] - 4 * C[i][j]) / (DELTA_X));
            }
        }
        // Atualizar matriz para a próxima iteração
        for (int i = 1; i < N - 1; i++) {
            for (int j = 1; j < N - 1; j++) {
                C[i][j] = C_new[i][j];
            }
        }
    }
}

int main(int argc, char ** argv) {
    int T = atoi(argv[1]);

    char arquivo[100];
    sprintf(arquivo, "saida_sequencial/%d.csv", T);
    FILE * saida = fopen(arquivo, "w+");

    double C[N][N] = {0}; // Concentração inicial
    double C_new[N][N] = {0}; // Concentração para a próxima iteração

    C[N/2][N/2] = 1.0; // Inicializar uma concentração alta no centro
    diff_eq(C, C_new, T);// Executar a equação de difusão

    printf("Concentração final no centro: %f\n", C[N/2][N/2]); // Exibir resultado para verificação

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if(j == N-1){
                fprintf(saida, "%f\n", C[i][j]);
            }
            else{
                fprintf(saida, "%f,", C[i][j]);
            }
        }
    }
}