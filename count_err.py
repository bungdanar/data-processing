import pandas as pd

from utils import clean_and_remove_duplicates


err_df = pd.read_csv('err_data/err500.log', sep='#', names=[
                     'Log Level', 'Method', 'Path', 'Status Code', 'Validation Mode', 'Err Message'])

res_time_df = pd.read_csv('err_data/res-time.log', sep=' ', names=[
    'Log Level', 'Method', 'Path', 'Status Code', 'Response Time', 'Validation Mode'])

err_df = clean_and_remove_duplicates(err_df)

print({
    'Validation mode': res_time_df['Validation Mode'].iloc[0].split('=')[1],
    'Total endpoint coverage': res_time_df['Path'].nunique(),
    'Total err endpoints': err_df['Path'].nunique(),
    'Total errors': len(err_df),
})
