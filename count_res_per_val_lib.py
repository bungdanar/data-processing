import os
import sys

import pandas as pd


dir_path = 'res_data'

all_files = [file for file in os.listdir(dir_path)]

df_list: list[pd.DataFrame] = []
for file in all_files:
    file_path = os.path.join(dir_path, file)
    df = pd.read_csv(file_path, sep=' ', names=[
        'Log Level', 'Method', 'Path', 'Status Code', 'Response Time', 'Validation Mode'])
    df_list.append(df)

df_aggr = pd.concat(df_list, ignore_index=True)

num_of_validation = df_aggr['Validation Mode'].nunique()
if num_of_validation > 1:
    print('Validation mode is more than 1. Your data may not correct')
    sys.exit()

validation_mode = df_aggr['Validation Mode'].iloc[0].split('=')[1]

df_res = df_aggr['Response Time']
df_res = df_res.apply(lambda r: float(r.rstrip('ms')))

print({
    'Validation mode': validation_mode,
    'Avg response time (ms)': df_res.mean()
})
