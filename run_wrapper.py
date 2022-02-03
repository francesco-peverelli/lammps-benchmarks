# This script is used as a wrapper to run the benchmark program and collect additional information for each run. 
# The script assumes that the program does not require to use standard input and error. 

import argparse
import os
import io
import time
import subprocess
import metric_parsers
from datetime import datetime

parser = argparse.ArgumentParser(
    description="Run a benchmark program and record standard output and additional information")

parser.add_argument('--cmd', dest='cmd_string', type=str, required=True,
help='[REQUIRED]\tCommand used to run the benchmark, will be recorded for reference')
parser.add_argument('--bench', dest='bench_name', type=str, required=True,
help='[REQUIRED]\tBenchmark name. Is used to create a subdirectory of the same name to store results')
parser.add_argument('--tag', dest='run_tag', type=str, required=True,
help='[REQUIRED]\tShorthand for the name of the run. Is used to plot graphs, so keep it short but meaningful')
# Used to override CPU arch info (e.g. GPU/FPGA info)
parser.add_argument('--arch', dest='arch_info', type=str,
help='[OPTIONAL]\tAllows to specify details on the architecture. By default is the output of lscpu')
parser.add_argument('--dir', dest='dir', type=str,
help='[OPTIONAL]\tAllows to specify the directory where the benchmark should be run, this script\'s directory by default')
parser.add_argument('--gpu-power', dest='gpu_power',type=int,
help='[OPTIONAL]\tAllows to monitor gpu power draw (requires nvidia-smi)')
args = parser.parse_args()

timestamp = datetime.today().strftime("%d-%m-%Y") + '_' + str(datetime.now().time())

script_dir = os.getcwd()
out_dir = script_dir + '/' + args.bench_name

# Create output directory if does not exist
if not os.path.exists(out_dir):
    os.system('mkdir ' + args.bench_name)

# Move to the specified directory
if args.dir is not None:
    os.chdir(args.dir)

if args.arch_info is None:
    # Get arch info 
    strout = io.StringIO()
    proc = subprocess.Popen('lscpu', shell=True, stdout=subprocess.PIPE)
    arch_info = proc.stdout.read().decode("utf-8")
else:
    # Override custom arch info
    arch_info = args.arch_info

if args.gpu_power is not None:
    id_str = ''
    for i in range(0,args.gpu_power):
        id_str += str(i) + ','
    id_str = id_str[:-1]
    smi_proc = subprocess.Popen('nvidia-smi -i ' + id_str + ' --loop-ms=1000 --format=csv --query-gpu=power.draw,gpu_uuid > ' + out_dir + '/' + timestamp + '_nv-smi.txt', shell=True)

# Start timed portion
start_time = time.time()

# Launch benchmark
proc = subprocess.Popen(args.cmd_string, shell=True, stdout=subprocess.PIPE)
proc.wait()

# End timed portion
end_time = time.time()

result_str = proc.stdout.read().decode("utf-8")

elapsed_time = end_time - start_time

if args.gpu_power is not None:
    smi_proc.kill()

print('*** Timestamp: ' + timestamp + '\n')
print('*** Bench name: ' + args.bench_name + '\n')
print('*** Run tag: ' + args.run_tag + '\n')
print('*** Command: ' + args.cmd_string + '\n')
print('*** Elapsed time: ' + str(elapsed_time) + '\n')
print('*** Arch info:\n\n' + arch_info + '\n********\n')
print('*** Result:\n\n' + result_str + '\n********\n')

print('Writing run results on file...')

runs_file = out_dir + '/runs.csv'
out_res_file = out_dir + '/' + timestamp + '_out.txt' 
out_res_name = args.bench_name + timestamp + '_out.txt'
out_arch_file = out_dir + '/' + timestamp + '_arch.txt'
out_arch_name = args.bench_name + timestamp + '_arch.txt'

# Write runs in runs file

line = timestamp + ',' + args.bench_name + ',' + args.run_tag \
    + ',' + args.cmd_string.replace(',',';') + ',' + str(elapsed_time) + ', ' + out_res_name + ',' + out_arch_name + ',\n'
try:
    if os.path.exists(runs_file):
        f = open(runs_file, mode='a')
        f.writelines(line)
    else:
        f = open(runs_file, 'w')
        header = 'TIMESTAMP,BENCH,TAG,CMD,EXEC_TIME,RES_FILE,ARCH_FILE,PERFORMANCE\n'
        f.writelines(header)
        f.writelines(line)
finally:
    f.close()
# Write stdout for the benchmark
try:
    resf = open(out_res_file,'w')
    resf.write(result_str)
finally:
    resf.close()
# Write arch info for the benchmark
try:
    archf = open(out_arch_file,'w')
    archf.write(arch_info)
finally:
    archf.close()

# Update performace metrics
metric_parsers.update_performance_metric(timestamp, args.bench_name, out_dir)
