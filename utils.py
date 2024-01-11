import os
import pandas as pd


__regex_and_replacement_list = [
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
    },
    {
        'regex': r'Value .*? is not None, True, or False',
        'replacement': 'Value is not None, True, or False'
    },
    {
        'regex': r"MySQL server version for the right syntax to use near '\)(.*?)at line 1\"\)$",
        'replacement': "MySQL server version for the right syntax to use near"
    }
]


def __remove_duplicates(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return df.drop_duplicates(
        subset=columns).reset_index(drop=True)


def clean_and_remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    # Remove duplicates by Path and Err Message
    df = __remove_duplicates(df, ['Path', 'Err Message'])

    # Clean Err Message from input/parameter
    for re_and_replace in __regex_and_replacement_list:
        df['Err Message'] = df['Err Message'].str.replace(
            re_and_replace['regex'], re_and_replace['replacement'], regex=True)

    # Remove duplicates by Path and Err Message (again)
    df = __remove_duplicates(df, ['Path', 'Err Message'])

    return df


def get_err_aggr() -> pd.DataFrame:
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

    return df_aggr
