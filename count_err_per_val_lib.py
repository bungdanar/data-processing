import sys

from utils import get_err_aggr


df_aggr = get_err_aggr()

total_err = len(df_aggr)
validation_mode = '-'

if total_err > 0:
    num_of_validation = df_aggr['Validation Mode'].nunique()
    if num_of_validation > 1:
        print('Validation mode is more than 1. Your data may not correct')
        sys.exit()
    else:
        validation_mode = df_aggr['Validation Mode'].iloc[0].split('=')[1]

output_path = f'output/aggr_err.xlsx'
df_aggr.to_excel(output_path, index=False)

print({
    'Validation mode': validation_mode,
    'Total errors': total_err,
})
