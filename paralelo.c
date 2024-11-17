# include <stdio.h>
#include <omp.h>
# include <stdlib.h>

# define N 100 // Tamanho da grade
# define D 0.1 // Coeficiente de difusão
# define DELTA_T 0.01
# define DELTA_X 1.0

void diff_eq(double C[2][N][N], int T) {
    for (int t = 0; t < T; t++) {
        int i, j;
        #pragma omp parallel default(none) private(i,j) shared(C,t)
        {   
            #pragma omp for
            for (i = 1; i < N - 1; i++) {
                for (j = 1; j < N - 1; j++) {
                    C[(t+1)%2][i][j] = C[t%2][i][j] + D * DELTA_T * ((C[t%2][i+1][j] + C[t%2][i-1][j] + C[t%2][i][j+1] + C[t%2][i][j-1] - 4 * C[t%2][i][j]) / (DELTA_X));
                }
            }
        }
        
    }
}

int main(int argc, char ** argv) {
    int T = atoi(argv[1]);
    char arquivo[100];
    sprintf(arquivo, "saida_paralelo/%d.csv", T);
    FILE * saida = fopen(arquivo, "w+");

    double C[2][N][N] = {0}; 

    C[0][N/2][N/2] = 1.0; // Inicializar uma concentração alta no centro

    omp_set_num_threads(4);

    diff_eq(C, T); // Executar a equação de difusão

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
}