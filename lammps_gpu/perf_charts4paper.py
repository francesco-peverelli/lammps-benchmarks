
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

def main(benchmarks, sizes, procs, do_power, experiment_name, fig_extns):

    gpu_mpi_dict = [{1 : 6, 2 : 12, 4 : 12, 6 : 18, 8 : 24},
        {1 : 16, 2 : 28, 4 : 32, 6 : 48, 8 : 48},
        {1 : 36, 2 : 36, 4 : 36, 6 : 48, 8 : 48},
        {1 : 16, 2 : 48, 4 : 48, 6 : 48, 8 : 48}]

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
    
    #filter pairs MPI/GPUs
    s_index = 0
    for s in sizes:
        for p in procs:
            index = bench_df[(bench_df['SIZE'] == s) & (bench_df['GPU'] == p) & (bench_df['MPI'] != gpu_mpi_dict[s_index][p])].index
            print(index)
            print(str(s) + ' ' + str(p) + ' ' + str(s_index) + ' ' + str(gpu_mpi_dict[s_index][p]))
            bench_df = bench_df.drop(index)
        s_index = s_index + 1
   
    print(bench_df[bench_df['NAME'] == 'chain']) 

    # Compute parallel efficiency column
    base_p_nums = []
    for s in sizes:
        max_min_p = 0
        for b in benchmarks:
            min_p = np.Inf
            for p in procs:
                series = bench_df[(bench_df['GPU'] == p) & (bench_df['SIZE'] == s) & 
                    (bench_df['NAME'] == b)]
                if (min_p > p) and (len(series) > 0):
                    min_p = p
            if max_min_p < min_p:
                max_min_p = min_p
        base_p_nums.append(max_min_p)

    for b in benchmarks:
        s_index = 0
        for s in sizes:
            for p in procs:
                if p < base_p_nums[s_index]:
                    bench_df.loc[(bench_df['GPU'] == p) & (bench_df['MPI'] == gpu_mpi_dict[s_index][p]) & (bench_df['SIZE'] == s) & (bench_df['NAME'] == b),'PAREFF'] = np.NAN
                else:
                    perf = bench_df.loc[(bench_df['GPU'] == p) & (bench_df['MPI'] == gpu_mpi_dict[s_index][p]) & (bench_df['SIZE'] == s) & (bench_df['NAME'] == b),'PAREFF']
                    perf_0 = bench_df.loc[(bench_df['GPU'] == base_p_nums[s_index]) & (bench_df['MPI'] == gpu_mpi_dict[s_index][base_p_nums[s_index]]) & (bench_df['SIZE'] == s) & (bench_df['NAME'] == b),'PERFORMANCE']
                    div = (p / base_p_nums[s_index]) * perf_0
                    bench_df.loc[(bench_df['GPU'] == p) & (bench_df['MPI'] == gpu_mpi_dict[s_index][p]) & (bench_df['SIZE'] == s) & (bench_df['NAME'] == b),'PAREFF'] = (float(perf) / float(div)) * 100.0    
            s_index = s_index + 1

    bench_df = bench_df[bench_df['PAREFF'].isnull() == 0]
    bench_df.to_csv('elaborated.csv',sep=';')

    print(bench_df[bench_df['NAME'] == 'chain'])
    df = bench_df
    ########################eliminating for unique catplot##################
    # for s in sizes:
    #     sns.set_style("whitegrid")
    #     g = sns.catplot(data=df[df['SIZE'] == s], hue='NAME', x='PROCS', y='PERFORMANCE', \
    #         kind='point', palette='mako')
    #     #g.set(yscale="log")
    #     scale = '[timestep/s]'
    #     g.set_axis_labels("MPI Processes","Performance " + scale)
    #     g.savefig(experiment_name + str(s) + 'k_perf'+fig_extns)
    ########################end of  unique catplot##################
    
    # Reset matplotlib settings;
    plt.rcdefaults()
    # plt.rcParams["font.family"] = ["Palatino"]

    plt.rcParams.update({
      "text.usetex": True,
      "font.family": "serif",
      "font.serif": ["Palatino"],
    })
    plt.rcParams["font.size"] = 28
    plt.rcParams["xtick.labelsize"]= 28    # major tick size in points
    plt.rcParams["ytick.labelsize"]= 25    # major tick size in points
    plt.rcParams["legend.fontsize"]= 28   # major tick size in points
    plt.rcParams["legend.handletextpad"]=0.01    # major tick size in points
    # plt.rcParams["axes.titlesize"]= 10     # major tick size in points

    plt.rcParams['hatch.linewidth'] = 0.6
   
    plt.rcParams['axes.labelpad'] = 0
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    scale_points=1.75
    g = sns.catplot(data=df, col='SIZE', hue='NAME', x='GPU', y='PERFORMANCE', \
            kind='point', palette='mako', scale =scale_points, sharey=False)
    scale = '[timestep/s]'
    g.set_axis_labels("GPU devices","Performance " + scale)
    g.savefig(experiment_name + 'k_perf'+fig_extns)
    
    if do_power:
        g = sns.catplot(data=df, col='SIZE', hue='NAME', x='GPU', y='POWEREFF', \
            kind='point', palette='mako', scale =scale_points, sharey=False)
        scale = '[timestep/s/Watt]'
        g.set_axis_labels("GPU devices","Energy Efficiency " + scale)
        g.savefig(experiment_name + 'k_power'+fig_extns)
 
    print(data)
        
#    if do_power:
#        for s in sizes:
#            sns.set_style("whitegrid")
#            g = sns.catplot(data=df[df['SIZE'] == s], hue='NAME', x='GPU', y='POWEREFF', \
#                kind='point', palette='mako')
#            #g.set(yscale="log")
#            scale = '[timestep/s/Watt]'
#            g.set_axis_labels("MPI Processes","Performance " + scale)
#            g.savefig(experiment_name + str(s) + 'k_power_data' + fig_extns)

    # Reset matplotlib settings;
    plt.rcdefaults()
    # plt.rcParams["font.family"] = ["Palatino"]

    plt.rcParams.update({
      "text.usetex": True,
      "font.family": "serif",
      "font.serif": ["Palatino"],
    })
    plt.rcParams["font.size"] = 28
    plt.rcParams["xtick.labelsize"]= 28    # major tick size in points
    plt.rcParams["ytick.labelsize"]= 25    # major tick size in points
    plt.rcParams["legend.fontsize"]= 28   # major tick size in points
    plt.rcParams["legend.handletextpad"]=0.01    # major tick size in points
    # plt.rcParams["axes.titlesize"]= 10     # major tick size in points

    plt.rcParams['hatch.linewidth'] = 0.6
   
    plt.rcParams['axes.labelpad'] = 0
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    scale_points=1.75

    #Exclude the runs with no counterpart for other sizes in parallel efficiency graph
    s_idx = 0
    for s in sizes:
        df = df[(df['SIZE'] != s) | (df['GPU'] >= base_p_nums[s_idx])]
        s_idx = s_idx + 1
    sns.set_style("whitegrid", {"font.family":"Palatino"})

    g = sns.catplot(data=df, col='SIZE', hue='NAME', x='GPU', y='PAREFF', \
        kind='point', palette='mako', scale = scale_points)
    g.set(yscale="log")
    scale = '[timestep/s]'
    #g.set_xticklabels(g.get_xticklabels(), rotation=20, horizontalalignment='right')
    #g.set_yticklabels(g.get_yticklabels(),rotation=10, horizontalalignment='right')
    # ylabels = ['{:,.2f}'.format(x) + 'K' for x in g.get_xticks()/1000]
    # g.set_xticklabels(ylabels)
    g.set_axis_labels("GPU devices","Parallel Efficiency(\%)")
    # g.set_ylabels("Parallel Efficiency(%)",labelpad=-5)
    g.savefig(experiment_name+'parallel_efficiency_data'+fig_extns)
