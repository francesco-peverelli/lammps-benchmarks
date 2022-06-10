import os

benchmarks= ["rhodo", "lj", "eam", "chain"]
sizes =  ["", ".scaled", ".scaled_864", ".scaled_2048"]
katoms = ["32", "256", "864", "2048"]

for b in benchmarks:
    snum = 0
    for s in sizes:
        in_name = "in." + b + s 
        cmd="python3 profile_lammps_gpu.py " + in_name + " " + katoms[snum] + " " + str(snum)
        print("Executing" + cmd)
        os.system(cmd)
        snum = snum + 1
