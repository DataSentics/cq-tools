
import re
import os

def get_function_argument(line: str, arg_name=None) -> str:
    if not arg_name:
        match = re.search(r'\(\s*(.+?)\)', line)
    else:
        match = re.search(r'{}\s?\=\s?(.+?)\s?[\,|\)]'.format(arg_name), line)
    if match: return match.group(1)
    return None

def line_contains_function(line: str, f_name: str) -> bool:
    # new line
    if re.match(r"^\s*{}\(".format(f_name), line):
        return True

    # return value or semicolon or object function
    if re.match(r".*[\=|\;|\.]\s*{}\(".format(f_name), line):
        return True
    return False

def line_contains_adaptive_query_on(line: str) -> bool:
    if re.match(r"^\s*spark.conf.set\([\"|\']spark.sql.adaptive.enabled[\"|\']\s*,\s*True\s*\)", line):
        return True
    return False

def get_variable_value(line: str, var_name: str) -> str:
    match = re.search(r'^\s*{}\s?\=\s?(.+?)\s*\;?\s*$'.format(var_name), line)
    if match:
        return match.group(1)
    return None
    
def get_magic(line: str) -> bool:
    match = re.search(r"^\#\sMAGIC\s\%([^\s]+)", line)
    if match:
        return match.group(1)
    return None

def line_contains_hardcoded_env_assignment(line: str, env_name: str) -> bool:
    if re.match(r"[^\#\=]+\s*\=\s*[\"|\']{}[\"|\']\s*\;?$".format(env_name), line):
        return True
    return False
    
def convert_path_dbx_format(ntb_path: str):

    path_list = ntb_path.split(os.sep)
    try:
        src_index = path_list.index("src")
    except ValueError:
        src_index = 0
        print("The notebook is not located in src folder. Return the whole path")
    
    path_dbx = '/'.join(path_list[src_index:])
    path_dbx_noextention = path_dbx.split('.')[0]

    return path_dbx_noextention


def find_dict(key, dictionary):
    """ Returns all values of a given key in a dictionary """
    for k, v in dictionary.items():
        if k == key:
            yield v 
        if isinstance(v, dict):
            for result in find_dict(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in find_dict(key, d):
                        yield result

def get_adf_activity_execute_pipeline_name(activity: dict):
    if activity['type'] == "ExecutePipeline":
        pname = activity['typeProperties']['pipeline']
        if type(pname) is dict: pname = pname['referenceName']
        return pname
        
    return None
