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

def main(fname, fout, fig_extns):
    mpi_funcs = ["MPI_Scan", "MPI_Comm_dup", "MPI_Comm_size", "MPI_Alltoallv", "MPI_Cart_shift", \
        "MPI_Finalize", "MPI_Wait", "MPI_Reduce", "MPI_Comm_rank", "MPI_Allgather", "MPI_Reduce_scatter", \
        "MPI_Barrier", "MPI_Sendrecv", "MPI_Waitany", "MPI_Cart_rank", "MPI_Cart_create", "MPI_Irecv", \
        "MPI_Cart_get", "MPI_Allreduce", "MPI_Comm_free", "MPI_Bcast", "MPI_Init", "MPI_Alltoall", "MPI_Send"]

    data = pd.read_csv(fname, sep=',')

    # Reset matplotlib settings;
    plt.rcdefaults()
    plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"],
    })
    plt.rcParams["font.size"] = 30
    plt.rcParams["xtick.labelsize"]= 30    # major tick size in points
    plt.rcParams["ytick.labelsize"]= 30    # major tick size in points
    plt.rcParams["legend.fontsize"]= 30   # major tick size in points
    plt.rcParams["legend.handletextpad"]=0.01    # major tick size in points
    # plt.rcParams["axes.titlesize"]= 10     # major tick size in points

    plt.rcParams['hatch.linewidth'] = 0.6

    plt.rcParams['axes.labelpad'] = 0
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    data['Benchmark'] = data['Benchmark'].apply(lambda x: x[3:])
    print(data)
    mpi_tot_data = data.melt(id_vars=["Processes", "Size", "Benchmark"],    \
    value_vars=["MPI_(%)","Max_MPI_(%)","Min_MPI_(%)","MPI_Imb_(%)", "Max_Imb_(%)","Min_Imb_(%)"])
    print(mpi_tot_data)

    sns.set_style("whitegrid")
    g = sns.catplot(data=mpi_tot_data, x='Processes', hue ='variable', row='Benchmark', col='Size', y='value', \
         kind='bar', palette='Paired')
    g.savefig(fout + "_mpi_old"+fig_extns)
    
    procs = mpi_tot_data['Processes'].unique()
    procsmap = {}
    categorical_value = 0
    for p in procs:
        procsmap[p] = categorical_value
        categorical_value += 1
    mpi_tot_data['Category'] = mpi_tot_data['Processes']
    mpi_tot_data['Category'] = mpi_tot_data['Category'].apply(lambda x: procsmap[x])
    mprocs = mpi_tot_data['Category'].max()+1

    mpi_tot_data=mpi_tot_data.groupby(['Benchmark','Size','Processes','variable']).mean()
    g= sns.displot(data=mpi_tot_data, col='Size', row='Benchmark', kind='hist',\
                x='Processes', hue='variable', weights='value', multiple="stack", palette='PuBu'\
                , bins=mprocs, binrange=(0,mprocs))
    g.set_titles(row_template="B.={row_name}",col_template="Size={col_name}")
        
    g.set_axis_labels("Problem Size [K atoms]","MPI Tot-al Time [\%]")
    g.savefig(fout + "_mpi_tot_data"+fig_extns)

    # g= sns.displot(data=mpi_tot_data, col='Size', kind='hist',\
    #             x='Benchmark', hue='Processes', weights='variable', multiple="stack", palette='PuBu'\
    #             , bins=mprocs, binrange=(0,mprocs))
    g.set_axis_labels("Problem Size [K atoms]","MPI Total Time [\%]")
    g.savefig(fout + "_mpi_tot_version"+fig_extns)

    # Reset matplotlib settings;
    plt.rcdefaults()
    plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"],
    })
    plt.rcParams["font.size"] = 30
    plt.rcParams["xtick.labelsize"]= 30    # major tick size in points
    plt.rcParams["ytick.labelsize"]= 30    # major tick size in points
    plt.rcParams["legend.fontsize"]= 30   # major tick size in points
    plt.rcParams["legend.handletextpad"]=0.01    # major tick size in points
    # plt.rcParams["axes.titlesize"]= 10     # major tick size in points

    plt.rcParams['hatch.linewidth'] = 0.6

    plt.rcParams['axes.labelpad'] = 0
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    top_N = 5
    vals = {}
    for f in mpi_funcs:
        if f not in data.columns:
            print(f + " not in data...")
            continue
        vals[f] = data[f].mean()

    #top 5 used in the benchmark
    vals = {k: v for k, v in sorted(vals.items(), reverse=True, key=lambda item: item[1])}
    #TODO add others?
    top_vals = take(top_N, vals.items())
    top_funcs = [top_val[0] for top_val in top_vals]

    mpi_func_data = data.melt(id_vars=["Processes", "Size", "Benchmark"], value_vars=top_funcs)
    g2 = sns.catplot(data=mpi_func_data, col='Processes', hue='variable', row='Benchmark', x='Size', y='value', \
        kind='bar', palette='CMRmap')
    g2.set_axis_labels("Problem Size [K atoms]","MPI Function Time [%]")
    g2.savefig(fout + "_mpi_funcsi"+fig_extns)

if __name__ == "__main__": 
    main()
