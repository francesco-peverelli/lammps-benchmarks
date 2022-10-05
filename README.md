# LAMMPS Benchmarks [![DOI](https://zenodo.org/badge/537037512.svg)](https://zenodo.org/badge/latestdoi/537037512)

# Dependencies

- Requires CUDA >= 11.4 to run GPU experiments
- Requires the `powerstat` CPU profiling tool
- Requires the `nvidia-smi` and `NVIDIA Nsight Systems` utilities
- Requires `python 3`, and the `pandas` and `seaborn` python packages

# Important assumptions

This tool assumes that your LAMMPS software is located at `../lammps` relative to this repository. If your LAMMPS/ input files are in a different location, modify the run and profiling scripts accordingly. 

# How To Use

In this repo we collect results of different benchmarks and software on a range of architectures. 
A collection of `run_<RUN TYPE>.sh` and `run_<RUN TYPE>.py` scripts are available to run different experiment setups on CPU and GPU.
A collection of `profile_<RUN TYPE>.sh` and `profile_<RUN TYPE>.py` are available to manage profiling runs. These scripts are intended to be modified by the user to set up the desired experiments,

The `lammps` and `lammps_gpu` directories will contain the run results of the performance measurement experiments. If the content of the `runs.csv` file within this directory does not match the repo state, other utilities such as graph generation may not work properely.

`run_wrapper.py` is used internally to run the benchmarks with the following options

```
usage: run_wrapper.py [-h] --cmd CMD_STRING --bench BENCH_NAME --tag RUN_TAG
                      [--arch ARCH_INFO] [--dir DIR] [--gpu-power GPU_POWER]
                      [--cpu-power CPU_POWER] [--gpu-threshold GPU_THRESHOLD]
                      [--cpu-threshold CPU_THRESHOLD]

Run a benchmark program and record standard output and additional information

optional arguments:
  -h, --help            show this help message and exit
  --cmd CMD_STRING      [REQUIRED] Command used to run the benchmark, will be
                        recorded for reference
  --bench BENCH_NAME    [REQUIRED] Benchmark name. Is used to create a
                        subdirectory of the same name to store results
  --tag RUN_TAG         [REQUIRED] Shorthand for the name of the run. Is used
                        to plot graphs, so keep it short but meaningful
  --arch ARCH_INFO      [OPTIONAL] Allows to specify details on the
                        architecture. By default is the output of lscpu
  --dir DIR             [OPTIONAL] Allows to specify the directory where the
                        benchmark should be run, this script's directory by
                        default
  --gpu-power GPU_POWER
                        [OPTIONAL] Allows to monitor gpu power draw (requires
                        nvidia-smi)
  --cpu-power CPU_POWER
                        [OPTIONAL] Allows to monitor gpu power draw (requires
                        powerstat)
  --gpu-threshold GPU_THRESHOLD
                        [OPTIONAL] Allows to set a minimum threshold (Watt)
                        for GPU power average
  --cpu-threshold CPU_THRESHOLD
                        [OPTIONAL] Allows to set a minimum threshold (Watt)
                        for CPU power average
```

`erase_run.py` is used to erase data from a run while maintaining a consistent repo state:

```
usage: erase_run.py [-h] --timestamp TIMESTAMP --bench BENCH_NAME

Erase a benchmark run and keep the repo state clean and consistent

optional arguments:
  -h, --help            show this help message and exit
  --timestamp TIMESTAMP
                        [REQUIRED] Indexes the run to erase
  --bench BENCH_NAME    [REQUIRED] Speifies the benchmark for the run to erase
```

`generate_plots.py` is used to generate the graphs in /plots:

```
usage: generate_plots.py [-h] --x X_LIST --y Y_METRIC --y-name Y_NAME --x-name
                         X_NAME --x-label-pos X_LABEL_POS --name GRAPH_NAME
                         [--format FORMAT] [--bench-names BENCH_NAMES]
                         [--x-argsort X_SORT] [--y-mean Y_MEAN]

Plot different recorded metrics for a set of benchmark runs

optional arguments:
  -h, --help            show this help message and exit
  --x X_LIST            [REQUIRED] Command used to speciy x-axes as
                        BENCH_NAME:"TAG_REGEX"
  --y Y_METRIC          [REQUIRED] Command used to speciy which metric to plot
                        on the y axis
  --y-name Y_NAME       [REQUIRED] Command used to speciy which name to give
                        to the y axis
  --x-name X_NAME       [REQUIRED] Command used to speciy which name to give
                        to the x axis
  --x-label-pos X_LABEL_POS
                        [REQUIRED] Command used to speciy the position in the
                        regex, separated by '_', where the x axis label values
                        should be taken from, e.g. 1:2
  --name GRAPH_NAME     [REQUIRED] Command used to speciy the final graph name
  --format FORMAT       [OPTIONAL] Allows to specify the plot format (e.g.
                        svg,pdf)
  --bench-names BENCH_NAMES
                        [OPTIONAL] Allows to specify alternative names for the
                        benchmarks, e.g. NAME1:NAME2
  --x-argsort X_SORT    [OPTIONAL] If set to 1, sorts data accorfing to the
                        sorting of the x axis variable
  --y-mean Y_MEAN       [OPTIONAL] If set to 1, averages y values for data
                        with the same tag
```

# Generating Graphs

Each benchmark subdirectory contains a `generate_all_charts4paper.py`, used to generate figures based on the experiments run. Benchmark and experiments naming used when running the experiments must match with the benchmarks used in this script to generate the images. Not all available graphs are generated by default, at present, the user needs to manually uncomment the corresponding lines in the script.
