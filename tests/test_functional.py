from cqtools.checks import utils
import sys
import os
from cqtools.checks import (check_adaptive_query, check_adf_executes_ntb,
    check_adf_executes_pipeline, check_cache_unpersist, check_data_write_env,
    check_distinct_count, check_hardcoded_env, check_magic_commands)
 
TEST_FILES_PATH = "tests/test_files/src"

def test_check_adaptive_query_fails_when_no_statement():
    fpath = os.path.join(TEST_FILES_PATH, 'example_display.py')
    fails = True
    assert check_adaptive_query.main([fpath]) == fails

def test_check_adaptive_query():
    fpath = os.path.join(TEST_FILES_PATH, 'example_adaptive_on.py')
    fails = False
    assert check_adaptive_query.main([fpath]) == fails

def test_check_adf_executes_ntb_fails_when_no_job():
    fpath = os.path.join(TEST_FILES_PATH, 'example_no_pipeline.py')
    fails = True
    assert check_adf_executes_ntb.main([fpath]) == fails

def test_check_adf_executes_ntb_no_pipeline():
    fpath = os.path.join(TEST_FILES_PATH, 'example_with_pipeline.py')
    fails = False
    assert check_adf_executes_ntb.main([fpath]) == fails

def test_check_adf_executes_ntb_no_pipeline_multiple_reference():
    fpath = os.path.join(TEST_FILES_PATH, 'example_with_pipeline2.py')
    fails = False
    assert check_adf_executes_ntb.main([fpath]) == fails

def test_check_adf_executes_pipeline_fails_when_nopipeline():
    fpath_job = os.path.join(TEST_FILES_PATH, 'job_example_notebook2_nopipeline.json')
    fpath_pip1 = os.path.join(TEST_FILES_PATH, 'example_L4_pipeline.json')
    fpath_pip2 = os.path.join(TEST_FILES_PATH, 'example_L4_for_each.json')
    fails = True
    assert check_adf_executes_pipeline.main([fpath_job, fpath_pip1, fpath_pip2]) == fails

def test_check_adf_executes_pipeline():
    fpath_job = os.path.join(TEST_FILES_PATH, 'job_example_notebook1.json')
    fpath_pip1 = os.path.join(TEST_FILES_PATH, 'example_L4_pipeline.json')
    fpath_pip2 = os.path.join(TEST_FILES_PATH, 'example_L4_for_each.json')
    fails = False
    assert check_adf_executes_pipeline.main([fpath_job, fpath_pip1, fpath_pip2]) == fails

def test_check_adf_executes_pipeline_foreach_type():
    fpath_job = os.path.join(TEST_FILES_PATH, 'job_example_notebook2_inforeach.json')
    fpath_pip1 = os.path.join(TEST_FILES_PATH, 'example_L4_pipeline.json')
    fpath_pip2 = os.path.join(TEST_FILES_PATH, 'example_L4_for_each.json')
    fails = False
    assert check_adf_executes_pipeline.main([fpath_job, fpath_pip1, fpath_pip2]) == fails

def test_check_cache_unpersist_fails_when_cache_only():
    fpath = os.path.join(TEST_FILES_PATH, 'example_cache.py')
    fails = True
    assert check_cache_unpersist.main([fpath]) == fails

def test_check_cache_unpersist():
    fpath = os.path.join(TEST_FILES_PATH, 'example_cache_unpersist.py')
    fails = False
    assert check_cache_unpersist.main([fpath]) == fails

def test_check_data_write_env():
    fpath = os.path.join(TEST_FILES_PATH, 'example_write_current.py')
    fails = False
    assert check_data_write_env.main([fpath]) == fails

def test_check_data_write_env_fails_when_prod_multiline_write_function():
    fpath = os.path.join(TEST_FILES_PATH, 'example_write_prod_multiline.py')
    fails = True
    assert check_data_write_env.main([fpath]) == fails

def test_check_data_write_env_fails_when_prod():
    fpath = os.path.join(TEST_FILES_PATH, 'example_write_prod.py')
    fails = True
    assert check_data_write_env.main([fpath]) == fails

def test_check_data_write_env_fails_when_prod_multiline_write_function():
    fpath = os.path.join(TEST_FILES_PATH, 'example_write_prod_multiline.py')
    fails = True
    assert check_data_write_env.main([fpath]) == fails

def test_check_data_write_env_fails_when_multiple_assignment():
    fpath = os.path.join(TEST_FILES_PATH, 'example_write_multiple_assignment.py')
    fails = True
    assert check_data_write_env.main([fpath]) == fails

def test_check_distinct_count():
    fpath = os.path.join(TEST_FILES_PATH, 'example_display.py')
    fails = False
    assert check_distinct_count.main([fpath]) == fails

def test_check_distinct_count_fails_when_many_distinct():
    fpath = os.path.join(TEST_FILES_PATH, 'example_distinct.py')
    fails = True
    assert check_distinct_count.main([fpath]) == fails

def test_check_hardcoded_env():
    fpath = os.path.join(TEST_FILES_PATH, 'example_distinct.py')
    fails = False
    assert check_hardcoded_env.main([fpath]) == fails

def test_check_hardcoded_env_fails_when_variable_has_prod_value():
    fpath = os.path.join(TEST_FILES_PATH, 'example_write_prod.py')
    fails = True
    assert check_hardcoded_env.main([fpath]) == fails

def test_check_magic_commands_fails_when_sh_magic():
    fpath = os.path.join(TEST_FILES_PATH, 'example_magic_sh.py')
    fails = True
    assert check_magic_commands.main([fpath]) == fails

def test_check_magic_commands_ok_when_commented_magic():
    fpath = os.path.join(TEST_FILES_PATH, 'example_magic_commented.py')
    fails = False
    assert check_magic_commands.main([fpath]) == fails

def test_check_magic_commands():
    fpath = os.path.join(TEST_FILES_PATH, 'example_display.py')
    fails = False
    assert check_magic_commands.main([fpath]) == fails

def test_check_magic_commands():
    fpath = os.path.join(TEST_FILES_PATH, 'example_display.py')
    fails = False
    assert check_magic_commands.main([fpath]) == fails