program="paralelo"

# Number of times to run the program
n=1000000

for ((i=0; i<=n; i+=400)); do
  ./$program $i
done