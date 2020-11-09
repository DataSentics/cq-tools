import unittest
from utils import *


class TestStringMethods(unittest.TestCase):

    def test_line_contains_function_base(self):
        self.assertTrue(line_contains_function('display()', 'display'))

    def test_line_contains_function_return(self):
        line = ' = get_table(table_name=my_table_name)'
        self.assertTrue(line_contains_function(line, 'get_table'))

    def test_line_contains_function_semicolon_return(self):
        line = 'n=1; table_name = get_table(table_name=my_table_name)'
        self.assertTrue(line_contains_function(line, 'get_table'))
    
    def test_line_contains_function_semicolon(self):
        line = 'n=1; get_table(table_name=my_table_name)'
        self.assertTrue(line_contains_function(line, 'get_table'))

    def test_str_contains_display_spaces(self):
        self.assertTrue(line_contains_function('     display()', 'display'))
    
    def test_str_contains_display_tab(self):
        self.assertTrue(line_contains_function('    display()', 'display'))

    def test_str_contains_display_comment(self):
        self.assertFalse(line_contains_function('#display()', 'display'))

    def test_str_contains_display_argument(self):
        self.assertTrue(line_contains_function('display("Argument")', 'display'))
    
    def test_str_contains_function_obj(self):
        self.assertTrue(line_contains_function('var.display("Argument")', 'display'))
    
    def test_get_function_argument_return_value(self):
        s = 'table_name = get_table(table_name=\'{}_{}\'.format(input_layer,table), database_name = database_name, env=read_env)'
        write_table_name = get_function_argument(s, 'env')
        self.assertEqual(write_table_name, 'read_env')

    def test_get_function_argument_base(self):
        s = 'write_df(df=df, table_name=target_table, spark=spark)'
        write_table_name = get_function_argument(s, 'table_name')
        self.assertEqual(write_table_name, 'target_table')

    def test_get_function_argument_signle(self):
        s = 'write_df(argument_value)'
        write_table_name = get_function_argument(s)
        self.assertEqual(write_table_name, 'argument_value')
    
    def test_get_function_argument_extra_space(self):
        s = 'write_df(df=df, table_name=target_table , spark=spark)'
        write_table_name = get_function_argument(s, 'table_name')
        self.assertEqual(write_table_name, 'target_table')

    def test_get_function_argument_last_arg(self):
        s = 'write_df(df=df, table_name=target_table)'
        write_table_name = get_function_argument(s, 'table_name')
        self.assertEqual(write_table_name, 'target_table')

    def test_get_variable_value_string(self):
        s = 'df="value"'
        value = get_variable_value(s, 'df')
        self.assertEqual(value, '"value"')

    def test_get_variable_value_return_non_when_in_condition(self):
        s = 'if df=="value":'
        value = get_variable_value(s, 'df')
        self.assertIsNone(value)

    def test_get_variable_value_space(self):
        s = 'df = "value"'
        value = get_variable_value(s, 'df')
        self.assertEqual(value, '"value"')
    
    def test_get_variable_value_int(self):
        s = 'df = 5'
        value = get_variable_value(s, 'df')
        self.assertEqual(value, '5')
    
    def test_get_variable_value_int(self):
        s = '#df = 5'
        value = get_variable_value(s, 'df')
        self.assertIsNone(value)
    
    def test_get_variable_value_space_before(self):
        s = '   df = 5'
        value = get_variable_value(s, 'df')
        self.assertEqual(value, '5')
    
    def test_get_variable_value_semicol(self):
        s = 'df = 5;'
        value = get_variable_value(s, 'df')
        self.assertEqual(value, '5')
    
    def test_get_variable_value_semicol_space(self):
        s = 'df = 5 ;'
        value = get_variable_value(s, 'df')
        self.assertEqual(value, '5')
    
    def test_get_variable_value_semicol_space_after(self):
        s = 'df = 5 ;  '
        value = get_variable_value(s, 'df')
        self.assertEqual(value, '5')

    def test_get_variable_value_returns_one_when_prefix_diff(self):
        s = 'df = 5 ;  '
        value = get_variable_value(s, 'main_df')
        self.assertIsNone(value)

    def test_get_variable_value_func(self):
            s = 'target_table = get_table(table_name=\'{}_{}\'.format(output_layer, output_name), database_name=database_name, env=current_env)'
            value = get_variable_value(s, 'target_table')
            self.assertEqual(value, 'get_table(table_name=\'{}_{}\'.format(output_layer, output_name), database_name=database_name, env=current_env)')

    def test_get_magic_run_magic(self):
        s = '# MAGIC %run'
        self.assertEqual(get_magic(s), 'run')
    
    def test_gget_magic_run_magic_ith_args(self):
        s = '# MAGIC %run /src/utility/mount_sdk $ENV="live" $AZURE_STORAGE_NAME="sfmcresponsedatae1"'
        self.assertEqual(get_magic(s), 'run')

    def test_get_magic_returns_none_when_comment(self):
        s = '# %run'
        self.assertIsNone(get_magic(s))

    def test_line_contains_adaptive_query_on_doubleb(self):
        s = 'spark.conf.set("spark.sql.adaptive.enabled", True)'
        self.assertTrue(line_contains_adaptive_query_on(s))

    def test_line_contains_adaptive_query_on_sinlgeb(self):
        s = "spark.conf.set('spark.sql.adaptive.enabled', True)"
        self.assertTrue(line_contains_adaptive_query_on(s))
    
    def test_line_contains_adaptive_query_on_spaces(self):
        s = '  spark.conf.set("spark.sql.adaptive.enabled"  ,   True)  '
        self.assertTrue(line_contains_adaptive_query_on(s))

    def test_line_contains_adaptive_query_on_return_false_when_off(self):
        s = '  spark.conf.set("spark.sql.adaptive.enabled"  ,   False)  '
        self.assertFalse(line_contains_adaptive_query_on(s))
    
    def test_line_contains_adaptive_query_on_return_false_when_off(self):
        s = 'spark.conf.set("spark.sql.adaptive.enabled", False)'
        self.assertFalse(line_contains_adaptive_query_on(s))

    def test_line_contains_adaptive_query_on_return_false_when_other_string(self):
        s = 'any other string'
        self.assertFalse(line_contains_adaptive_query_on(s))
    
    def test_contains_hardcoded_env_assignment_basic(self):
        s = 'var ="prod"'
        self.assertTrue(line_contains_hardcoded_env_assignment(s, 'prod'))
    
    def test_contains_hardcoded_env_assignment_false_when_comment(self):
        s = '#var ="prod"'
        self.assertFalse(line_contains_hardcoded_env_assignment(s, 'prod'))

    def test_contains_hardcoded_env_assignment_false_when_contdition(self):
        s = 'var =="prod"'
        self.assertFalse(line_contains_hardcoded_env_assignment(s, 'prod'))

if __name__ == '__main__':
    unittest.main()