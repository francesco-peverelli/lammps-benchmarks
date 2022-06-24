

""" Argv 1: benchmark input file name
    Argv 2: problem size string (e.g. 32k, 2M, ...)
    Argv 3: problem size index [0-3]
"""

import os
import sys

gpu_mpi_dict = [{1 : 6, 2 : 12, 4 : 12, 6 : 18, 8 : 24},
        {1 : 16, 2 : 28, 4 : 32, 6 : 48, 8 : 48},
        {1 : 36, 2 : 36, 4 : 36, 6 : 48, 8 : 48},
        {1 : 16, 2 : 48, 4 : 48, 6 : 48, 8 : 48}]


problem_idx = int(sys.argv[3])
bench_dir="../lammps/bench/"
bench_in=sys.argv[1]
gthreshold=40

for gpu,mpi in gpu_mpi_dict[problem_idx].items():
    for k in range(0,10):
        bench_cmd="'mpiexec -np " + str(mpi) + " env OMP_NUM_THREADS=1 ../bin/lmp_intel_cpu_intelmpi -in " + bench_in + " -sf gpu -pk gpu " + str(gpu) + "'"
        tag = bench_in + "_" + str(gpu) + "g_" + str(mpi) + "n_"+ sys.argv[2]
#        cmd="python3 run_wrapper.py --cmd " + bench_cmd + " --bench lammps_gpu --tag " + tag + " --dir " + bench_dir + " --arch BM.GPU3.8 --gpu-power 0 --cpu-power 0"
        cmd="python3 run_wrapper.py --cmd " + bench_cmd + " --bench lammps_gpu --tag " + tag + " --dir " + bench_dir + " --arch BM.GPU3.8 --gpu-power " + str(gpu) + " --cpu-power 1 --gpu-threshold " + str(gthreshold)


        os.system(cmd) 
