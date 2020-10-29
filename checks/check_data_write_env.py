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

    retval = False
    write_df_tables_vars = set()
    used_env = set()
    
    for filename in args.filenames:
        print(filename)
        with open(filename) as f:
            # get write_df func table_name variable value
            for line in f.readlines(): 
                if line_contains_function(line, 'write_df'):
                    write_df_tables_vars.add(get_function_argument(line, 'table_name'))

            print(write_df_tables_vars)
            # exit if is not called 
            if not write_df_tables_vars: return False

            # if it is, find which env was used 
            for line in f.readlines(): 
                for v in write_df_tables_vars:
                    var_value = get_variable_value(line, v)
                    print(var_value)
                    
    return False
                    

if __name__ == '__main__':
    exit(main())