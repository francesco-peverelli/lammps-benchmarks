import pandas as pd 
import os 
import sys

experiments = ["rhodo", "lj", "eam", "chain"]
ngpus = [1, 2, 4, 6, 8]
nk_atoms = [32, 256, 864, 2048]

mpi_funcs = set() # MPI functions
mpi_data = []

files = os.listdir(os.getcwd())
filename = sys.argv[1]

first = True

for fname in files:
    if fname.endswith("nsys.csv") and fname.startswith("in."):
        try:
            file = open(fname, "r")
            in_mpi_calls = False
            in_total_time = False
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

            data = pd.read_csv(fname)
            bench_col = data.shape[0] * [bench]
            size_col = data.shape[0] * [size]
            ngpu_col = data.shape[0] * [ngpu]
            data['Benchmark'] = bench_col
            data['Size'] = size_col
            data['GPUs'] = ngpu_col
            print(data)

            if first:
                df = data
                first = False
            else:
                df = pd.concat([df, data], ignore_index = True, axis = 0)
    
        except IOError:
            print("File not found: " + fname)

for el in mpi_data:
    for func in mpi_funcs:
        if func not in el.keys():
            el[func] = 0.0

df = df.sort_values(['Benchmark','Size','GPUs'])
df.groupby(['Size','GPUs'])
print(df)
df.to_csv(filename + ".csv", index=False)
df.to_excel(filename + ".xlsx", index=False)
            
