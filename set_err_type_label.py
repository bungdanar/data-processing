import argparse
from pprint import pprint
from typing import TypedDict

import numpy as np

from utils import get_err_aggr


class __ErrTypeRef(TypedDict):
    unknown: str
    missing_required: str
    invalid_type: str
    constraint_violation: str


__err_type_ref: __ErrTypeRef = {
    'unknown': 'Unknown type',
    'missing_required': 'Missing required',
    'invalid_type': 'Invalid type',
    'constraint_violation': 'Constraint violation'
}


def __generate_err_type_ref(log_type: str) -> list[dict]:
    ref = []

    if log_type == 'nodejs':
        ref = [
            # missing_required
            {
                'pattern': 'notnull violation',
                'type': __err_type_ref['missing_required']
            },
            {
                'pattern': r'.*? properties of undefined',
                'type': __err_type_ref['missing_required']
            },
            # invalid_type
            {
                'pattern': 'string violation',
                'type': __err_type_ref['invalid_type']
            },
            {
                'pattern': r'incorrect .*? value',
                'type': __err_type_ref['invalid_type']
            },
            {
                'pattern': r'.*? is not a function',
                'type': __err_type_ref['invalid_type']
            },
            {
                'pattern': r'.*? properties of null',
                'type': __err_type_ref['invalid_type']
            },
            # constraint_violation
            {
                'pattern': 'check constraint',
                'type': __err_type_ref['constraint_violation']
            },
            {
                'pattern': 'out of range',
                'type': __err_type_ref['constraint_violation']
            },
            {
                'pattern': 'data too long',
                'type': __err_type_ref['constraint_violation']
            },
        ]
    elif log_type == 'python':
        ref = [
            # missing_required
            {
                'pattern': 'cannot be null',
                'type': __err_type_ref['missing_required']
            },
            {
                'pattern': 'object is not subscriptable',
                'type': __err_type_ref['missing_required']
            },
            {
                'pattern': r"^msg=('tags'|'category'|'categories'|'coupons'|'address'|'addresses'|'product'|'shipping')$",
                'type': __err_type_ref['missing_required']
            },
            {
                'pattern': 'invalid keyword argument for',
                'type': __err_type_ref['missing_required']
            },
            # invalid_type
            {
                'pattern': r'incorrect .*? value',
                'type': __err_type_ref['invalid_type']
            },
            {
                'pattern': "MySQL server version for the right syntax to use near",
                'type': __err_type_ref['invalid_type']
            },
            {
                'pattern': 'is not None, True, or False',
                'type': __err_type_ref['invalid_type']
            },
            {
                'pattern': r'argument after \*\* must be a mapping',
                'type': __err_type_ref['invalid_type']
            },
            {
                'pattern': 'object is not iterable',
                'type': __err_type_ref['invalid_type']
            },
            {
                'pattern': 'unhashable type',
                'type': __err_type_ref['invalid_type']
            },
            {
                'pattern': 'indices must be',
                'type': __err_type_ref['invalid_type']
            },
            {
                'pattern': 'Not a boolean value',
                'type': __err_type_ref['invalid_type']
            },
            # constraint_violation
            {
                'pattern': 'check constraint',
                'type': __err_type_ref['constraint_violation']
            },
            {
                'pattern': 'out of range',
                'type': __err_type_ref['constraint_violation']
            },
            {
                'pattern': 'data too long',
                'type': __err_type_ref['constraint_violation']
            },
        ]
    else:
        pass

    return ref


def __set_err_type_label(log_type: str):
    output_path = 'output/err_aggr.xlsx'

    df = get_err_aggr()
    df['err_type'] = __err_type_ref['unknown']

    ref = __generate_err_type_ref(log_type)

    for re_and_type in ref:
        mask = (df['err_type'] == __err_type_ref['unknown'])
        df.loc[mask, 'err_type'] = np.where(df.loc[mask, 'Err Message'].str.contains(
            re_and_type['pattern'], case=False, regex=True), re_and_type['type'], __err_type_ref['unknown'])

    unknown_count = (df['err_type'] == __err_type_ref['unknown']).sum()
    missing_count = (df['err_type'] ==
                     __err_type_ref['missing_required']).sum()
    invalid_count = (df['err_type'] == __err_type_ref['invalid_type']).sum()
    constraint_count = (
        df['err_type'] == __err_type_ref['constraint_violation']).sum()

    df.to_excel(output_path, index=False)

    pprint({
        'unknown': unknown_count,
        'missing_required': missing_count,
        'invalid_type': invalid_count,
        'constraint_violation': constraint_count
    })


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--log', type=str,
                        help="Log type, either 'nodejs' or 'python'")

    args = parser.parse_args()

    log_type = str.lower(args.log)
    __set_err_type_label(log_type)


if __name__ == '__main__':
    main()
