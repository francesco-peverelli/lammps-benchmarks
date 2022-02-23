# This script is used to generate barcharts from the different benchmark runs

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
help='[REQUIRED]\tCommand used to speciy x-axes as BENCH_NAME:TAG')
parser.add_argument('--y', dest='y_metric', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy which metric to plot on the y axis')
parser.add_argument('--y-name', dest='y_name', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy which name to give to the y axis')
parser.add_argument('--x-name', dest='x_name', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy which name to give to the x axis')
parser.add_argument('--x-labels', dest='x_labels', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy the bars labels')
parser.add_argument('--name', dest='graph_name', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy the final graph name')
parser.add_argument('--format', dest='format', type=str, default='svg',
help='[OPTIONAL]\tAllows to specify the plot format (e.g. svg,pdf)')
parser.add_argument('--y-mean', dest='y_mean', type=bool,
help='[OPTIONAL]\tIf set to 1, averages y values for data with the same tag')
args = parser.parse_args()

x_split = args.x_list.split(',')
bench = [el.split(':')[0] for el in x_split]
tag_string = [el.split(':')[1] for el in x_split]
x_labels = args.x_labels.split(':')

x_ticklabels = []
y_axis = []
for b,t in zip(bench,tag_string):
    csv_path = os.getcwd() + '/' + b + '/runs.csv'
    runs_df = pd.read_csv(csv_path)
    x_vals = []
    y_val = 0
    seen_tags = set()
    tag_vals = {}
    for tag,i in zip(runs_df['TAG'],runs_df.index):
        if args.y_mean:
            if t == tag:
                if tag not in tag_vals:
                    tag_vals[tag] = []
                if args.y_metric == "PPW":
                    # Compute performance per Watt on the fly
                    ppw = float(runs_df.iloc[i]['PERFORMANCE']) / float(runs_df.iloc[i]['POWER'])
                    tag_vals[tag].append(ppw)
                else:
                    tag_vals[tag].append(runs_df.iloc[i][args.y_metric])
            
        else:
            if t == tag:
                if tag in seen_tags:
                    # TODO: implement averaging here
                    continue
                if args.y_metric == "PPW":
                    # Compute performance per Watt on the fly
                    ppw = float(runs_df.iloc[i]['PERFORMANCE']) / float(runs_df.iloc[i]['POWER'])
                    y_val = ppw
                else:
                    y_val = runs_df.iloc[i][args.y_metric]
                seen_tags.add(tag)
    # Compute per-tag mean
    if args.y_mean:
        for key in tag_vals:
            y_val = statistics.mean(tag_vals[key])
    
    y_axis.append(y_val)

x = np.arange(len(x_labels))
fig,ax = plt.subplots()
width = 0.5
print(x)
print(y_axis)
ax.bar(x, y_axis, width=width)
ax.set_ylabel(args.y_name)
ax.set_xlabel(args.x_name)
ax.set_xticks(x, x_labels)
ax.grid(visible=True, which='major', linestyle='dotted')
fig.tight_layout()

fig.savefig(os.getcwd() + '/plots/' + args.graph_name + '.' + args.format, \
    format=args.format, bbox_inches='tight', dpi=1200)