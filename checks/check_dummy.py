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

    return_flag=False
    return return_flag


if __name__ == '__main__':
    exit(main())