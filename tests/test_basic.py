import pytest
from cqtools.checks import utils 
import sys
 

def test_line_contains_function_base():
    assert utils.line_contains_function('display()', 'display')

def test_line_contains_function_return():
    line = ' = get_table(table_name=my_table_name)'
    assert utils.line_contains_function(line, 'get_table')

def test_line_contains_function_semicolon_return():
    line = 'n=1; table_name = get_table(table_name=my_table_name)'
    assert utils.line_contains_function(line, 'get_table')

def test_line_contains_function_semicolon():
    line = 'n=1; get_table(table_name=my_table_name)'
    assert utils.line_contains_function(line, 'get_table')

def test_str_contains_display_spaces():
   assert utils.line_contains_function('     display()', 'display')

def test_str_contains_display_tab():
    assert utils.line_contains_function('    display()', 'display')

def test_str_contains_display_comment():
    assert not utils.line_contains_function('#display()', 'display')

def test_str_contains_display_argument():
    assert utils.line_contains_function('display("Argument")', 'display')

def test_str_contains_function_obj():
    assert utils.line_contains_function('var.display("Argument")', 'display')

def test_get_function_argument_return_value():
    s = 'table_name = get_table(table_name=\'{}_{}\'.format(input_layer,table), database_name = database_name, env=read_env)'
    write_table_name = utils.get_function_argument(s, 'env')
    assert write_table_name == 'read_env'

def test_get_function_argument_base():
    s = 'write_df(df=df, table_name=target_table, spark=spark)'
    write_table_name = utils.get_function_argument(s, 'table_name')
    assert write_table_name == 'target_table'

def test_get_function_argument_single():
    s = 'write_df(argument_value)'
    write_table_name = utils.get_function_argument(s)
    assert write_table_name == 'argument_value'

def test_get_function_argument_extra_space():
    s = 'write_df(df=df, table_name=target_table , spark=spark)'
    write_table_name = utils.get_function_argument(s, 'table_name')
    assert write_table_name == 'target_table'

def test_get_function_argument_last_arg():
    s = 'write_df(df=df, table_name=target_table)'
    write_table_name = utils.get_function_argument(s, 'table_name')
    assert write_table_name == 'target_table'

def test_get_variable_value_string():
    s = 'df="value"'
    value = utils.get_variable_value(s, 'df')
    assert value == '"value"'

def test_get_variable_value_return_non_when_in_condition():
    s = 'if df=="value":'
    value = utils.get_variable_value(s, 'df')
    assert value is None

def test_get_variable_value_space():
    s = 'df = "value"'
    value = utils.get_variable_value(s, 'df')
    assert value == '"value"'

def test_get_variable_value_int():
    s = 'df = 5'
    value = utils.get_variable_value(s, 'df')
    assert  value == '5'

def test_get_variable_value_int_non_when_comment():
    s = '#df = 5'
    value = utils.get_variable_value(s, 'df')
    assert value is None

def test_get_variable_value_space_before():
    s = '   df = 5'
    value = utils.get_variable_value(s, 'df')
    assert value == '5'

def test_get_variable_value_semicol():
    s = 'df = 5;'
    value = utils.get_variable_value(s, 'df')
    assert value == '5'

def test_get_variable_value_semicol_space():
    s = 'df = 5 ;'
    value = utils.get_variable_value(s, 'df')
    assert value == '5'

def test_get_variable_value_semicol_space_after():
    s = 'df = 5 ;  '
    value = utils.get_variable_value(s, 'df')
    assert value == '5'

def test_get_variable_value_returns_one_when_prefix_diff():
    s = 'df = 5 ;  '
    value = utils.get_variable_value(s, 'main_df')
    assert value is None

def test_get_variable_value_func():
    s = 'target_table = get_table(table_name=\'{}_{}\'.format(output_layer, output_name), database_name=database_name, env=current_env)'
    expected = 'get_table(table_name=\'{}_{}\'.format(output_layer, output_name), database_name=database_name, env=current_env)'
    value = utils.get_variable_value(s, 'target_table')
    assert value == expected

def test_get_magic_run_magic():
    s = '# MAGIC %run'
    assert utils.get_magic(s) == 'run'

def test_gget_magic_run_magic_ith_args():
    s = '# MAGIC %run /src/utility/mount_sdk $ENV="live" $AZURE_STORAGE_NAME="sfmcresponsedatae1"'
    assert utils.get_magic(s) == 'run'

def test_get_magic_returns_none_when_comment():
    s = '# %run'
    assert utils.get_magic(s) is None

def test_line_contains_adaptive_query_on_doubleb():
    s = 'spark.conf.set("spark.sql.adaptive.enabled", True)'
    assert utils.line_contains_adaptive_query_on(s)

def test_line_contains_adaptive_query_on_sinlgeb():
    s = "spark.conf.set('spark.sql.adaptive.enabled', True)"
    assert utils.line_contains_adaptive_query_on(s)

def test_line_contains_adaptive_query_on_spaces():
    s = '  spark.conf.set("spark.sql.adaptive.enabled"  ,   True)  '
    assert utils.line_contains_adaptive_query_on(s)

def test_line_contains_adaptive_query_on_return_false_when_off_spaces():
    s = '  spark.conf.set("spark.sql.adaptive.enabled"  ,   False)  '
    assert not utils.line_contains_adaptive_query_on(s)

def test_line_contains_adaptive_query_on_return_false_when_off():
    s = 'spark.conf.set("spark.sql.adaptive.enabled", False)'
    assert not utils.line_contains_adaptive_query_on(s)

def test_line_contains_adaptive_query_on_return_false_when_other_string():
    s = 'any other string'
    assert not utils.line_contains_adaptive_query_on(s)

def test_contains_hardcoded_env_assignment_basic():
    s = 'var ="prod"'
    assert utils.line_contains_hardcoded_env_assignment(s, 'prod')

def test_contains_hardcoded_env_assignment_false_when_comment():
    s = '#var ="prod"'
    assert not utils.line_contains_hardcoded_env_assignment(s, 'prod')

def test_contains_hardcoded_env_assignment_false_when_contdition():
    s = 'var =="prod"'
    assert not utils.line_contains_hardcoded_env_assignment(s, 'prod')

def test_convert_path_dbx_format_basic():
    p = "/Users/lebedana/Documents/sources/cq-tools/tests/test_files/src/notebook_example.py"

    assert utils.convert_path_dbx_format(p) == 'src/notebook_example'

def test_convert_path_dbx_format_nosrc():
    p = "/Users/lebedana/Documents/sources/cq-tools/tests/test_files/notebook_example.py"
    r = "/Users/lebedana/Documents/sources/cq-tools/tests/test_files/notebook_example"
    assert utils.convert_path_dbx_format(p) == r