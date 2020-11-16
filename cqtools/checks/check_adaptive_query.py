import argparse
import json
from typing import Optional
import re
from typing import Sequence
from utils import line_contains_adaptive_query_on

def main(argv: Optional[Sequence[str]] = None) -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    return_flag=False
    
    for filename in args.filenames:
        present = False
        with open(filename) as f:
            for line in f.readlines(): 
                if line_contains_adaptive_query_on(line): 
                    present = True
                    break
        if not present:
            return_flag = True
            print(f'! {filename} does not use adaptive query feature')
    
    return return_flag


if __name__ == '__main__':
    exit(main())