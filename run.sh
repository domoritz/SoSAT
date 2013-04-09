for N in 1 2 3 4 5 6 7 8 9 10
do
  for f in 0 1 2 3 4 5 6 7 8 9 10
  do
    echo "N=$N, f=$f"

    eval "/usr/bin/time -o benchmark.txt --append ./run_3_times.sh \"python main.py -a genetic instances/random_ksat11.dimacs -f $f -N $N\""
  done
done
