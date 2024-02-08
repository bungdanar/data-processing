import os
from pprint import pprint

import pandas as pd


dir_path = 'res_data'

all_files = [file for file in os.listdir(dir_path)]

for file in all_files:
    file_path = os.path.join(dir_path, file)
    df = pd.read_csv(file_path, sep=' ', names=[
        'Log Level', 'Method', 'Path', 'Status Code', 'Response Time', 'Validation Mode'])

    pprint({
        'Filename': file,
        'Validation mode': df['Validation Mode'].iloc[0].split('=')[1],
        'Total request': len(df),
        'Total endpoint coverage': df['Path'].nunique()
    })
