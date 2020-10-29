
import re

def get_function_argument(line: str, arg_name:str) -> str:
    match = re.search(r'{}\s?\=\s?(.+?)\s?[\,|\)]'.format(arg_name), line)
    if match:
        return match.group(1)

def line_contains_function(line: str, f_name: str) -> bool:
    if re.match(r"^\s*{}\(".format(f_name), line):
        return True
    return False

def get_variable_value(line: str, var_name: str) -> str:
    match = re.search(r'{}\s?\=\s?(.+?)\s*\;?\s*$'.format(var_name), line)
    if match:
        return match.group(1)