import argparse
import json
from typing import Optional
import re
from typing import Sequence
from .utils import line_contains_function

def main(argv: Optional[Sequence[str]] = None) -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    return_flag = False; 
    for filename in args.filenames:
        cache_count = 0; unpersist_count = 0
        with open(filename) as f:
            for line in f.readlines(): 
                if line_contains_function(line, 'cache'):
                    cache_count += 1
                if line_contains_function(line, 'unpersist'):
                    unpersist_count += 1
            if cache_count != unpersist_count:       
                print(f'! {filename}: not equal #of calls of cache and unpersist functions')
                return_flag = True
    return return_flag


if __name__ == '__main__':
    exit(main())