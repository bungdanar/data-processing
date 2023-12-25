import pandas as pd


err_df = pd.read_csv('data/err500.log', sep='#', names=[
                     'Log Level', 'Method', 'Path', 'Status Code', 'Validation Mode', 'Err Message'])

res_time_df = pd.read_csv('data/res-time.log', sep=' ', names=[
    'Log Level', 'Method', 'Path', 'Status Code', 'Response Time', 'Validation Mode'])

# Remove duplicates by Path and Err Message
err_df = err_df.drop_duplicates(
    subset=['Path', 'Err Message']).reset_index(drop=True)

# Clean Err Message from input/parameter
regex_and_replacement_list = [
    {
        'regex': r'value:(.*?)(\sfor column)',
        'replacement': 'value:for column'
    },
    {
        'regex': r'msg=(.*?)(\sis an invalid keyword argument)',
        'replacement': 'msg=is an invalid keyword argument'
    },
    {
        'regex': r'boolean value:(.*?)$',
        'replacement': 'boolean value:'
    }
]

for re_and_replace in regex_and_replacement_list:
    err_df['Err Message'] = err_df['Err Message'].str.replace(
        re_and_replace['regex'], re_and_replace['replacement'], regex=True)

# Remove duplicates by Path and Err Message
err_df = err_df.drop_duplicates(
    subset=['Path', 'Err Message']).reset_index(drop=True)

print({
    'Validation mode': res_time_df['Validation Mode'].iloc[0].split('=')[1],
    'Total endpoint coverage': res_time_df['Path'].nunique(),
    'Total err endpoints': err_df['Path'].nunique(),
    'Total errors': len(err_df),
})
