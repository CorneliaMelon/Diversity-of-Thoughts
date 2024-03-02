import sys

import eval

res_json_dir = './'
filter_str = 'None'

results = eval.run_evaluations(res_json_dir, filter_str)


print(results)