import subprocess
import os

benchmarks = ["rhodo", "lj","eam","chain","chute"]
variants = ["",".scaled",".scaled_864",".scaled_2048"]
dims = [32, 256, 864, 2048]

for b in benchmarks:
    i = 0
    for v in variants:
        name = "in." + b + v
        cmd = "./profile_lammps_intel.sh " + name + " " + str(dims[i])
        os.system("/bin/bash -c '" + cmd + "'")
        i = i + 1
