# Used to plot power consumption during benchmark execution

from sqlite3 import Timestamp
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import os
import metric_parsers
import scipy.integrate as it

colors = ['#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0', '#225ea8', '#228ea8', '#258ea8', '#278ea8']

parser = argparse.ArgumentParser(
    description="Plot power over time of benchmark runs")

parser.add_argument('--type', dest='type', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy the device to consider [CPU|GPU]')
parser.add_argument('--timestamp', dest='timestamp', type=str, required=True,
help='[REQUIRED]\tIndexes the run to plot')
parser.add_argument('--bench', dest='bench_name', type=str, required=True,
help='[REQUIRED]\tBenchmark name')

args = parser.parse_args()
y_values = []
maxw = 0
if args.type == 'CPU':
    file = os.getcwd() + '/' + args.bench_name + '/' + args.timestamp + '_powerstat.txt'
    power_list = metric_parsers.parse_powerstat_power(file)
    x = np.arange(len(power_list))
    y_values.append(power_list)
    max_watts = max([float(x) for x in power_list])
    if max_watts > maxw:
        maxw = max_watts
else:
    file = os.getcwd() + '/' + args.bench_name + '/' + args.timestamp + '_nv-smi.txt'
    power_dict = metric_parsers.parse_nvidia_smi_power(file)
    maxl = 0
    for key in power_dict:
        newl = len(power_dict[key])
        if maxl < newl:
            maxl = newl
        y_values.append(power_dict[key])
        max_watts = max([float(x) for x in power_dict[key]])
        if max_watts > maxw:
            maxw = max_watts
    x = np.arange(maxl)
    
fig, ax1 = plt.subplots(figsize=(48,20))

for y,i in zip(y_values,np.arange(len(y_values))):
    y = [float(v) for v in y]
    ax1.plot(x,y, marker='.', color=colors[i])
    print(it.cumtrapz(y,x=x)[-1])

ax1.set_yticks(np.linspace(0,maxw,num=20))
fig.savefig(os.getcwd() + '/plots/' + args.timestamp + '_' + args.bench_name + '_' + args.type + '.svg', \
    format='svg', bbox_inches='tight', dpi=1200)
