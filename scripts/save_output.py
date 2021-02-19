import numpy as np
import pandas as pd

from scripts.parameters import *


def format_parameters(l1_params: PhysicalLayerParameters,
                      l2_params: VirtualLayerParameters,
                      l2_voter_params: QVoterParameters,
                      l2_social_media_params: SocialMediaParameters,
                      n_runs: int,
                      n_steps: int,
                      n_agents: int,
                      n_additional_virtual_links: int):
    l2 = f'_L2-{l2_params}_{l2_voter_params}_{l2_social_media_params}'
    return f'L1-{l1_params}' + l2 + f'_NRUNS={n_runs}' + f'_NSTEPS={n_steps}' \
           + f'_NAGENTS={n_agents}' + f'_NLINKS={n_additional_virtual_links}'


def save_results(output_dead_rate: dict, output_infected_rate: dict, params1, params2, path: str):
    output_dead_rate = _format_result(output_dead_rate, params1, params2)
    output_infected_rate = _format_result(output_infected_rate, params1, params2)
    output_dead_rate.to_csv('dead_ratio_' + path)
    output_infected_rate.to_csv('infected_ratio_' + path)


def _format_result(output_results: dict, params1, params2):
    output_results = np.array(list(output_results.values())).reshape(len(params1), len(params2))
    output_results = pd.DataFrame(output_results, index=params1, columns=params2)
    return output_results
