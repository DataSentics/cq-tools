
import re

def get_function_argument(line: str, arg_name=None) -> str:
    if not arg_name:
        match = re.search(r'\(\s*(.+?)\)', line)
    else:
        match = re.search(r'{}\s?\=\s?(.+?)\s?[\,|\)]'.format(arg_name), line)
    if match:
        return match.group(1)

def line_contains_function(line: str, f_name: str) -> bool:
    # new line
    if re.match(r"^\s*{}\(".format(f_name), line):
        return True

    # return value or semicolon
    if re.match(r".*[\=|\;]\s*{}\(".format(f_name), line):
        return True
    return False

def line_contains_adaptive_query_on(line: str) -> bool:
    if re.match(r"^\s*spark.conf.set\([\"|\']spark.sql.adaptive.enabled[\"|\']\s*,\s*True\s*\)", line):
        return True
    return False

def get_variable_value(line: str, var_name: str) -> str:
    match = re.search(r'^{}\s?\=\s?(.+?)\s*\;?\s*$'.format(var_name), line)
    if match:
        return match.group(1)

def get_magic(line: str) -> bool:
    match = re.search(r"^\#\sMAGIC\s\%([^\s]+)", line)
    if match:
        return match.group(1)
    
