import pandas as pd
import os
import sys

experiments = ["rhodo", "rhodo-e-5", "rhodo-e-6", "rhodo-e-7"]
mpi_nproc = [1, 2, 4, 8, 16, 32, 64]
nk_atoms = [32, 256, 864, 2048]

files = os.listdir(os.getcwd())
filename = sys.argv[1]

new_df = True

for fname in files:
    if fname.endswith("_profiling.txt") and fname.startswith("in."):
        try:
            file = open(fname, "r")
            params = fname.replace(".scaled","").split('_')
            if params[1].endswith('-double'):
                params[0] += '-double'
            elif params[1].endswith('-single'):
                params[0] += '-single'
            bench = params[0]
            size = int(params[len(params)-2][:-1])
            processes = int(params[len(params)-4][:-1])
            if (bench[3:] not in experiments):
                print(bench[3:] + " not found!")
                continue
            if (size not in nk_atoms):
                print(size + " not found!")
                continue
            if (processes not in mpi_nproc):
                print(processes + " not found!")
                continue
            in_header = False
            skip_line = False
            read_vals = False
            done = False
            header = []
            cols = []
            for line in file:
                if line.find("MPI task timing breakdown:") >= 0:
                    in_header = True
                    continue
                if in_header:
                    header = line.split('|')
                    header = [x.strip() for x in header]
                    header = ['Benchmark','Size','Processes'] + header
                    skip_line = True
                    in_header = False
                    continue
                if skip_line:
                    read_vals = True
                    skip_line = False
                    continue
                if read_vals:
                    col = line.split('|')
                    col = [x.strip() for x in col]
                    col = [bench, size, processes] + col
                    cols.append(col)
                    if line.find("Other") >= 0:
                        read_vals = False

            print(header)
            print(cols)

            if new_df:
                data = pd.DataFrame(cols, columns=header)
                new_df = False
            else:
                d2 = pd.DataFrame(cols, columns=header)
                data = pd.concat([data, d2], ignore_index = True, axis = 0)
        except IOError:
            print("File not found: " + fname)

data = data.sort_values(['Benchmark','Size','Processes'])
data.groupby(['Size','Processes'])
data.to_csv(filename + ".csv", index=False)
data.to_excel(filename + ".xlsx", index=False)