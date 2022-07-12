from unicodedata import category
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

def main(fname, fout,fig_extns):

    data = pd.read_csv(fname, sep=',')

    data['Benchmark'] = data['Benchmark'].apply(lambda x: x[3:])

    #add missing sections
    op_type = data['Category'].unique()
    operation = data['Operation'].unique()
    bench = data['Benchmark'].unique()
    gpus = data['GPUs'].unique()
    sizes = data['Size'].unique()

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


    filt_df = data[data['Time(%)'] > -10.0]
    filt_df = filt_df[filt_df['Category'] != 'CUDA_API']
    first = True

    for b in bench:
        for g in gpus:
            for s in sizes:
                partial_df = filt_df[(filt_df['Benchmark'] == b) & (filt_df['GPUs'] == g) & (filt_df['Size'] == s)]
                tot_time = float(partial_df['Total Time (ns)'].sum())
                partial_df['Time(%)'] = 100 * (partial_df['Total Time (ns)'].div(tot_time))
                if first:
                    df = partial_df
                    first = False
                else:
                    df = pd.concat([df, partial_df], ignore_index = True, axis = 0)
                

    #mpi_tot_data = data.melt(id_vars=["Processes", "Size", "Benchmark"], value_vars=["MPI_(%)"])
    filt_df = df.sort_values(['Benchmark','Size','GPUs','Operation'])
    original_data = filt_df.copy()
    filt_df.groupby(['Size','GPUs','Operation'])
    # sns.set_style("whitegrid")
    g = sns.catplot(data=filt_df, col='GPUs', row='Benchmark', x='Size', hue='Operation', y='Time(%)', \
        kind='bar', palette='Paired')
    #g.set_axis_labels("Problem Size [K atoms]","Task Total Time [%]")
    #g.set_xticklabels(sorted(phases))
    g.savefig(fout + fig_extns)

    original_data.drop('Average (ns)', inplace=True, axis=1)
    original_data.drop('Minimum (ns)', inplace=True, axis=1)
    original_data.drop('Maximum (ns)', inplace=True, axis=1)
    original_data.drop('StdDev (ns)', inplace=True, axis=1)
    original_data.drop('Total Time (ns)', inplace=True, axis=1)


    procsmap = {}
    categorical_value = 0
    for p in gpus:
        procsmap[p] = categorical_value
        categorical_value += 1
    data=original_data
    data['Category'] = data['GPUs']

    data['Category'] = data['Category'].apply(lambda x: procsmap[x])
    mprocs = data['Category'].max()+1
    functions = data['Operation'].unique()

    data=data.groupby(['Benchmark','Size', 'GPUs','Operation']).mean()
    g= sns.displot(data=data, col='Size', row='Benchmark', kind='hist',\
                x='Category', hue='Operation', weights='Time(%)', multiple="stack", palette='OrRd', bins=mprocs, binrange=(0,mprocs))
    g.set_axis_labels("GPUs","Run Time [\%]")
    sns.move_legend(g, "lower center", bbox_to_anchor=(.46, 1), ncol=int(len(functions)/3), title=None, frameon=False)

    x = np.arange(0+0.5,categorical_value+0.5, 1)
    g.set(xticks=x)
    g.set_xticklabels(gpus)
    g.set_titles(row_template="B.={row_name}",col_template="S.={col_name}")
    g.savefig(fout + "_stacked" + fig_extns)

