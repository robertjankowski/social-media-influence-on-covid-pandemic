import itertools
import math
import multiprocessing as mp
import time
from collections import ChainMap
from typing import Callable

import numpy as np

from scripts.constants import SimulationConstants
from scripts.epidemic_metrics import *
from scripts.parameters import *
from scripts.save_output import format_parameters, save_results
from scripts.simulation import init_run_simulation


def run_parallel(params1: list,
                 params2: list,
                 filename: str,
                 experiment_fun: Callable,
                 l1_params: PhysicalLayerParameters = None,
                 l2_voter_params: QVoterParameters = None,
                 l2_social_media_params: SocialMediaParameters = None,
                 metrics: dict = None,
                 n_agents: int = None,
                 n_steps: int = None,
                 frac_additional_virtual_links: float = None,
                 constants: SimulationConstants = SimulationConstants(),
                 n_runs=100,
                 cpus=mp.cpu_count()):
    """
    Perform simulations in parallel

    :param params1: list of parameters
    :param params2: list of parameters
    :param filename: output file name prefix
    :param experiment_fun: function to execute in parallel (see more in `example_experiment` function)
    :param l1_params:
    :param l2_voter_params:
    :param l2_social_media_params:
    :param metrics:
    :param n_agents:
    :param n_steps:
    :param frac_additional_virtual_links:
    :param constants:
    :param n_runs: number of realizations of each run
    :param cpus: number of threads (default max number)
    """
    if metrics is None:
        metrics = {'dead_ratio': ('l1_layer', dead_ratio),
                   'infected_ratio': ('l1_layer', infected_ratio)}
    if l1_params is None:
        l1_params = constants.L1_DEFAULT_PARAMS
    if l2_voter_params is None:
        l2_voter_params = constants.L2_VOTER_DEFAULT_PARAMS
    if l2_social_media_params is None:
        l2_social_media_params = constants.L2_SOCIAL_MEDIA_DEFAULT_PARAMS
    if n_agents is None:
        n_agents = constants.N_AGENTS
    if n_steps is None:
        n_steps = constants.N_STEPS
    if frac_additional_virtual_links is None:
        frac_additional_virtual_links = constants.FRAC_ADDITIONAL_VIRTUAL_LINKS

    updated_constants = SimulationConstants(n_agents, n_steps, frac_additional_virtual_links,
                                            l1_params, l2_voter_params, l2_social_media_params)

    params_all = list(itertools.product(params1, params2))
    length = math.ceil(len(params_all) / cpus)
    params_chunks = []
    for i in range(cpus):
        start_idx = i * length
        end_idx = (i + 1) * length
        to_add = params_all[start_idx:end_idx]
        if len(to_add) > 0:
            params_chunks.append(to_add)

    all_parameters = {
        'constants': updated_constants,
        'metrics': metrics,
        'n_runs': n_runs
    }
    all_parameters = [[p, all_parameters] for p in params_chunks]

    output_dead_rate = []
    output_infected_rate = []
    start = time.time()
    with mp.Pool(cpus) as pool:
        for tmp_dead_rate, tmp_infected_rate in pool.starmap(experiment_fun, all_parameters):
            output_dead_rate.append(tmp_dead_rate)
            output_infected_rate.append(tmp_infected_rate)

    output_dead_rate = dict(ChainMap(*output_dead_rate))
    output_infected_rate = dict(ChainMap(*output_infected_rate))
    parameters_name = filename + '_' + format_parameters(l1_params, l2_voter_params, l2_social_media_params,
                                                         n_runs, n_steps, n_agents, frac_additional_virtual_links) + '.csv'
    save_results(output_dead_rate, output_infected_rate, params1, params2, parameters_name)
    end = time.time()
    print(f'Elapsed: {end - start} s')


def example_experiment(qs_ps: list, params: dict):
    """
    Example function to run in parallel

    :param qs_ps: parameters in format: [(q1, p1), (q2, p2), ...]
    :param params: dictionary with all possible parameters (see variable `all_parameters` in `run_parallel` function)
    :return: tuple of dead and infected ratio for every parameters
    """
    output_dead_rate = {}
    output_infected_rate = {}
    constants = params['constants']
    for q, p in qs_ps:
        print(f'Running q={q}, p={p} in process {mp.current_process().name}')
        dead_rate = []
        infected_rate = []
        for _ in range(params['n_runs']):
            q_voter_parameters = QVoterParameters(q, p)

            out, _, _ = init_run_simulation(constants.n_agents,
                                            constants.n_additional_virtual_links,
                                            constants.n_steps,
                                            constants.l1_params,
                                            q_voter_parameters,
                                            constants.l2_social_media_params,
                                            params['metrics'])
            dead_rate.append(out['dead_ratio'][-1])
            infected_rate.append(max(out['infected_ratio']))
        output_dead_rate[(p, q)] = np.mean(dead_rate)
        output_infected_rate[(p, q)] = np.mean(infected_rate)
    return output_dead_rate, output_infected_rate


if __name__ == '__main__':
    qs = [3, 4, 5, 6, 7]
    ps = [0.1, 0.2, 0.3, 0.4]
    run_parallel(qs, ps, 'p_q', example_experiment, l1_params=PhysicalLayerParameters(0.4, 0.2, 0.9, 0.05, 10),
                 n_agents=100, n_steps=1000, cpus=8)
