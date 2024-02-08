import os
from pprint import pprint
import pandas as pd

from utils import clean_and_remove_duplicates


dir_path = 'err_data'

all_files = [file for file in os.listdir(dir_path)]

for file in all_files:
    file_path = os.path.join(dir_path, file)
    df = pd.read_csv(file_path, sep='#', names=[
                     'Log Level', 'Method', 'Path', 'Status Code', 'Validation Mode', 'Err Message'])
    df = clean_and_remove_duplicates(df)

    validation_mode = '-'
    if len(df):
        validation_mode = df['Validation Mode'].iloc[0].split('=')[1]

    pprint({
        'Filename': file,
        'Validation mode': validation_mode,
        'Total err endpoints': df['Path'].nunique(),
        'Total errors': len(df),
    })
