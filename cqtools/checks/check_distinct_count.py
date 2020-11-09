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

    return_flag = False; func_name = 'distinct'
    for filename in args.filenames:
        f_count = 0
        with open(filename) as f:
            for line in f.readlines(): 
                if line_contains_function(line, func_name):
                    f_count += 1
            if f_count > 5:       
                print(f'! {filename}: uses {func_name}() function more than 5 times')
                return_flag = True
    return return_flag


if __name__ == '__main__':
    exit(main())