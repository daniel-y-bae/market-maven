import os

import numpy as np
import pandas as pd

np.set_printoptions(formatter={'all':lambda x: str(x)})
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df = pd.read_csv('metrics_v.csv')