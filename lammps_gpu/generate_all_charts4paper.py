import os
import perf_charts4paper
import prof.cuda_charts4paper
import prof.parse_task_breakdown
import prof.task_charts4paper
import prof.aggregate_gpu_data

# benchmarks = ['chain','chain-single','chain-double']
benchmarks = ['rhodo', 'lj']

fig_extns='.pdf'

sizes = [32, 256, 864, 2048]
procs = [1, 2, 4, 6, 8]
do_power = False
experiment_name = 'gpu_bench'
# experiment_name = 'chain_precision'
    
perf_charts4paper.main(benchmarks, sizes, procs, do_power, experiment_name,fig_extns)

os.chdir('./prof')

prof.aggregate_gpu_data.main(benchmarks, procs, sizes, experiment_name + '_gpu')
prof.cuda_charts4paper.main(experiment_name + '_gpu.csv', experiment_name + '_gpu',fig_extns)
prof.parse_task_breakdown.main(benchmarks, procs, sizes, experiment_name + '_tasks')
prof.task_charts4paper.main(experiment_name + '_tasks.csv', experiment_name + '_tasks',fig_extns)
