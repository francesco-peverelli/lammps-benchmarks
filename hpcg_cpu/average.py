import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import re
import os
import statistics

csv_path = os.getcwd() + '/runs.csv'
runs_df = pd.read_csv(csv_path)