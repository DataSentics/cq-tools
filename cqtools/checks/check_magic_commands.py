import argparse
import json
from typing import Optional
import re
from typing import Sequence
from .utils import get_magic 

def main(argv: Optional[Sequence[str]] = None) -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    return_flag = False
    for filename in args.filenames:
        with open(filename) as f:
            for line in f.readlines(): 
                magic = get_magic(line)
                if not magic: continue
                if magic in ['md']: continue
                print(f'! {filename}: contains magic command "{magic}"')
                return_flag = True
            
    return return_flag


if __name__ == '__main__':
    exit(main())