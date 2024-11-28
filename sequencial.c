# include <stdio.h>
# include <stdlib.h>
# include <omp.h>
# include<math.h>

# define N 2000 // Tamanho da grade
# define D 0.1 // Coeficiente de difusão
# define DELTA_T 0.01
# define DELTA_X 1.0

void diff_eq(double ***C, int T) {
    double difmedio = 0.0;
    for (int t = 0; t < T; t++) {
        for (int i = 1; i < N - 1; i++) {
            for (int j = 1; j < N - 1; j++) {
                C[(t+1)%2][i][j] = C[t%2][i][j] + D * DELTA_T * ((C[t%2][i+1][j] + C[t%2][i-1][j] + C[t%2][i][j+1] + C[t%2][i][j-1] - 4 * C[t%2][i][j]) / (DELTA_X));
                difmedio += fabs(C[(t + 1) % 2][i][j] - C[t % 2][i][j]);
            }
        }
        if ((t%100) == 0)
          printf("interacao %d - diferenca=%g\n", t, difmedio/((N-2)*(N-2)));
    }
}

int main(int argc, char ** argv) {
    int T = atoi(argv[1]);

    char arquivo[100];
    sprintf(arquivo, "saida_sequencial/%d.csv", T);
    FILE * saida = fopen(arquivo, "w+");

    double ***C = (double ***)malloc(2 * sizeof(double **));
    for(int t = 0; t<2; t++){
        C[t] = (double **)malloc(N * sizeof(double *));
        for (int i = 0; i < N; i++) {
            C[t][i] = (double *)malloc(N * sizeof(double));
        }
    }
    // double C[2][N][N] = {0}; // Concentração inicial

    for (int t = 0; t < 2; t++)
        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++)
                C[t][i][j] = 0.0;

    C[0][N/2][N/2] = 1.0; // Inicializar uma concentração alta no centro
    double start = omp_get_wtime();
    diff_eq(C, T);// Executar a equação de difusão
    double end = omp_get_wtime();

    printf("Concentração final no centro: %f\n", C[T%2][N/2][N/2]); // Exibir resultado para verificação

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if(j == N-1){
                fprintf(saida, "%f\n", C[T%2][i][j]);
            }
            else{
                fprintf(saida, "%f,", C[T%2][i][j]);
            }
        }
    }

    printf("%f\n", end - start);

    for (int t = 0; t < 2; t++) {
        for (int i = 0; i < N; i++) {
            free(C[t][i]);
        }
        free(C[t]);
    }
    free(C);

    return 0;
}
