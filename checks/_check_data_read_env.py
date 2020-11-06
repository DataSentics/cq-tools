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
        
        get_table_name = set()

        with open(filename) as f:
            f_content = f.readlines()

            # get get_table func env variable value
            for line in f_content: 
                
                if line_contains_function(line, 'spark.read.table('):
                    arg = get_function_argument(line)
                    if arg: 
                        get_table_name.add(arg)
                    else:
                        # try with the arg name
                        arg = get_function_argument(line, 'tableName')
                        if arg: 
                            get_table_name.add(arg) 

            # exit if is not called 
            if not get_table_name: continue


            # find declaration of current env
            for line in f_content: 
                for env in list(get_table_name):
                    value = get_variable_value(line, env)
                    if not value: continue
                    if not "READ_ENV" in value:
                        print(f"! File {filename}: get_table is not done from 'READ_ENV' env. variable. Found value is '{value}'")
                        return_flag = True

    return True
                    

if __name__ == '__main__':
    exit(main())