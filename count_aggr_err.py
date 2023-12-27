import os
import sys

import pandas as pd

from utils import clean_and_remove_duplicates


dir_path = 'aggr_err_data'

all_files = [file for file in os.listdir(dir_path)]

df_list: list[pd.DataFrame] = []
for file in all_files:
    file_path = os.path.join(dir_path, file)
    df = pd.read_csv(file_path, sep='#', names=[
                     'Log Level', 'Method', 'Path', 'Status Code', 'Validation Mode', 'Err Message'])
    df_list.append(df)

df_aggr = pd.concat(df_list, ignore_index=True)
df_aggr = clean_and_remove_duplicates(df_aggr)

total_err = len(df_aggr)
validation_mode = '-'

if total_err > 0:
    num_of_validation = df_aggr['Validation Mode'].nunique()
    if num_of_validation > 1:
        print('Validation mode is more than 1. Your data may not correct')
        sys.exit()
    else:
        validation_mode = df_aggr['Validation Mode'].iloc[0].split('=')[1]

print({
    'Validation mode': validation_mode,
    'Total errors': total_err
})
