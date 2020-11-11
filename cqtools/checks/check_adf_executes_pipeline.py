import argparse
import json
from typing import Optional
import re
from typing import Sequence
from utils import convert_path_dbx_format
import json


def main(argv: Optional[Sequence[str]] = None) -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    return_flag = False

    # split on adf and ntbs
    job_filenames = []
    pipelines_filenames = []
    for f in args.filenames:
        if re.match(".*\/job_.*", f):
            job_filenames.append(f)
        else:
            pipelines_filenames.append(f)

    execute_pipeline_map = {}
    execute_pipeline_set = set()
    # for each pipeline get the executing ntb name
    for pipeline in pipelines_filenames:
        with open(pipeline) as f:
            data = json.load(f)

            pipeline_activities = data['properties']['activities']

            for a in pipeline_activities:
                
                # continue only for execute pipelines activities 
                if not a['type'] == "ExecutePipeline": continue   
                execute_pipeline_name = a['typeProperties']['pipeline']
                # get value if required
                if type(execute_pipeline_name) is dict:
                    execute_pipeline_name = execute_pipeline_name['referenceName']

                # add adf file name if not present 
                if not pipeline in execute_pipeline_map.keys():
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