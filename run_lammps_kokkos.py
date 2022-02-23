import os

bench_dir="../../../lammps/bench/"
bench_in="in.rhodo.scaled.test"
gthreshold=75

for k in range(0,10):
    bench_cmd="'/usr/bin/mpiexec.openmpi -np 1 ../bin/lmp_kokkos_cuda_mpi -in " + bench_in + " -k on g 1 -sf kk -pk kokkos neigh half newton on'"
    tag = bench_in + "_kokkos_1g_1n_2M"
    cmd="python3 run_wrapper.py --cmd " + bench_cmd + " --bench lammps_gpu --tag " + tag + " --dir " + bench_dir + " --arch BM.GPU3.8 --gpu-power 1 --cpu-power 1 --gpu-threshold " + str(gthreshold)
    print("running " + cmd)
    os.system(cmd) 
