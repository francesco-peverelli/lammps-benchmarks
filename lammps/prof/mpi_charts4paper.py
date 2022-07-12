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
    mpi_percentage = ["MPI_(%)","Max_MPI_(%)","Min_MPI_(%)","MPI_Imb_(%)", "Max_Imb_(%)","Min_Imb_(%)"]
    mpi_percentage_nomaxmin=["Max_MPI_(%)","Min_MPI_(%)","MPI_Imb_(%)", "Max_Imb_(%)","Min_Imb_(%)"]


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
    plt.rcParams["legend.handletextpad"]=0.1    # major tick size in points
    plt.rcParams["legend.handlelength"]=1    # major tick size in points
    # plt.rcParams["axes.titlesize"]= 10     # major tick size in points
    # plt.rcParams["legend.markerscale"]=0.01   # major tick size in points

    plt.rcParams['hatch.linewidth'] = 0.6

    plt.rcParams['axes.labelpad'] = 0
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    #add missing sections
    bench = data['Benchmark'].unique()
    procs = data['Processes'].unique()
    sizes = data['Size'].unique()

    data['Benchmark'] = data['Benchmark'].apply(lambda x: x[3:])
    new_size_string='Size[k atoms]'
    data.rename(columns = {'Size':new_size_string}, inplace = True)

    mpi_tot_data = data.melt(id_vars=["Processes", new_size_string, "Benchmark"],    \
    value_vars=mpi_percentage)

    # sns.set_style("whitegrid")
    # g = sns.catplot(data=mpi_tot_data, x='Processes', hue ='variable', row='Benchmark', col='Size', y='value', \
    #      kind='bar', palette='Paired')
    # g.savefig(fout + "_mpi_old"+fig_extns)

    mpi_tot_data['Processes'] = mpi_tot_data['Processes'].apply(lambda x: int(x)) 
    mpi_tot_data[new_size_string] = mpi_tot_data[new_size_string].apply(lambda x: int(x)) 

    # Plot MPI total runtime % per rank, min max and average
    mpi_time_data = mpi_tot_data[(mpi_tot_data['variable'] == "MPI_(%)") 
        | (mpi_tot_data['variable'] == "Max_MPI_(%)")
        | (mpi_tot_data['variable'] == "Min_MPI_(%)")]
    # pd.set_option('display.max_rows', None)
    # print(mpi_time_data.to_markdown())
    g=sns.catplot(data=mpi_time_data, hue=new_size_string, col='Benchmark', kind='bar',\
                x='Processes', y='value', palette='PuBu', aspect=1.4, errwidth=.85, capsize=.4)
    g.set_axis_labels("MPI Processes", "MPI Time [\%]")
    g.savefig(fout + "_mpi_tot_data"+fig_extns)
    
    g=sns.catplot(data=mpi_time_data, hue=new_size_string, col='Benchmark', kind='box',\
                x='Processes', y='value', palette='PuBu', sharey=False, linewidth=2)
    g.set_axis_labels("MPI Processes", "MPI Time [\%]")
    g.savefig(fout + "_mpi_violin_tot_data"+fig_extns)

    # Plot MPI total imbalance % per rank, min max and average
    mpi_imb_data = mpi_tot_data[(mpi_tot_data['variable'] == "MPI_Imb_(%)") 
        | (mpi_tot_data['variable'] == "Max_Imb_(%)")
        | (mpi_tot_data['variable'] == "Min_Imb_(%)")]

    # print(mpi_imb_data.to_markdown())

    g=sns.catplot(data=mpi_imb_data, hue=new_size_string, col='Benchmark', kind='bar',\
                x='Processes', y='value', palette='PuBu', aspect=1.4, errwidth=.85, capsize=.4)
    g.set_axis_labels("MPI Processes", "MPI imbalance [\%]")
    g.savefig(fout + "_mpi_imb_data"+fig_extns)

    g=sns.catplot(data=mpi_imb_data, hue=new_size_string, col='Benchmark', kind='box',\
                x='Processes', y='value', palette='PuBu', sharey=False, linewidth=2)
    g.set_axis_labels("MPI Processes", "MPI imbalance [\%]")
    g.savefig(fout + "_mpi_imb_violin_data"+fig_extns)

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
    plt.rcParams["legend.handletextpad"]=0.05    # major tick size in points
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
    # print()
    # print(vals)
    # print()
    # print(top_vals)
    # print()
    top_funcs = [top_val[0] for top_val in top_vals]
    # print(top_funcs)
    # # print()
    # mpi_func_data = data.melt(id_vars=["Processes", "Size", "Benchmark"], value_vars=top_funcs)
    # # print(mpi_func_data)
    # # print()
########################################
    original_data=data.copy()

    original_data.drop(top_funcs, inplace=True, axis=1)
    original_data.drop(mpi_percentage, inplace=True, axis=1)
    original_data.drop('MPI_Time', inplace=True, axis=1)

    # print(original_data.columns.values.tolist())
    # print(original_data)
    # print()

    idxess=['Benchmark','Processes',new_size_string]
    tmp=set(original_data.columns.values.tolist())-set(idxess)-set(top_funcs)
    # print(tmp)
    # print()
    # original_data.drop(idxess, inplace=True, axis=1)
    original_data['others'] = original_data[tmp].sum(axis=1)
    # print(original_data['others'])
    # print()
##########################
    # # mpi_func_data = data.melt(id_vars=["Processes", "Size", "Benchmark"], value_vars=top_funcs)
    # # print(mpi_func_data)
    # # print()
    # g2 = sns.catplot(data=mpi_func_data, col='Processes', hue='variable', row='Benchmark', x='Size', y='value', \
    #     kind='bar', palette='CMRmap')
    # g2.set_axis_labels("Problem Size [K atoms]","MPI Function Time [%]")
    # g2.savefig(fout + "_mpi_funcsi"+fig_extns)

    ##################
    # print(top_funcs)
    top_funcs.append('others')
    # print(top_funcs)
    data['others']=original_data['others'] 

    mpi_func_data = data.melt(id_vars=["Processes", new_size_string, "Benchmark"], value_vars=top_funcs)
    # print(mpi_func_data)
    # print()

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
    plt.rcParams["legend.handletextpad"]=0.1    # major tick size in points
    plt.rcParams["legend.handlelength"]=1    # major tick size in points
    # plt.rcParams["axes.titlesize"]= 10     # major tick size in points

    plt.rcParams['hatch.linewidth'] = 0.6

    plt.rcParams['axes.labelpad'] = 0
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    
    procsmap = {}
    categorical_value = 0
    for p in procs:
        procsmap[p] = categorical_value
        categorical_value += 1
    mpi_func_data['Category'] = mpi_func_data['Processes']
    mpi_func_data['Category'] = mpi_func_data['Category'].apply(lambda x: procsmap[x])
    mprocs = mpi_func_data['Category'].max()+1
 
    mpi_func_data[new_size_string] = mpi_tot_data[new_size_string].apply(lambda x: int(x)) 
    procs = [int(x) for x in procs]
  
    # print(mpi_func_data)
    mpi_func_data.rename(columns = {'variable':'Function'}, inplace = True)
    functions = mpi_func_data['Function'].unique()

    mpi_func_data=mpi_func_data.groupby(['Benchmark',new_size_string,'Processes','Function']).mean()
    g2= sns.displot(data=mpi_func_data, col=new_size_string, row='Benchmark', kind='hist',\
                x='Category', hue='Function', weights='value', multiple="stack", palette='OrRd', bins=mprocs, binrange=(0,mprocs))
    g2.set_axis_labels("Processes","MPI Function Time [\%]")
    x = np.arange(0+0.5,categorical_value+0.5, 1)
    #x=x
    sns.move_legend(g2, "lower center", bbox_to_anchor=(.43, 1), ncol=len(functions), title=None, frameon=False)
    g2.set(xticks=x)
    #procs=list(procs)
    #procs.insert(0,0)
    # print(procs)
    g2.set_xticklabels(procs)
    g2.set_titles(row_template="B.={row_name}",col_template="S.={col_name}")
    g2.savefig(fout + "_mpi_funcsi_stacked"+fig_extns)

if __name__ == "__main__": 
    main()
