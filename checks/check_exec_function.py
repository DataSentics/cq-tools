import argparse
import json
from typing import Optional
import re
from typing import Sequence
from utils import * 

def main(argv: Optional[Sequence[str]] = None) -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    return_flag = False; func_name = 'exec'
    for filename in args.filenames:
        with open(filename) as f:
            for line in f.readlines(): 
                if line_contains_function(line, func_name):
                    print(f'! {filename}: contains {func_name}() function')
                    return_flag = True
    return return_flag


if __name__ == '__main__':
    exit(main())