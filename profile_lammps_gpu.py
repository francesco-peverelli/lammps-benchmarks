import os
import sys

""" Argv 1: benchmark input file name
    Argv 2: problem size string (e.g. 32k, 2M, ...)
    Argv 3: problem size index [0-3]
"""


gpu_mpi_dict = [{1 : 6, 2 : 12, 4 : 12, 6 : 18, 8 : 24},
        {1 : 16, 2 : 28, 4 : 32, 6 : 48, 8 : 48},
        {1 : 36, 2 : 36, 4 : 36, 6 : 48, 8 : 48},
        {1 : 16, 2 : 48, 4 : 48, 6 : 48, 8 : 48}]


problem_idx = int(sys.argv[3])
start_dir=os.getcwd()
bench_dir="../lammps/bench/"
bench_in=sys.argv[1] 
bench_name = bench_in
bench_in += "-double"
os.chdir(bench_dir)

for gpu,mpi in gpu_mpi_dict[problem_idx].items():
    bench_cmd="nsys profile mpiexec -mps -np " + str(mpi) + " env OMP_NUM_THREADS=1 ../bin/lmp_intel_cpu_intelmpi-double -in " + bench_name + " -sf gpu -pk gpu " + str(gpu) + ""
    tag = bench_in + "_" + str(gpu) + "g_" + str(mpi) + "n_"+ sys.argv[2]
    cmd = bench_cmd + " > " + start_dir + "/lammps_gpu/prof/" + bench_in + "_" + sys.argv[2] + "_g" + str(gpu) + "_profiling.txt"
    print("running " + cmd)
    os.system(cmd) 
    os.system("rm log.* ")
    os.system("mv aps_* " + start_dir + "/lammps_gpu/prof/" + bench_in + "_" + sys.argv[2] + "_g" + str(gpu) + "_aps")
    os.system("nsys stats report1.qdrep -f csv -r apigpusum:base > " + start_dir + "/lammps_gpu/prof/" + bench_in + "_" + sys.argv[2] + "_g" + str(gpu) + "_nsys.csv")
    os.system("sed -i 1,4d " + start_dir + "/lammps_gpu/prof/" + bench_in + "_" + sys.argv[2] + "_g" + str(gpu) + "_nsys.csv")
    os.system("rm report1.*")
