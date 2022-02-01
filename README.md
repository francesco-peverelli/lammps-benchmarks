# Spatial Arch Benchmarks

In this repo we collect results of different benchmarks and software on a range of architectures. `run_wrapper.py` is used to run a benchmark:

```
usage: run_wrapper.py [-h] --cmd CMD_STRING --bench BENCH_NAME --tag RUN_TAG
                      [--arch ARCH_INFO] [--dir DIR]

Run a benchmark program and record standard output and additional information

optional arguments:
  -h, --help          show this help message and exit
  --cmd CMD_STRING    [REQUIRED] Command used to run the benchmark, will be
                      recorded for reference
  --bench BENCH_NAME  [REQUIRED] Benchmark name. Is used to create a
                      subdirectory of the same name to store results
  --tag RUN_TAG       [REQUIRED] Shorthand for the name of the run. Is used to
                      plot graphs, so keep it short but meaningful
  --arch ARCH_INFO    [OPTIONAL] Allows to specify details on the
                      architecture. By default is the output of lscpu
  --dir DIR           [OPTIONAL] Allows to specify the directory where the
                      benchmark should be run, this script's directory by
                      default
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
