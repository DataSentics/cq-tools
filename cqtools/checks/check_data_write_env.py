import argparse
import json
from typing import Optional
import re
from typing import Sequence
from cqtools.checks.utils import (line_contains_function, get_function_argument, get_variable_value)
import re

def main(argv: Optional[Sequence[str]] = None) -> bool:

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    
    return_flag = False
    
    for filename in args.filenames:
        write_df_tables_vars = set()
        table_vars = set()
        env_vars = set()
        line_concat_func = '' 

        with open(filename) as f:
            f_content = f.readlines()
            # get write_df func table_name variable value

            for i in range(len(f_content)):
                line = f_content[i]
                
                if not line_contains_function(line, 'write_df') and line_concat_func == '': continue
                
                # form the function string 
                line_concat_func += line
                # if line end with comma or opening bracket (argument follows)
                if re.match(r".*[,|\(]\s*$", line): continue
                # find args and resent string 
                arg = get_function_argument(line_concat_func, 'table_name')
                line_concat_func = ''
                if arg: 
                    write_df_tables_vars.add(arg)
                else:
                    raise Warning(f"Argument table_name is missing: {filename}")

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