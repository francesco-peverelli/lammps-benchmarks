# Allows to erase a run from a benchmark

import argparse
import os
import pandas as pd

parser = argparse.ArgumentParser(
    description="Erase a benchmark run and keep the repo state clean and consistent")

parser.add_argument('--timestamp', dest='timestamp', type=str, required=True,
help='[REQUIRED]\tIndexes the run to erase')
parser.add_argument('--bench', dest='bench_name', type=str, required=True,
help='[REQUIRED]\tSpeifies the benchmark for the run to erase')
args = parser.parse_args()

cwd = os.getcwd()
bench_dir = cwd + '/' + args.bench_name
csv_path = bench_dir + '/runs.csv'
out_res_file = bench_dir + '/' + args.timestamp + '_out.txt'
out_arch_file = bench_dir + '/' + args.timestamp + '_arch.txt'

if not os.path.exists(bench_dir):
    print("No such benchmark, terminating...")
    exit(0)
if not os.path.exists(csv_path):
    print("No runs file inside benchmark folder, terminating...")
    exit(0)

runs_data = pd.read_csv(csv_path, index_col='TIMESTAMP')
print(runs_data)
if (runs_data.index == args.timestamp).any():
    runs_data = runs_data.drop(labels=args.timestamp, axis=0)
    runs_data.to_csv(csv_path)
    os.remove(out_res_file)
    os.remove(out_arch_file)
    print("Run " + args.timestamp + " was succesfully deleted!")
else:
    print("No such timestamp, terminating...")
