from tabulate import tabulate
from pprint import pprint
import pandas as pd

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.regression_tests.models import config_multi_1, config_multi_2
from cadCAD import configs

exec_mode = ExecutionMode()

local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=configs)

# for config in multi_exp.configs:
#     print(config.__dict__['model_id'])
raw_result, tensor_fields, sessions = run.execute()
result = pd.DataFrame(raw_result)
# # print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
# # pprint(sessions)
print(tabulate(result, headers='keys', tablefmt='psql'))