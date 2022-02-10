# This script is used as a wrapper to run the benchmark program and collect additional information for each run. 
# The script assumes that the program does not require to use standard input and error. 

import argparse
from audioop import avg
import os
import io
import time
import subprocess
import metric_parsers
from datetime import datetime
from statistics import mean

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
parser.add_argument('--cpu-power', dest='cpu_power',type=bool,
help='[OPTIONAL]\tAllows to monitor gpu power draw (requires powerstat)')
parser.add_argument('--gpu-threshold', dest='gpu_threshold',type=int,
help='[OPTIONAL]\tAllows to set a minimum threshold (Watt) for GPU power average')
parser.add_argument('--cpu-threshold', dest='cpu_threshold',type=int,
help='[OPTIONAL]\tAllows to set a minimum threshold (Watt) for CPU power average')

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

try:
    if args.gpu_power is not None:
        id_str = ''
        for i in range(0,args.gpu_power):
            id_str += str(i) + ','
        id_str = id_str[:-1]
        smi_proc = subprocess.Popen('nvidia-smi -i ' + id_str + ' --loop-ms=500 --format=csv --query-gpu=power.draw,gpu_uuid > ' + out_dir + '/' + timestamp + '_nv-smi.txt', shell=True)

    if args.cpu_power is not None:
        pow_proc = subprocess.Popen('sudo powerstat 0.5 7200 -R -n > ' + out_dir + '/' + timestamp + '_powerstat.txt', shell=True)

    # Start timed portion
    start_time = time.time()

    # Launch benchmark
    proc = subprocess.Popen(args.cmd_string, shell=True, stdout=subprocess.PIPE)
    proc.wait()

    # End timed portion
    end_time = time.time()

    gpu_avg = 0
    min_idx = 2e+16
    max_idx = 0
    if args.gpu_power is not None:
        smi_proc.kill()
        smi_proc.wait()
        gpu_watts = metric_parsers.parse_nvidia_smi_power(out_dir + '/' + timestamp + '_nv-smi.txt')
        if args.gpu_threshold is not None:
            th = args.gpu_threshold
        else:
            th = 90
        for key in gpu_watts:
            float_watts = [float(x) for x in gpu_watts[key]]
            filtered_idx = [idx for idx, element in enumerate(float_watts) if element > th]
            maxi = max(filtered_idx)
            mini = min(filtered_idx)
            if maxi > max_idx:
                max_idx = maxi
            if mini < min_idx:
                min_idx = mini
            gpu_avg += mean(filter(lambda v: v > th, float_watts))

    cpu_avg = 0
    if args.cpu_power is not None:
        pow_proc.kill()
        pow_proc.wait()
        while os.path.getsize(out_dir + '/' + timestamp + '_powerstat.txt') == 0:
            print("Waiting for power file to finish writing...")
            time.sleep(1)
        cpu_watts = metric_parsers.parse_powerstat_power(out_dir + '/' + timestamp + '_powerstat.txt')
        if args.gpu_power is None:
            if args.cpu_threshold is not None:
                th = args.cpu_threshold
            else:
                th = 0
            print(cpu_watts)
            print(th)
            cpu_avg = mean(filter(lambda v: v > th,[float(x) for x in cpu_watts]))
        else:
            print("Indexes are " + str(min_idx) + ' and ' + str(max_idx) + ', len is ' + str(len(cpu_watts)))
            cpu_avg = mean([float(x) for x in cpu_watts[min_idx:max_idx]])

    power_average = gpu_avg + cpu_avg
    power_str = str(power_average) if power_average > 0 else ''

    result_str = proc.stdout.read().decode("utf-8")

    elapsed_time = end_time - start_time

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
        + ',' + args.cmd_string.replace(',',';') + ',' + str(elapsed_time) \
        + ', ' + out_res_name + ',' + out_arch_name + ',,' + power_str + '\n'
    try:
        if os.path.exists(runs_file):
            f = open(runs_file, mode='a')
            f.writelines(line)
        else:
            f = open(runs_file, 'w')
            header = 'TIMESTAMP,BENCH,TAG,CMD,EXEC_TIME,RES_FILE,ARCH_FILE,PERFORMANCE,POWER\n'
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
finally:
    try:
        if smi_proc is not None:
            smi_proc.kill()
    except NameError:
        print("No smi to kill...")
    try:
        if pow_proc is not None:
            pow_proc.kill()
    except NameError:
        print("No powerstat to kill...")
    try:
        if proc is not None:
            proc.kill()
    except NameError:
        print("No app process to kill...")
