import os
import sys
import pandas as pd

base_regex = sys.argv[1]
benchmark = sys.argv[2]

os.system("cat " + benchmark + "/runs.csv | grep -E \"(" + base_regex + ")|TIMESTAMP\" > to_erase.csv")

data = pd.read_csv("to_erase.csv")

print(data)

for index, row in data.iterrows():
    os.system("python3 erase_run.py --timestamp " + row['TIMESTAMP'] + " --bench " + row['BENCH'])

os.system("rm to_erase.csv")
