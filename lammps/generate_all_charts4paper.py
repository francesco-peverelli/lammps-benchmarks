import os
import perf_charts4paper
import prof.mpi_charts4paper
import prof.aggregate_mpi_data
import prof.parse_task_breakdown
import prof.task_charts4paper

benchmarks = ['rhodo', 'rhodo-single', 'rhodo-double']
sizes = [32, 256, 864, 2048]
procs = [1, 2, 4, 8, 16, 32, 64]
do_power = False
experiment_name = 'rhodo_precision'
    
perf_charts4paper.main(benchmarks, sizes, procs, do_power)

os.chdir('./prof')

prof.aggregate_mpi_data.main(experiment_name)
prof.mpi_charts4paper.main(experiment_name + '.csv', experiment_name)
prof.parse_task_breakdown.main(benchmarks, procs, sizes, experiment_name + '_tasks')
prof.task_charts4paper.main(experiment_name + '_tasks.csv', experiment_name + '_tasks')