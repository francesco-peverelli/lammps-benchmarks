
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

def main(benchmarks, sizes, procs, do_power):

    benchmarks = sorted(benchmarks)
    sizes = sorted(sizes)
    procs = sorted(procs)

    bench_ts = { 'rhodo' : 2, 'lj' : 0.005, 'eam' : 0.005, 'chain' : 0.012}
    bench_units = { 'rhodo' : 'real', 'lj' : 'lj', 'eam' : 'metal', 'chain' : 'lj'}

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
    first = True
    for b in benchmarks:
        tmp = bench_df[[b in benchmarks for x in bench_df['TAG']]]
        if first:
            bench_df = tmp
            first = False
        else:
            pd.concat([bench_df, tmp])

    for s in sizes:
        bench_df['TAG'] = bench_df['TAG'].apply(lambda x: x.replace('scaled_' + str(s) + '_','scaled_'))
        bench_df['TAG'] = bench_df['TAG'].apply(lambda x: x.replace('scaled_' + str(s) + '-','scaled-'))
    if do_power:
        bench_df = bench_df[bench_df['POWER'].isnull() == 0]
    #bench_df = bench_df[['1ont' in x for x in bench_df['TAG']]]
    bench_df = bench_df.groupby('TAG',as_index=False).mean()
    bench_df[['NAME','GPU','MPI','SIZE']] = bench_df['TAG'].str.split('_', expand=True)
    bench_df.drop('TAG', inplace=True, axis=1)
    #bench_df.drop('THRESHOLD', inplace=True, axis=1)
    #bench_df.drop('ONT', inplace=True, axis=1)
    bench_df['SIZE'] = bench_df['SIZE'].apply(lambda x: 2048 if x == '2M' else int(x.replace('k','')))
    bench_df['GPU'] = bench_df['GPU'].apply(lambda x: int(x.replace('g','')))
    bench_df['MPI'] = bench_df['MPI'].apply(lambda x: int(x.replace('n','')))
    bench_df['NAME'] = bench_df['NAME'].apply(lambda x: x.replace('.scaled','').replace('in.','').replace('.test',''))

    # Convert all to timesteps/s
    bench_df['PERFORMANCE'] = bench_df.apply(lambda x: convert_to_tss(x.PERFORMANCE, bench_units[x.NAME.split('-')[0]],bench_ts[x.NAME.split('-')[0]]), axis=1)

    if do_power:
        bench_df['POWEREFF'] = bench_df['PERFORMANCE'] / bench_df['POWER']
    bench_df = bench_df[bench_df['GPU'] <= 64]
    bench_df['PAREFF'] = bench_df['PERFORMANCE']
    bench_df = bench_df.sort_values(['NAME','SIZE','GPU'])

    bench_df = bench_df[[x in benchmarks for x in bench_df['NAME']]] 

    # Compute parallel efficiency column
    divisor = []
    base_p_nums = []
    for b in benchmarks:
        max_min_p = 0
        for s in sizes:
            min_p = np.Inf
            for p in procs:
                series = bench_df[(bench_df['GPU'] == p) & (bench_df['SIZE'] == s) & 
                    (bench_df['NAME'] == b)]
                if (min_p > p) and (len(series) > 0):
                    min_p = p
            if max_min_p < min_p:
                max_min_p = min_p
        base_p_nums.append(max_min_p)

    s_index = 0
    for b in benchmarks:
        for s in sizes:
            for p in procs:
                if p < base_p_nums[s_index]:
                    bench_df.loc[(bench_df['GPU'] == p) & (bench_df['SIZE'] == s) & (bench_df['NAME'] == b),'PAREFF'] = np.NAN
                else:
                    perf = bench_df[(bench_df['GPU'] == p) & (bench_df['SIZE'] == s) & (bench_df['NAME'] == b)].PAREFF
                    perf_0 = bench_df[(bench_df['GPU'] == base_p_nums[s_index]) & (bench_df['SIZE'] == s) & (bench_df['NAME'] == b)].PERFORMANCE
                    div = (p / base_p_nums[s_index]) * perf_0
                    bench_df.loc[(bench_df['GPU'] == p) & (bench_df['SIZE'] == s) & (bench_df['NAME'] == b),'PAREFF'] = (float(perf) / float(div)) * 100.0    
        s_index = s_index + 1

    bench_df = bench_df[bench_df['PAREFF'].isnull() == 0]
    bench_df.to_csv('elaborated.csv',sep=';')

    df = bench_df
    for s in sizes:
        sns.set_style("whitegrid")
        g = sns.catplot(data=df[df['SIZE'] == s], hue='NAME', x='GPU', y='PERFORMANCE', \
            kind='point', palette='mako')
        #g.set(yscale="log")
        scale = '[timestep/s]'
        g.set_axis_labels("GPU devices","Performance " + scale)
        g.savefig(str(s) + 'k_test_perf_data.png')

    if do_power:
        for s in sizes:
            sns.set_style("whitegrid")
            g = sns.catplot(data=df[df['SIZE'] == s], hue='NAME', x='GPU', y='POWEREFF', \
                kind='point', palette='mako')
            #g.set(yscale="log")
            scale = '[timestep/s/Watt]'
            g.set_axis_labels("GPU devices","Performance " + scale)
            g.savefig(str(s) + 'k_test_power_data.png')

    sns.set_style("whitegrid")
    g = sns.catplot(data=df, col='SIZE', hue='NAME', x='GPU', y='PAREFF', \
        kind='point', palette='mako')
    g.set(yscale="log")
    scale = '[timestep/s]'
    g.set_axis_labels("GPU devices","Parallel Efficiency(%)")
    g.savefig('parallel_efficiency_data.png')
