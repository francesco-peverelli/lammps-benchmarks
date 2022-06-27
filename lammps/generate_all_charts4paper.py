import os
import perf_charts4paper
import prof.mpi_charts4paper
import prof.aggregate_mpi_data
import prof.parse_task_breakdown
import prof.task_charts4paper


fig_extns='.pdf'
#bench kind

benchmarks = ['lj', 'lj-single', 'lj-double']
#benchmarks = ['chute', 'chute-single', 'chute-double']
#atom #
sizes = [32, 256, 864, 2048]
#proc MPI
procs = [1, 2, 4, 8, 16, 32, 64]
#for now falzo
do_power = False
#collection bench name
experiment_name = 'lammps_benchs_chute_prec_'
#experiment_name = 'rhodo_precision'

#TODO give the experiment name for this
#perf, // efficiency
perf_charts4paper.main(benchmarks, sizes, procs, do_power, experiment_name, fig_extns)

os.chdir('./prof')

# prof.aggregate_mpi_data.main(experiment_name, benchmarks, procs, sizes)
# prof.mpi_charts4paper.main(experiment_name + '.csv', experiment_name, fig_extns)
# prof.parse_task_breakdown.main(benchmarks, procs, sizes, experiment_name + '_tasks')
# prof.task_charts4paper.main(experiment_name + '_tasks.csv', experiment_name + '_tasks', fig_extns)
