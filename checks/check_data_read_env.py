import argparse
import json
from typing import Optional
import re
from typing import Sequence
from utils import *

def main(argv: Optional[Sequence[str]] = None) -> bool:
    print("here")
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    print(args)
    return_flag = False
    
    for filename in args.filenames:
        
        get_table_env_vars = set()

        with open(filename) as f:
            f_content = f.readlines()

            # get get_table func env variable value
            for line in f_content: 
                if line_contains_function(line, 'get_table'):
                    arg = get_function_argument(line, 'env')
                    if arg: get_table_env_vars.add(arg)

            # exit if is not called 
            if not get_table_env_vars: continue

            print(get_table_env_vars)
            # find declaration of current env
            for line in f_content: 
                for env in list(get_table_env_vars):
                    value = get_variable_value(line, env)
                    if not value: continue
                    if not "READ_ENV" in value:
                        print(f"! File {filename}: get_table is not done from 'READ_ENV' env. variable. Found value is '{value}'")
                        return_flag = True

    return return_flag
                    

if __name__ == '__main__':
    exit(main())