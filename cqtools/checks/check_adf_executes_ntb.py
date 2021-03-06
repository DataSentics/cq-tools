import argparse
import json
from typing import Optional
import re
from typing import Sequence
from cqtools.checks.utils import (convert_path_dbx_format, find_dict)
import json
from cqtools.checks.config import ADF_PIPELINE_PATH
import glob 

def main(argv: Optional[Sequence[str]] = None) -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    ntb_filenames = args.filenames
    # get adf pipelines
    if not ADF_PIPELINE_PATH: raise ValueError("ADF_PIPELINE_PATH (required env. environment variable) is None")
    adf_filenames = [f for f in glob.glob(ADF_PIPELINE_PATH + "**/*.json", recursive=True)]
    adf_ntb_executed_map = {}
    ntbs_set = set()
    return_flag=False

    # for each pipeline get the executing ntb name
    for adf_fname in adf_filenames:
        with open(adf_fname) as f:
            data = json.load(f)

            # get all activities declaration withing the pipeline
            pipeline_activities = find_dict('activities', data)

            # iterate over declarations
            for alist in pipeline_activities:
                # iterate over pipelines
                for a in alist:
                    # continue only for dbx ntbs activities 
                    if not a['type'] == "DatabricksNotebook": continue   
                    ntb_n = a['typeProperties']['notebookPath']
                    # get value if required
                    if type(ntb_n) is dict: ntb_n = ntb_n['value']
                    # add adf file name if not present 
                    if not adf_fname in adf_ntb_executed_map:
                        adf_ntb_executed_map[adf_fname] = []
                    # add the notebooks name
                    adf_ntb_executed_map[adf_fname].append(ntb_n)
                    ntbs_set.add(ntb_n)
            
    # for each ntb estim its dbx name
    for ntb_fname in ntb_filenames:
        ntb_fname_dbx = convert_path_dbx_format(ntb_fname)
        if not '/' + ntb_fname_dbx in ntbs_set:
            return_flag = True
            print('! No pipeline found which executes the notebook {}'.format(ntb_fname))
    
    return return_flag


if __name__ == '__main__':
    exit(main())