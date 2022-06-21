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

def main(fname, fout):

    data = pd.read_csv(fname, sep=',')

    data['Benchmark'] = data['Benchmark'].apply(lambda x: x[3:])

    #add missing sections
    op_type = data['Category'].unique()
    operation = data['Operation'].unique()
    bench = data['Benchmark'].unique()
    gpus = data['GPUs'].unique()
    sizes = data['Size'].unique()

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
    filt_df.groupby(['Size','GPUs','Operation'])
    sns.set_style("whitegrid")
    g = sns.catplot(data=filt_df, col='GPUs', row='Benchmark', x='Size', hue='Operation', y='Time(%)', \
        kind='bar', palette='Paired')
    #g.set_axis_labels("Problem Size [K atoms]","Task Total Time [%]")
    #g.set_xticklabels(sorted(phases))
    g.savefig(fout + ".png")
