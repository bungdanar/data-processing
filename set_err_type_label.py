from pprint import pprint
from typing import TypedDict

import numpy as np

from utils import get_err_aggr


class ErrTypeRef(TypedDict):
    unknown: str
    missing_required: str
    invalid_type: str
    constraint_violation: str


err_type_ref: ErrTypeRef = {
    'unknown': 'Unknown type',
    'missing_required': 'Missing required',
    'invalid_type': 'Invalid type',
    'constraint_violation': 'Constraint violation'
}

regex_and_type_list = [
    {
        'pattern': 'check constraint',
        'type': err_type_ref['constraint_violation']
    },
    {
        'pattern': 'out of range',
        'type': err_type_ref['constraint_violation']
    },
    {
        'pattern': 'data too long',
        'type': err_type_ref['constraint_violation']
    },
    {
        'pattern': 'msg=notnull violation',
        'type': err_type_ref['missing_required']
    },
    {
        'pattern': r'msg=.*? properties of undefined',
        'type': err_type_ref['missing_required']
    },
    {
        'pattern': 'cannot be null',
        'type': err_type_ref['missing_required']
    },
    {
        'pattern': 'msg=string violation',
        'type': err_type_ref['invalid_type']
    },
    {
        'pattern': r'incorrect .*? value',
        'type': err_type_ref['invalid_type']
    },
    {
        'pattern': r'msg=.*? is not a function',
        'type': err_type_ref['invalid_type']
    },
    {
        'pattern': r'msg=.*? properties of null',
        'type': err_type_ref['invalid_type']
    },
]

output_path = 'output/err_aggr.xlsx'

df = get_err_aggr()
df['err_type'] = err_type_ref['unknown']

for re_and_type in regex_and_type_list:
    mask = (df['err_type'] == err_type_ref['unknown'])
    df.loc[mask, 'err_type'] = np.where(df.loc[mask, 'Err Message'].str.contains(
        re_and_type['pattern'], case=False, regex=True), re_and_type['type'], err_type_ref['unknown'])

unknown_count = (df['err_type'] == err_type_ref['unknown']).sum()
missing_count = (df['err_type'] == err_type_ref['missing_required']).sum()
invalid_count = (df['err_type'] == err_type_ref['invalid_type']).sum()
constraint_count = (
    df['err_type'] == err_type_ref['constraint_violation']).sum()

df.to_excel(output_path, index=False)

pprint({
    'unknown': unknown_count,
    'missing_required': missing_count,
    'invalid_type': invalid_count,
    'constraint_violation': constraint_count
})
