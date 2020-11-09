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
    
    return_flag = False
    
    for filename in args.filenames:
        write_df_tables_vars = set()
        table_vars = set()
        env_vars = set()

        with open(filename) as f:
            f_content = f.readlines()

            # get write_df func table_name variable value
            for line in f_content: 
                if line_contains_function(line, 'write_df'):
                    arg = get_function_argument(line, 'table_name')
                    if arg: write_df_tables_vars.add(arg)

            # exit if is not called 
            if not write_df_tables_vars: continue

            # if it is, find which env was used 
            for line in f_content: 
                for v in list(write_df_tables_vars):
                    name = get_variable_value(line, v)
                    if name: table_vars.add(name)

            # find declaration of the variable
            for v in table_vars:
                env = get_function_argument(v, 'env')
                if env: 
                    env_vars.add(env)

            # find declaration of current env
            for line in f_content: 
                for env in list(env_vars):
                    value = get_variable_value(line, env)
                    if not value: continue
                    if not "CURRENT_ENV" in value:
                        print(f"! File {filename}: write_df is not done from 'CURRENT_ENV' env. variable. Found value is '{value}'")
                        return_flag = True

    return return_flag
                    

if __name__ == '__main__':
    exit(main())