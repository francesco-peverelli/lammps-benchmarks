import subprocess
import os

benchmarks = ["chute"]
variants = ["",".scaled",".scaled_864",".scaled_2048"]
dims = [32, 256, 864, 2048]
#variants = ["",]
#dims = [32]


for b in benchmarks:
    i = 0
    for v in variants:
        name = "in." + b + v
        cmd = "./run_lammps_intel.sh " + name + " " + str(dims[i])
        os.system("/bin/bash -c '" + cmd + "'")
        i = i + 1
