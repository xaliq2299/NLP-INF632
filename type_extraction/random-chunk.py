import pandas as pd
import numpy as np

data = pd.read_csv('results.tsv', sep='\t')
for i in range(20):
	ind = np.random.randint(data.shape[0])
	print(data.loc[[ind]])
