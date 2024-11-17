program="sequencial"

# Number of times to run the program
n=100000

for ((i=0; i<=n; i+=400)); do
  ./$program $i
done