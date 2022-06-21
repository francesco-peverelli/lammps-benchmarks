import os
import perf_charts4paper
import prof.mpi_charts4paper
import prof.aggregate_mpi_data
import prof.parse_task_breakdown
import prof.task_charts4paper

#bench kind

#bench_units = { 'rhodo', 'lj', 'eam', 'chain', 'chute'}
benchmarks = ['rhodo', 'rhodo-single', 'rhodo-double']
#atom #
sizes = [32, 256, 864, 2048]
#proc MPI
procs = [1, 2, 4, 8, 16, 32, 64]
#for now falzo
do_power = False
#collection bench name
experiment_name = 'rhodo_precision'

#TODO give the experiment name for this
#perf, // efficiency
perf_charts4paper.main(benchmarks, sizes, procs, do_power, experiment_name)

os.chdir('./prof')

prof.aggregate_mpi_data.main(experiment_name, benchmarks, procs, sizes)
prof.mpi_charts4paper.main(experiment_name + '.csv', experiment_name)
prof.parse_task_breakdown.main(benchmarks, procs, sizes, experiment_name + '_tasks')
prof.task_charts4paper.main(experiment_name + '_tasks.csv', experiment_name + '_tasks')
