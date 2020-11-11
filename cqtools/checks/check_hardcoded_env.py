import argparse
import json
from typing import Optional
import re
from typing import Sequence
from utils import line_contains_hardcoded_env_assignment

def main(argv: Optional[Sequence[str]] = None) -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    return_flag = False
    for filename in args.filenames:
        with open(filename) as f:
            for line in f.readlines(): 
                if line_contains_hardcoded_env_assignment(line, 'prod') or \
                    line_contains_hardcoded_env_assignment(line, 'dev') or \
                    line_contains_hardcoded_env_assignment(line, 'test'):

                    print(f'! {filename}: contains hardcoded environment assignment to a variable')
                    return_flag = True
    return return_flag


if __name__ == '__main__':
    exit(main())