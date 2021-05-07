import itertools
import logging
import math
import multiprocessing as mp
import time
from collections import ChainMap
from typing import Callable
from logger_tt import setup_logging, logger

import numpy as np

from scripts.singlelayer.constants import SimulationConstants
from scripts.epidemic_metrics import *
from scripts.parameters import *
from scripts.singlelayer.save_output import format_parameters, save_results
from scripts.singlelayer.simulation import init_run_simulation


def run_parallel(params1: list,
                 params2: list,
                 filename: str,
                 experiment_fun: Callable,
                 l1_params: PhysicalLayerParameters = None,
                 metrics: dict = None,
                 n_agents: int = None,
                 n_steps: int = None,
                 comorbid_disease_A_fraction: float = None,
                 comorbid_disease_B_fraction: float = None,
                 n_runs=100,
                 cpus=mp.cpu_count()):
    """
    Perform simulations in parallel

    :param params1: list of parameters
    :param params2: list of parameters
    :param filename: output file name prefix
    :param experiment_fun: function to execute in parallel (see more in `example_experiment` function)
    :param l1_params:
    :param metrics:
    :param n_agents:
    :param n_steps:
    :param comorbid_disease_A_fraction:
    :param comorbid_disease_B_fraction:
    :param constants:
    :param n_runs: number of realizations of each run
    :param cpus: number of threads (default max number)
    """
    if metrics is None:
        metrics = {'dead_ratio': ('l1_layer', dead_ratio),
                   'infected_ratio': ('l1_layer', infected_ratio)}

    updated_constants = SimulationConstants(n_agents, n_steps, l1_params, comorbid_disease_A_fraction,
                                            comorbid_disease_B_fraction)

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
    parameters_name = filename + '_' + format_parameters(updated_constants.l1_params,
                                                         n_runs,
                                                         updated_constants.n_steps,
                                                         updated_constants.n_agents,
                                                         updated_constants.comorbid_disease_A_fraction,
                                                         updated_constants.comorbid_disease_B_fraction) + '.csv'
    save_results(output_dead_rate, output_infected_rate, params1, params2, parameters_name)
    end = time.time()
    logger.info(f'Elapsed: {end - start} s')


def example_experiment(beta_gamma: list, params: dict):
    """
    Example function to run in parallel

    :param beta_gamma: parameters in format: [(beta1, gamma1), (beta2, gamma2), ...]
    :param params: dictionary with all possible parameters (see variable `all_parameters` in `run_parallel` function)
    :return: tuple of dead and infected ratio for every parameters
    """
    output_dead_rate = {}
    output_infected_rate = {}
    constants = params['constants']
    for beta, gamma in beta_gamma:
        print(f'Running beta={beta}, gamma={gamma} in process {mp.current_process().name}')
        dead_rate = []
        infected_rate = []
        for _ in range(params['n_runs']):
            l1_params = PhysicalLayerParameters(beta, gamma, constants.l1_params.p_mu, constants.l1_params.p_kappa,
                                                constants.l1_params.max_infected_time)
            out, _, = init_run_simulation(constants.n_agents,
                                          constants.n_steps,
                                          l1_params,
                                          params['metrics'],
                                          comorbid_disease_A_fraction=constants.comorbid_disease_A_fraction,
                                          comorbid_disease_B_fraction=constants.comorbid_disease_B_fraction)

            dead_rate.append(out['dead_ratio'][-1])
            infected_rate.append(max(out['infected_ratio']))
        output_dead_rate[(beta, gamma)] = np.mean(dead_rate)
        output_infected_rate[(beta, gamma)] = np.mean(infected_rate)
    return output_dead_rate, output_infected_rate


if __name__ == '__main__':
    setup_logging(full_context=1, suppress_level_below=logging.DEBUG, use_multiprocessing=True)
    beta = np.linspace(0.01, 0.99, num=50)
    gamma = [0.5]
    run_parallel(beta, gamma, 'beta_gamma_v1', example_experiment, n_runs=1, cpus=50,
                 n_agents=10000, n_steps=200000,
                 comorbid_disease_A_fraction=0,
                 comorbid_disease_B_fraction=0)
