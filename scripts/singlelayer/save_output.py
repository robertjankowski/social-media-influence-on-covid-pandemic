import numpy as np
import pandas as pd

from scripts.parameters import *


def format_parameters(l1_params: PhysicalLayerParameters,
                      n_runs: int,
                      n_steps: int,
                      n_agents: int,
                      comorbid_disease_A_fraction: float,
                      comorbid_disease_B_fraction: float):
    c = f'_FRAC_A={comorbid_disease_A_fraction}_FRAC_B={comorbid_disease_B_fraction}'
    return f'L1-{l1_params}' + c + f'_NRUNS={n_runs}' + f'_NSTEPS={n_steps}' + f'_NAGENTS={n_agents}'


def save_results(output_dead_rate: dict, output_infected_rate: dict, params1, params2, path: str):
    output_dead_rate = _format_result(output_dead_rate, params1, params2)
    output_infected_rate = _format_result(output_infected_rate, params1, params2)
    output_dead_rate.to_csv('dead_ratio_' + path)
    output_infected_rate.to_csv('infected_ratio_' + path)


def _format_result(output_results: dict, params1, params2):
    output_results = np.array(list(output_results.values())).reshape(len(params1), len(params2))
    output_results = pd.DataFrame(output_results, index=params1, columns=params2)
    return output_results
