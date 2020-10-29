import unittest
from utils import *


class TestStringMethods(unittest.TestCase):

    def test_line_contains_function_base(self):
        self.assertTrue(line_contains_function('display()', 'display'))

    def test_str_contains_display_spaces(self):
        self.assertTrue(line_contains_function('     display()', 'display'))
    
    def test_str_contains_display_tab(self):
        self.assertTrue(line_contains_function('    display()', 'display'))

    def test_str_contains_display_comment(self):
        self.assertFalse(line_contains_function('#display()', 'display'))

    def test_str_contains_display_argument(self):
        self.assertTrue(line_contains_function('display("Argument")', 'display'))
    
    def test_get_function_argument_base(self):
        s = 'write_df(df=df, table_name=target_table, spark=spark)'
        write_table_name = get_function_argument(s, 'table_name')
        self.assertEqual(write_table_name, 'target_table')
    
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

    def test_get_variable_value_space(self):
        s = 'df = "value"'
        value = get_variable_value(s, 'df')
        self.assertEqual(value, '"value"')
    
    def test_get_variable_value_int(self):
        s = 'df = 5'
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

    def test_get_variable_value_diff_func(self):
        s = 'df = 5 ;  '
        value = get_variable_value(s, 'main_df')
        self.assertIsNone(value)

    def test_get_variable_value_func(self):
            s = 'target_table = get_table(table_name=\'{}_{}\'.format(output_layer, output_name), database_name=database_name, env=current_env)'
            value = get_variable_value(s, 'target_table')
            self.assertEqual(value, 'get_table(table_name=\'{}_{}\'.format(output_layer, output_name), database_name=database_name, env=current_env)')


if __name__ == '__main__':
    unittest.main()