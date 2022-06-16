
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

benchmarks = ['rhodo', 'lj', 'eam', 'chain', 'chute']
sizes = [32, 256, 864, 2048]
procs = [1, 2, 4, 8, 16, 32, 64]
do_power = False

benchmarks = sorted(benchmarks)
sizes = sorted(sizes)
procs = sorted(procs)

bench_ts = { 'rhodo' : 2, 'lj' : 0.005, 'eam' : 0.005, 'chain' : 0.012, 'chute' : 0.0001}
bench_units = { 'rhodo' : 'real', 'lj' : 'lj', 'eam' : 'metal', 'chain' : 'lj', 'chute' : 'lj'}

def convert_to_tss(time,unit, ts_v):
    if unit == 'lj':
        return (time / (24*60*60)) * (1/ts_v)
    elif unit == 'metal':
        return ((time*1000) / (24*60*60)) * (1/ts_v)
    elif unit == 'real':
        return ((time*1e6) / (24*60*60)) * (1/ts_v)

data = pd.read_csv('runs.csv')

#Cleanup data for graph generation
bench_df = data
bench_df = bench_df[['kokkos' not in x for x in bench_df['TAG']]]
bench_df = bench_df[['testkmp' not in x for x in bench_df['TAG']]]
bench_df = bench_df[bench_df['PERFORMANCE'].isnull() == 0]
for s in sizes:
    bench_df['TAG'] = bench_df['TAG'].apply(lambda x: x.replace('scaled_' + str(s) + '_','scaled_'))
    bench_df['TAG'] = bench_df['TAG'].apply(lambda x: x.replace('scaled_' + str(s) + '-','scaled-'))
tmp = bench_df[['chute' in x for x in bench_df['TAG']]]
#for index, row in tmp.iterrows():
#    print(row)

if do_power:
    bench_df = bench_df[bench_df['POWER'].isnull() == 0]
bench_df = bench_df[['1ont' in x for x in bench_df['TAG']]]
bench_df = bench_df.groupby('TAG',as_index=False).mean()
tmp = bench_df[['chute' in x for x in bench_df['TAG']]]
bench_df[['NAME','PROCS','ONT','SIZE','THRESHOLD']] = bench_df['TAG'].str.split('_', expand=True)
bench_df.drop('TAG', inplace=True, axis=1)
bench_df.drop('THRESHOLD', inplace=True, axis=1)
bench_df.drop('ONT', inplace=True, axis=1)
bench_df['SIZE'] = bench_df['SIZE'].apply(lambda x: int(x.replace('k','')))
bench_df['PROCS'] = bench_df['PROCS'].apply(lambda x: int(x.replace('n','')))
bench_df['NAME'] = bench_df['NAME'].apply(lambda x: x.replace('.scaled','').replace('in.','').replace('.test',''))

bench_df = bench_df[[x in benchmarks for x in bench_df['NAME']]]

# Convert all to timesteps/s
bench_df['PERFORMANCE'] = bench_df.apply(lambda x: convert_to_tss(x.PERFORMANCE, bench_units[x.NAME.split('-')[0]],bench_ts[x.NAME.split('-')[0]]), axis=1)
if do_power:
    bench_df['POWEREFF'] = bench_df['PERFORMANCE'] / bench_df['POWER']
bench_df = bench_df[bench_df['PROCS'] <= 64]
bench_df['PAREFF'] = bench_df['PERFORMANCE']
bench_df = bench_df.sort_values(['NAME','SIZE','PROCS'])

# Compute parallel efficiency column
divisor = []
for b in benchmarks:
    for s in sizes:
        for p in procs:
            i = 0
            c = 0
            while c == 0:
                series = bench_df[(bench_df['PROCS'] == procs[i]) & (bench_df['SIZE'] == s) & 
            (bench_df['NAME'] == b)].PAREFF / procs[i]
                c = len(series.values)
                i = i + 1 
            if p < i:
                continue
            divisor.append((series.values[0] * p) / 100)
bench_df['PAREFF'] = bench_df['PAREFF'].divide(divisor)
bench_df.to_csv('elaborated.csv',sep=';')

df = bench_df
for s in sizes:
    sns.set_style("whitegrid")
    g = sns.catplot(data=df[df['SIZE'] == s], hue='NAME', x='PROCS', y='PERFORMANCE', \
        kind='point', palette='mako')
    #g.set(yscale="log")
    scale = '[timestep/s]'
    g.set_axis_labels("MPI Processes","Performance " + scale)
    g.savefig(str(s) + 'k_test_perf_data.png')

if do_power:
    for s in sizes:
        sns.set_style("whitegrid")
        g = sns.catplot(data=df[df['SIZE'] == s], hue='NAME', x='PROCS', y='POWEREFF', \
            kind='point', palette='mako')
        #g.set(yscale="log")
        scale = '[timestep/s/Watt]'
        g.set_axis_labels("MPI Processes","Performance " + scale)
        g.savefig(str(s) + 'k_test_power_data.png')

sns.set_style("whitegrid")
g = sns.catplot(data=df, col='SIZE', hue='NAME', x='PROCS', y='PAREFF', \
    kind='point', palette='mako')
g.set(yscale="log")
scale = '[timestep/s]'
g.set_axis_labels("MPI Processes","Parallel Efficiency(%)")
g.savefig('parallel_efficiency_data.png')
