import argparse
import json
from typing import Optional
import re
from typing import Sequence
import json
# TODO: fix import 
from utils import (find_dict, get_adf_activity_execute_pipeline_name)

def main(argv: Optional[Sequence[str]] = None) -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    return_flag = False

    # split on adf and ntbs
    job_filenames = []
    pipelines_filenames = []
    for f in args.filenames:
        if re.match(".*/job_.*", f):
            job_filenames.append(f)
        else:
            pipelines_filenames.append(f)

    execute_pipeline_map = {}
    execute_pipeline_set = set()
    # for each pipeline get the executing ntb name
    for pipeline in pipelines_filenames:
        with open(pipeline) as f:
            data = json.load(f)
            
            # get all activities declaration withing the pipeline
            pipeline_activities = find_dict('activities', data)

            # iterate over declarations
            for alist in pipeline_activities:
                # iterate over pipelines
                for a in alist:
                    # get execute pipeline name 
                    execute_pipeline_name = get_adf_activity_execute_pipeline_name(a)
                    # continue of no pipeline is executed withing the activity
                    if not execute_pipeline_name: continue
                    # add adf file name if not present 
                    if not pipeline in execute_pipeline_map:
                        execute_pipeline_map[pipeline] = []
                    # add the notebooks name
                    execute_pipeline_map[pipeline].append(execute_pipeline_name)
                    execute_pipeline_set.add(execute_pipeline_name)
            
    # for each ntb estim its dbx name
    for job in job_filenames:
        # get activites name
        with open(job) as f:
            data = json.load(f)
            job_name = data['name']
            if not job_name in execute_pipeline_set:
                return_flag = True
                print('! No pipeline executing the job(pipeline) found {}'.format(job_name))
    
    return return_flag


if __name__ == '__main__':
    exit(main())