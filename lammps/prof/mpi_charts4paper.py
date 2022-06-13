import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns              
import matplotlib.ticker as tkr
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import os
import matplotlib.lines as lines
import matplotlib.ticker as ticker
from itertools import islice
import sys
#from plot_utils import *

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))
#PALETTE = [COLORS["peach2"], COLORS["g1"]]
#PALETTE_B = [COLORS["b3"], COLORS["b3"]]
#PALETTE_GW = [COLORS[r] for r in ["gw3","gw2","gw1"]]
#HATCHES = ['', '/'*4, '\\'*4]

mpi_funcs = ["MPI_Scan", "MPI_Comm_dup", "MPI_Comm_size", "MPI_Alltoallv", "MPI_Cart_shift", \
    "MPI_Finalize", "MPI_Wait", "MPI_Reduce", "MPI_Comm_rank", "MPI_Allgather", "MPI_Reduce_scatter", \
    "MPI_Barrier", "MPI_Sendrecv", "MPI_Waitany", "MPI_Cart_rank", "MPI_Cart_create", "MPI_Irecv", \
    "MPI_Cart_get", "MPI_Allreduce", "MPI_Comm_free", "MPI_Bcast", "MPI_Init", "MPI_Alltoall", "MPI_Send"]

fname = sys.argv[1]
fout = sys.argv[2]
data = pd.read_csv(fname, sep=',')

data['Benchmark'] = data['Benchmark'].apply(lambda x: x[3:])

mpi_tot_data = data.melt(id_vars=["Processes", "Size", "Benchmark"], value_vars=["MPI_(%)"])

sns.set_style("whitegrid")
g = sns.catplot(data=mpi_tot_data, hue='Processes', x='Benchmark', col='Size', y='value', \
    kind='bar', palette='mako')
g.set_axis_labels("Problem Size [K atoms]","MPI Total Time [%]")
g.savefig(fout + "_mpi_tot_data.png")

top_N = 5
vals = {}
for f in mpi_funcs:
    if f not in data.columns:
        print(f + " not in data...")
        continue
    vals[f] = data[f].mean()

vals = {k: v for k, v in sorted(vals.items(), reverse=True, key=lambda item: item[1])}

top_vals = take(top_N, vals.items())
top_funcs = [top_val[0] for top_val in top_vals]

mpi_func_data = data.melt(id_vars=["Processes", "Size", "Benchmark"], value_vars=top_funcs)
print(mpi_func_data)
g2 = sns.catplot(data=mpi_func_data, col='Processes', hue='variable', row='Benchmark', x='Size', y='value', \
    kind='bar', palette='CMRmap')
g2.set_axis_labels("Problem Size [K atoms]","MPI Function Time [%]")
g2.savefig(fout + "_mpi_funcs.png")
