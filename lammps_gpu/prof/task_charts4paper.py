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

def main(fname, fout):

    data = pd.read_csv(fname, sep=',')

    data['Benchmark'] = data['Benchmark'].apply(lambda x: x[3:])

    #add missing sections
    phases = data['Section'].unique()
    bench = data['Benchmark'].unique()
    procs = data['GPUs'].unique()
    sizes = data['Size'].unique()

    for ph in phases:
        for b in bench:
            for p in procs:
                for s in sizes:
                    combo = [b, s, p, ph]
                    if len(data[(data['Benchmark'] == b) & (data['GPUs'] == p) 
                        & (data['Size'] == s) & (data['Section'] == ph)]) == 0:
                        entries = combo + [0.0, 0.0, 0.0, 0.0, 0.0]
                        new_data = pd.DataFrame([entries], columns=list(data.columns.values)) 
                        data = pd.concat([data, new_data], ignore_index = True, axis = 0)

    #mpi_tot_data = data.melt(id_vars=["GPUs", "Size", "Benchmark"], value_vars=["MPI_(%)"])
    data = data.sort_values(['Benchmark','Size','GPUs','Section'])
    data.groupby(['Size','GPUs','Section'])
    data = data.groupby(['Benchmark','Size','GPUs','Section'],as_index=False).mean()
    sns.set_style("whitegrid")
    g = sns.catplot(data=data, col='GPUs', row='Benchmark', x='Size', hue='Section', y='%total', \
        kind='bar', palette='mako')
    #g.set_axis_labels("Problem Size [K atoms]","Task Total Time [%]")
    #g.set_xticklabels(sorted(phases))
    g.savefig(fout + ".png")
