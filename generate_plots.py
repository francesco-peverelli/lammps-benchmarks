# This script is used to generate plots from the different benchmark runs

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import re
import os
import statistics

colors = ['#c7e9b4', '#7fcdbb', '#41b6c4', '#1d91c0', '#225ea8', '#228ea8']

parser = argparse.ArgumentParser(
    description="Plot different recorded metrics for a set of benchmark runs")

parser.add_argument('--x', dest='x_list', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy x-axes as BENCH_NAME:"TAG_REGEX"')
parser.add_argument('--y', dest='y_metric', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy which metric to plot on the y axis')
parser.add_argument('--y-name', dest='y_name', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy which name to give to the y axis')
parser.add_argument('--x-name', dest='x_name', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy which name to give to the x axis')
parser.add_argument('--x-label-pos', dest='x_label_pos', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy the position in the regex, separated by\
 \'_\', where the x axis label values should be taken from, e.g. 1:2')
parser.add_argument('--name', dest='graph_name', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy the final graph name')
parser.add_argument('--format', dest='format', type=str, default='svg',
help='[OPTIONAL]\tAllows to specify the plot format (e.g. svg,pdf)')
parser.add_argument('--bench-names', dest='bench_names', type=str,
help='[OPTIONAL]\tAllows to specify alternative names for the benchmarks, e.g. NAME1:NAME2')
parser.add_argument('--x-argsort', dest='x_sort', type=bool,
help='[OPTIONAL]\tIf set to 1, sorts data accorfing to the sorting of the x axis variable')
parser.add_argument('--y-mean', dest='y_mean', type=bool,
help='[OPTIONAL]\tIf set to 1, averages y values for data with the same tag')
args = parser.parse_args()

x_split = args.x_list.split(',')
bench = [el.split(':')[0] for el in x_split]
tag_string = [el.split(':')[1] for el in x_split]
label_pos = args.x_label_pos.split(':')
label_pos = [int(x) for x in label_pos]
print(label_pos)
print(tag_string)
assert(len(label_pos) == len(tag_string))

x_ticklabels = []
y_axes = []
for b,t,pos in zip(bench,tag_string,label_pos):
    csv_path = os.getcwd() + '/' + b + '/runs.csv'
    runs_df = pd.read_csv(csv_path)
    regex = re.compile(t)
    x_vals = []
    y_vals = []
    seen_tags = set()
    tag_vals = {}
    for tag,i in zip(runs_df['TAG'],runs_df.index):
        if args.y_mean:
            if regex.match(tag):
                if tag not in tag_vals:
                    tag_vals[tag] = []
                    x_vals.append((runs_df.iloc[i]['TAG']).split('_')[pos][:-1])
                if args.y_metric == "PPW":
                    # Compute performance per Watt on the fly
                    ppw = float(runs_df.iloc[i]['PERFORMANCE']) / float(runs_df.iloc[i]['POWER'])
                    tag_vals[tag].append(ppw)
                else:
                    tag_vals[tag].append(runs_df.iloc[i][args.y_metric])
            
        else:
            if regex.match(tag):
                if tag in seen_tags:
                    # TODO: implement averaging here
                    continue
                x_vals.append((runs_df.iloc[i]['TAG']).split('_')[pos][:-1])
                if args.y_metric == "PPW":
                    # Compute performance per Watt on the fly
                    ppw = float(runs_df.iloc[i]['PERFORMANCE']) / float(runs_df.iloc[i]['POWER'])
                    y_vals.append(ppw)
                else:
                    y_vals.append(runs_df.iloc[i][args.y_metric])
                seen_tags.add(tag)
    # Compute per-tag mean
    if args.y_mean:
        for key in tag_vals:
            y_vals.append(statistics.mean(tag_vals[key]))
    
    y_axes.append(y_vals)
    x_ticklabels.append(x_vals)

fig, ax1 = plt.subplots(figsize=(8,8))
for y_axis, x_labels,i in zip(y_axes,x_ticklabels,np.arange(len(y_axes))):
    x_axis = np.arange(0,len(x_labels))
    if args.x_sort is not None:
        int_x_labels = [int(l) for l in x_labels] 
        x_index = np.array(int_x_labels).argsort()
        y_axis = list(np.array(y_axis)[x_index])
        x_labels = list(np.array(x_labels)[x_index])
    print(x_axis)
    print(y_axis)
    print(x_labels)
    ax1.plot(x_axis,y_axis, marker='.', color=colors[i])
    ax1.set_xticks(x_axis)
    ax1.set_xticklabels(x_labels)

ax1.set_xlabel(args.x_name)
ax1.set_ylabel(args.y_name)
ax1.grid(visible=True, which='major', linestyle='dotted')
if args.bench_names is not None:
    names_list = args.bench_names.split(':')
    ax1.legend(labels=names_list)
else:
    ax1.legend(labels=bench)
fig.savefig(os.getcwd() + '/plots/' + args.graph_name + '.' + args.format, \
    format=args.format, bbox_inches='tight', dpi=1200)
