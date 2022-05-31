import pandas as pd
import os
import sys

experiments = ["rhodo", "lj", "chain", "eam"]
ngpus = [1, 2, 4, 6, 8]
nk_atoms = [32, 256, 864, 2048]

files = os.listdir(os.getcwd())
filename = sys.argv[1]

new_df = True

for fname in files:
    if fname.endswith("_profiling.txt") and fname.startswith("in."):
        try:
            file = open(fname, "r")
            print(fname)
            params = fname.split('_')
            bench = params[0].replace(".scaled","")
            if params[len(params)-3].endswith('k'):
                size = int(params[len(params)-3][:-1])
            else:
                size = int(params[len(params)-3])
            ngpu = int(params[len(params)-2][1:])
            if (bench[3:] not in experiments):
                print(bench[3:] + " not found!")
                continue
            if (size not in nk_atoms):
                print(str(size) + " not found!")
                continue
            if (ngpu not in ngpus):
                print(str(ngpu) + " not found!")
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
                    header = ['Benchmark','Size','GPUs'] + header
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
                    col = [bench, size, ngpu] + col
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

data = data.sort_values(['Benchmark','Size','GPUs'])
data.groupby(['Size','GPUs'])
data.to_csv(filename + ".csv", index=False)
data.to_excel(filename + ".xlsx", index=False)