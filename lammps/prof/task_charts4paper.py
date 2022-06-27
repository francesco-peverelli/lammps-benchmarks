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

    data = pd.read_csv(fname, sep=',')

    data['Benchmark'] = data['Benchmark'].apply(lambda x: x[3:])

    #add missing sections
    phases = data['Section'].unique()
    bench = data['Benchmark'].unique()
    procs = data['Processes'].unique()
    sizes = data['Size'].unique()

    for ph in phases:
        for b in bench:
            for p in procs:
                for s in sizes:
                    combo = [b, s, p, ph]
                    if len(data[(data['Benchmark'] == b) & (data['Processes'] == p) 
                        & (data['Size'] == s) & (data['Section'] == ph)]) == 0:
                        entries = combo + [0.0, 0.0, 0.0, 0.0, 0.0]
                        new_data = pd.DataFrame([entries], columns=list(data.columns.values)) 
                        data = pd.concat([data, new_data], ignore_index = True, axis = 0)

    #mpi_tot_data = data.melt(id_vars=["Processes", "Size", "Benchmark"], value_vars=["MPI_(%)"])
    data = data.sort_values(['Benchmark','Size','Processes','Section'])
    data.groupby(['Size','Processes','Section'])
    sns.set_style("whitegrid")
    g = sns.catplot(data=data, col='Processes', row='Benchmark', x='Size', hue='Section', y='%total', \
        kind='bar', palette='mako')
    g.savefig(fout + fig_extns)

    data.drop('min time', inplace=True, axis=1)
    data.drop('avg time', inplace=True, axis=1)
    data.drop('max time', inplace=True, axis=1)
    data.drop('%varavg', inplace=True, axis=1)

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
    
    procsmap = {}
    categorical_value = 0
    for p in procs:
        procsmap[p] = categorical_value
        categorical_value += 1
    data['Category'] = data['Processes']
    data['Category'] = data['Category'].apply(lambda x: procsmap[x])
    mprocs = data['Category'].max()+1
   
    # print(data)
    data=data.groupby(['Benchmark','Size','Processes','Section']).mean()
    g= sns.displot(data=data, col='Size', row='Benchmark', kind='hist',\
                x='Category', hue='Section', weights='%total', multiple="stack", palette='BuPu', bins=mprocs, binrange=(0,mprocs))
    g.set_axis_labels("MPI Processes","Run Time [\%]")
    x = np.arange(0+0.5,categorical_value+0.5, 1)
    #x=x
    g.set(xticks=x)
    #procs=list(procs)
    #procs.insert(0,0)
    # print(procs)
    g.set_xticklabels(procs)
    g.set_titles(row_template="B.={row_name}",col_template="S.={col_name}")

    #g= sns.displot(data=data_mod, col='Size', row='Benchmark', \
     #           x='Processes', hue='Section', multiple="stack", palette='mako')
    
    # for p in procs:
    #     for b in bench:
    #         print(data[(data['Benchmark'] == b) & (data['Processes'] == p) ].columns.values)
    #         g.map_dataframe(sns.displot(data=data[(data['Benchmark'] == b) & (data['Processes'] == p) ], \
    #             x='Size', hue='Section', multiple="stack", palette='mako'))
            # sns.displot(data=data[(data['Benchmark'] == b) & (data['Processes'] == p) ], x='Size', y='%total', hue='Section', multiple="stack" )
    #g.set_axis_labels("Problem Size [K atoms]","Task Total Time [%]")
    #g.set_xticklabels(sorted(phases))
    
    g.savefig(fout + "_stacked" + fig_extns)
