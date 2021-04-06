from pprint import pprint
from typing import Dict, List, Any

# from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import env_trigger, var_substep_trigger, config_sim, psub_list
from simulations.regression_tests.experiments import param_sweep_exp, combo_exp


def some_function(x):
    return x

# Optional
# dict must contain lists opf 2 distinct lengths
g: Dict[str, List[Any]] = {
    'alpha': [1],
    'beta': [2, some_function],
    'gamma': [3, 4],
    'omega': [7]
}

psu_steps = ['m1', 'm2', 'm3']
system_substeps = len(psu_steps)
var_timestep_trigger = var_substep_trigger([0, system_substeps])
env_timestep_trigger = env_trigger(system_substeps)
env_process = {}


# ['s1', 's2', 's3', 's4']
# Policies per Mechanism
def gamma(_g, step, sL, s, **kwargs):
    return {'gamma': _g['gamma']}


def omega(_g, step, sL, s, **kwargs):
    return {'omega': _g['omega']}


# Internal States per Mechanism
def alpha(_g, step, sL, s, _input, **kwargs):
    return 'alpha', _g['alpha']


def beta(_g, step, sL, s, _input, **kwargs):
    return 'beta', _g['beta']


def policies(_g, step, sL, s, _input, **kwargs):
    return 'policies', _input


def sweeped(_g, step, sL, s, _input, **kwargs):
    return 'sweeped', {'beta': _g['beta'], 'gamma': _g['gamma']}

psu_block = {k: {"policies": {}, "variables": {}} for k in psu_steps}
for m in psu_steps:
    psu_block[m]['policies']['gamma'] = gamma
    psu_block[m]['policies']['omega'] = omega
    psu_block[m]["variables"]['alpha'] = alpha
    psu_block[m]["variables"]['beta'] = beta
    psu_block[m]['variables']['policies'] = policies
    psu_block[m]["variables"]['sweeped'] = var_timestep_trigger(y='sweeped', f=sweeped)


# Genesis States
genesis_states = {
    'alpha': 0,
    'beta': 0,
    'policies': {},
    'sweeped': {}
}

# Environment Process
env_process['sweeped'] = env_timestep_trigger(trigger_field='timestep', trigger_vals=[5], funct_list=[lambda _g, x: _g['beta']])


sim_config = config_sim(
    {
        "N": 2,
        "T": range(2),
        "M": g, # Optional
    }
)
# print()
# pprint(sim_config)
# exit()

# New Convention
partial_state_update_blocks = psub_list(psu_block, psu_steps)
# param_sweep_exp.append_configs(
#     model_id='param_sweep',
#     sim_configs=sim_config,
#     initial_state=genesis_states,
#     env_processes=env_process,
#     partial_state_update_blocks=partial_state_update_blocks
# )

combo_exp.append_configs(
    user_id='user_c',
    # model_id='param_sweep',
    sim_configs=sim_config,
    initial_state=genesis_states,
    env_processes=env_process,
    partial_state_update_blocks=partial_state_update_blocks
)
