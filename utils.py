from pandas import DataFrame


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
    }
]


def __remove_duplicates(df: DataFrame, columns: list[str]) -> DataFrame:
    return df.drop_duplicates(
        subset=columns).reset_index(drop=True)


def clean_and_remove_duplicates(df: DataFrame) -> DataFrame:
    # Remove duplicates by Path and Err Message
    df = __remove_duplicates(df, ['Path', 'Err Message'])

    # Clean Err Message from input/parameter
    for re_and_replace in __regex_and_replacement_list:
        df['Err Message'] = df['Err Message'].str.replace(
            re_and_replace['regex'], re_and_replace['replacement'], regex=True)

    # Remove duplicates by Path and Err Message (again)
    df = __remove_duplicates(df, ['Path', 'Err Message'])

    return df
