import argparse
from pprint import pprint

from utils import get_err_aggr, ErrTypeSetter


def __set_err_type_label(log_type: str):
    output_path = 'output/err_aggr.xlsx'

    df = get_err_aggr()

    err_type_setter = ErrTypeSetter(df)
    df = err_type_setter.extend_df(log_type)

    unknown_count = err_type_setter.get_unknown_count()
    missing_count = err_type_setter.get_missing_count()
    invalid_count = err_type_setter.get_invalid_count()
    constraint_count = err_type_setter.get_constraint_count()

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
