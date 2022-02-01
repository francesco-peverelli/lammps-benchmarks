# This script defines custom parsers to extract performance metrics from raw output

import pandas as pd
import re

# Testing parser for hello toy benchmark
def hello_parser(runs_data, out_file, timestamp):
    try:
        outf = open(out_file, mode='r')
        data = outf.read()
        z = re.search(r'(\d+ GFLOPs)|(\d+\.\d+ GFLOPs)', str(data))
        perf = re.search(r'(\d)|(\d+\.\d)', z.group()).group()
        runs_data.loc[timestamp,'PERFORMANCE'] = perf
    finally:
        outf.close()

    return runs_data

# Try matching the benchmark to a performance metric parser
def update_performance_metric(timestamp, benchmark, out_dir):
    csv_path = out_dir + '/runs.csv'
    out_file = out_dir + '/' + timestamp + '_out.txt'

    runs_data = pd.read_csv(csv_path, index_col='TIMESTAMP')

    if benchmark == 'hello':
        updated_data = hello_parser(runs_data, out_file, timestamp)
    else:
        print('*** No parser found for ' + benchmark + ', skipping performance recording  ***')

    runs_data.to_csv(csv_path)