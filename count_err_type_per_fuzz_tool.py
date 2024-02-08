import argparse
import os
from pprint import pprint

import pandas as pd

from utils import ErrTypeSetter, clean_and_remove_duplicates


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', '--log', type=str,
                        help="Log type, either 'nodejs' or 'python'")

    args = parser.parse_args()

    log_type = str.lower(args.log)

    dir_path = 'err_data'

    all_files = [file for file in os.listdir(dir_path)]

    for file in all_files:
        file_path = os.path.join(dir_path, file)
        output_path = f'output/{file}.xlsx'

        df = pd.read_csv(file_path, sep='#', names=[
            'Log Level', 'Method', 'Path', 'Status Code', 'Validation Mode', 'Err Message'])

        df = clean_and_remove_duplicates(df)

        err_type_setter = ErrTypeSetter(df)
        df = err_type_setter.extend_df(log_type)

        unknown_count = err_type_setter.get_unknown_count()
        missing_count = err_type_setter.get_missing_count()
        invalid_count = err_type_setter.get_invalid_count()
        constraint_count = err_type_setter.get_constraint_count()

        df.to_excel(output_path, index=False)

        pprint({
            'Filename': file,
            'Total Err': len(df),
            'Detail': {
                'unknown': unknown_count,
                'missing_required': missing_count,
                'invalid_type': invalid_count,
                'constraint_violation': constraint_count
            }
        })


if __name__ == '__main__':
    main()
