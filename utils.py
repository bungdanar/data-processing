import os
from typing import TypedDict
import numpy as np

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


class ErrTypeRef(TypedDict):
    unknown: str
    missing_required: str
    invalid_type: str
    constraint_violation: str


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


class ErrTypeSetter:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    __err_type_ref: ErrTypeRef = {
        'unknown': 'Unknown type',
        'missing_required': 'Missing required',
        'invalid_type': 'Invalid type',
        'constraint_violation': 'Constraint violation'
    }

    def __generate_err_type_ref(self, log_type: str) -> list[dict]:
        ref = []

        if log_type == 'nodejs':
            ref = [
                # missing_required
                {
                    'pattern': 'notnull violation',
                    'type': self.__err_type_ref['missing_required']
                },
                {
                    'pattern': r'.*? properties of undefined',
                    'type': self.__err_type_ref['missing_required']
                },
                # invalid_type
                {
                    'pattern': 'string violation',
                    'type': self.__err_type_ref['invalid_type']
                },
                {
                    'pattern': r'incorrect .*? value',
                    'type': self.__err_type_ref['invalid_type']
                },
                {
                    'pattern': r'.*? is not a function',
                    'type': self.__err_type_ref['invalid_type']
                },
                {
                    'pattern': r'.*? properties of null',
                    'type': self.__err_type_ref['invalid_type']
                },
                # constraint_violation
                {
                    'pattern': 'check constraint',
                    'type': self.__err_type_ref['constraint_violation']
                },
                {
                    'pattern': 'out of range',
                    'type': self.__err_type_ref['constraint_violation']
                },
                {
                    'pattern': 'data too long',
                    'type': self.__err_type_ref['constraint_violation']
                },
            ]
        elif log_type == 'python':
            ref = [
                # missing_required
                {
                    'pattern': 'cannot be null',
                    'type': self.__err_type_ref['missing_required']
                },
                {
                    'pattern': 'object is not subscriptable',
                    'type': self.__err_type_ref['missing_required']
                },
                {
                    'pattern': r"^msg=('tags'|'category'|'categories'|'coupons'|'address'|'addresses'|'product'|'shipping')$",
                    'type': self.__err_type_ref['missing_required']
                },
                {
                    'pattern': 'invalid keyword argument for',
                    'type': self.__err_type_ref['missing_required']
                },
                # invalid_type
                {
                    'pattern': r'incorrect .*? value',
                    'type': self.__err_type_ref['invalid_type']
                },
                {
                    'pattern': "MySQL server version for the right syntax to use near",
                    'type': self.__err_type_ref['invalid_type']
                },
                {
                    'pattern': 'is not None, True, or False',
                    'type': self.__err_type_ref['invalid_type']
                },
                {
                    'pattern': r'argument after \*\* must be a mapping',
                    'type': self.__err_type_ref['invalid_type']
                },
                {
                    'pattern': 'object is not iterable',
                    'type': self.__err_type_ref['invalid_type']
                },
                {
                    'pattern': 'unhashable type',
                    'type': self.__err_type_ref['invalid_type']
                },
                {
                    'pattern': 'indices must be',
                    'type': self.__err_type_ref['invalid_type']
                },
                {
                    'pattern': 'Not a boolean value',
                    'type': self.__err_type_ref['invalid_type']
                },
                # constraint_violation
                {
                    'pattern': 'check constraint',
                    'type': self.__err_type_ref['constraint_violation']
                },
                {
                    'pattern': 'out of range',
                    'type': self.__err_type_ref['constraint_violation']
                },
                {
                    'pattern': 'data too long',
                    'type': self.__err_type_ref['constraint_violation']
                },
            ]
        else:
            pass

        return ref

    def extend_df(self, log_type: str):
        self.df['err_type'] = self.__err_type_ref['unknown']

        ref = self.__generate_err_type_ref(log_type)

        for re_and_type in ref:
            mask = (self.df['err_type'] == self.__err_type_ref['unknown'])
            self.df.loc[mask, 'err_type'] = np.where(self.df.loc[mask, 'Err Message'].str.contains(
                re_and_type['pattern'], case=False, regex=True), re_and_type['type'], self.__err_type_ref['unknown'])

        return self.df

    def get_unknown_count(self):
        return (self.df['err_type'] == self.__err_type_ref['unknown']).sum()

    def get_missing_count(self):
        return (self.df['err_type'] ==
                self.__err_type_ref['missing_required']).sum()

    def get_invalid_count(self):
        return (self.df['err_type'] == self.__err_type_ref['invalid_type']).sum()

    def get_constraint_count(self):
        return (self.df['err_type'] == self.__err_type_ref['constraint_violation']).sum()
