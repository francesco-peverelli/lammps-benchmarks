# This script is used to generate plots from the different benchmark runs

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import re

parser = argparse.ArgumentParser(
    description="Plot different recorded metrics for a set of benchmark runs")

parser.add_argument('--x', dest='x_list', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy x-axes as BENCH_NAME:TAG_REGEX')
parser.add_argument('--y', dest='y_metric', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy which metric to plot on the y axis')
parser.add_argument('--name', dest='graph_name', type=str, required=True,
help='[REQUIRED]\tCommand used to speciy the final graph name')
parser.add_argument('--format', dest='format', type=str, default='svg',
help='[OPTIONAL]\tAllows to specify the plot format (e.g. svg,pdf)')

args = parser.parse_args()

x_split = args.x_list.split(',')
bench = [el.split(':')[0] for el in x_split]
tag_string = [el.split(':')[0] for el in x_split]