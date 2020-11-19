import numpy as np
import pandas as pd
from tqdm import tqdm

from scripts.simulation import init_run_simulation
from scripts.parameters import *
from scripts.epidemic_metrics import *
from scripts.virtual_metrics import *

DEFAULT_L1_PARAMS = PhysicalLayerParameters(0.2, 0.6, 0.999)
DEFAULT_L2_PARAMS = VirtualLayerParameters(0.4, 0.6)
DEFAULT_L2_VOTER_PARAMS = QVoterParameters(4, 0.1, 0.3)
DEFAULT_L2_SOCIAL_MEDIA_PARAMS = SocialMediaParameters(0.1, 1)

metrics = {'aware_ratio': ('l2_layer', aware_ratio),
           'unaware_ratio': ('l2_layer', unaware_ratio),
           'infected_ratio': ('l1_layer', infected_ratio),
           'dead_ratio': ('l1_layer', dead_ratio),
           'quarantined_ratio': ('l1_layer', quarantined_ratio),
           'recovered_ratio': ('l1_layer', recovered_ratio),
           'susceptible_ratio': ('l1_layer', susceptible_ratio),
           'mean_opinion': ('l2_layer', mean_opinion)}

N_AGENTS = 100
N_STEPS = 20000
N_ADDITIONAL_VIRTUAL_LINKS = 200
INIT_INFECTED_FRACTION = 0.05
INIT_AWARE_FRACTION = 0.05


def perform_simulation(l1_params=DEFAULT_L1_PARAMS,
                       l2_params=DEFAULT_L2_PARAMS,
                       l2_voter_params=DEFAULT_L2_VOTER_PARAMS,
                       l2_social_media_params=DEFAULT_L2_SOCIAL_MEDIA_PARAMS):
    return init_run_simulation(
        N_AGENTS,
        N_ADDITIONAL_VIRTUAL_LINKS,
        INIT_INFECTED_FRACTION,
        INIT_AWARE_FRACTION,
        N_STEPS,
        l1_params,
        l2_params,
        l2_voter_params,
        l2_social_media_params,
        metrics,
        verbose=True)


def beta_lambda_dead_experiment(resolution=100):
    """
    In this experiment, I would like to check how the probability of being infected (Beta)
        and the probability of becoming aware (Lambda) induce the toll of deaths.

    Beta: 0 - 1
    Lambda: 0 - 1
    """
    betas = np.linspace(0, 1, resolution)
    lambdas = np.linspace(0, 1, resolution)
    metrics = {'dead_ratio': ('l1_layer', dead_ratio), 'recovered_ratio': ('l1_layer', recovered_ratio)}

    l2_voter_params = QVoterParameters(4, 0.5, 0.3)
    l2_social_media_params = SocialMediaParameters(1e-10, 1e10)  # I remove social media
    dead_ratio_output = []
    recovered_ratio_output = []
    for b in tqdm(betas):
        dead_ratio_output_part = []
        recovered_ratio_output_part = []
        for l in lambdas:
            l1_params = PhysicalLayerParameters(b, 0.6, 0.9)
            l2_params = VirtualLayerParameters(l, 0.4)

            out, l1, l2 = init_run_simulation(N_AGENTS, N_ADDITIONAL_VIRTUAL_LINKS, INIT_INFECTED_FRACTION,
                                              INIT_AWARE_FRACTION, N_STEPS, l1_params, l2_params, l2_voter_params,
                                              l2_social_media_params, metrics)

            dead_ratio_output_part.append(out['dead_ratio'][-1])
            recovered_ratio_output_part.append(out['recovered_ratio'][-1])
        dead_ratio_output.append(dead_ratio_output_part)
        recovered_ratio_output.append(recovered_ratio_output_part)

    return betas, lambdas, dead_ratio_output, recovered_ratio_output


def gamma_lambda_dead_experiment(resolution=100):
    """
    In this experiment, I would like to check how the probability of going into qurantine (Gamma)
        and the probability of becoming aware (Lambda) induce the toll of deaths.

    Gamma: 0 - 1
    Lambda: 0 - 1
    """
    gammas = np.linspace(0, 1, resolution)
    lambdas = np.linspace(0, 1, resolution)
    metrics = {'dead_ratio': ('l1_layer', dead_ratio), 'recovered_ratio': ('l1_layer', recovered_ratio)}

    l2_voter_params = QVoterParameters(4, 0.5, 0.3)
    l2_social_media_params = SocialMediaParameters(1e-10, 1e10)  # I remove social media
    dead_ratio_output = []
    recovered_ratio_output = []
    for g in tqdm(gammas):
        dead_ratio_output_part = []
        recovered_ratio_output_part = []
        for l in lambdas:
            l1_params = PhysicalLayerParameters(0.3, g, 0.9)
            l2_params = VirtualLayerParameters(l, 0.4)

            out, l1, l2 = init_run_simulation(N_AGENTS, N_ADDITIONAL_VIRTUAL_LINKS, INIT_INFECTED_FRACTION,
                                              INIT_AWARE_FRACTION, N_STEPS, l1_params, l2_params, l2_voter_params,
                                              l2_social_media_params, metrics)

            dead_ratio_output_part.append(out['dead_ratio'][-1])
            recovered_ratio_output_part.append(out['recovered_ratio'][-1])
        dead_ratio_output.append(dead_ratio_output_part)
        recovered_ratio_output.append(recovered_ratio_output_part)

    return gammas, lambdas, dead_ratio_output, recovered_ratio_output


def gamma_p_dead_experiment(resolution=100):
    """
    In this experiment, I would like to check how the probability of going into qurantine (Gamma)
        and the probability of acting independently in voter model (p) induce the toll of deaths.

    p: 0 - 1
    Lambda: 0 - 1
    """
    gammas = np.linspace(0, 1, resolution)
    ps = np.linspace(0, 1, resolution)
    metrics = {'dead_ratio': ('l1_layer', dead_ratio),
               'recovered_ratio': ('l1_layer', recovered_ratio)}

    l2_params = VirtualLayerParameters(0.6, 0.4)
    l2_social_media_params = SocialMediaParameters(1e-10, 1e10)  # I remove social media
    dead_ratio_output = []
    recovered_ratio_output = []
    for g in tqdm(gammas):
        dead_ratio_output_part = []
        recovered_ratio_output_part = []
        for p in ps:
            l1_params = PhysicalLayerParameters(0.3, g, 0.9)
            l2_voter_params = QVoterParameters(4, p, 0.3)

            out, l1, l2 = init_run_simulation(N_AGENTS, N_ADDITIONAL_VIRTUAL_LINKS, INIT_INFECTED_FRACTION,
                                              INIT_AWARE_FRACTION, N_STEPS, l1_params, l2_params, l2_voter_params,
                                              l2_social_media_params, metrics)

            dead_ratio_output_part.append(out['dead_ratio'][-1])
            recovered_ratio_output_part.append(out['recovered_ratio'][-1])
        dead_ratio_output.append(dead_ratio_output_part)
        recovered_ratio_output.append(recovered_ratio_output_part)

    return gammas, ps, dead_ratio_output, recovered_ratio_output


def social_media_experiment(resolution=10, n_repeat_step=10):
    """
    In this experiment I will examine the social media influance on the toll of deaths.

    n: [0, 1, 10, 100, 1000]
    xi: 0 -- 1
    """
    social_media_n = [1e-10, 1, 10, 100, 1000]
    xis = np.linspace(0, 1, resolution)

    metrics = {'dead_ratio': ('l1_layer', dead_ratio), 'recovered_ratio': ('l1_layer', recovered_ratio)}
    l1_params = PhysicalLayerParameters(0.2, 0.6, 0.9)
    l2_params = VirtualLayerParameters(0.3, 0.4)
    l2_voter_params = QVoterParameters(4, 0.5, 0.3)

    dead_ratio_output = []
    recovered_ratio_output = []
    for n in tqdm(social_media_n):
        dead_ratio_output_xi = []
        recovered_ratio_output_xi = []
        for xi in xis:
            dead_ratio_output_part = []
            recovered_ratio_output_part = []

            # Run `n_repeat_step` and then average
            for _ in range(n_repeat_step):
                l2_social_media_params = SocialMediaParameters(xi, n)

                out, l1, l2 = init_run_simulation(N_AGENTS, N_ADDITIONAL_VIRTUAL_LINKS, INIT_INFECTED_FRACTION,
                                                  INIT_AWARE_FRACTION, N_STEPS, l1_params, l2_params, l2_voter_params,
                                                  l2_social_media_params, metrics)

                dead_ratio_output_part.append(out['dead_ratio'][-1])
                recovered_ratio_output_part.append(out['recovered_ratio'][-1])

            dead_ratio_output_xi.append(np.mean(dead_ratio_output_part))
            recovered_ratio_output_xi.append(np.mean(recovered_ratio_output_part))

        dead_ratio_output.append(dead_ratio_output_xi)
        recovered_ratio_output.append(recovered_ratio_output_xi)

    return social_media_n, xis, dead_ratio_output, recovered_ratio_output


def q_voter_experiment(qs: list, n_runs=10):
    metrics = {'dead_ratio': ('l1_layer', dead_ratio),
               'recovered_ratio': ('l1_layer', recovered_ratio),
               'infected_ratio': ('l1_layer', infected_ratio)}
    l1_params = PhysicalLayerParameters(0.2, 0.6, 0.9)
    l2_params = VirtualLayerParameters(0.3, 0.4)
    l2_social_media_params = SocialMediaParameters(0, 1e10)

    dr_output = []
    rr_output = []
    ir_output = []
    for q in tqdm(qs):
        dr = []
        rr = []
        ir = []
        for _ in range(n_runs):
            l2_voter_params = QVoterParameters(q, 0.5, 0.3)

            out, _, _ = init_run_simulation(N_AGENTS, N_ADDITIONAL_VIRTUAL_LINKS, INIT_INFECTED_FRACTION,
                                            INIT_AWARE_FRACTION, N_STEPS, l1_params, l2_params, l2_voter_params,
                                            l2_social_media_params, metrics)

            dr.append(out['dead_ratio'][-1])
            rr.append(out['recovered_ratio'][-1])
            ir.append(max(out['infected_ratio']))

        dr_output.append(dr)
        rr_output.append(rr)
        ir_output.append(ir)

    mean = lambda x: [np.mean(i) for i in x]
    std = lambda x: [np.std(i) for i in x]
    df = pd.DataFrame(data={'q': qs,
                            'mean_dead_ratio': mean(dr_output),
                            'std_dead_ratio': std(dr_output),
                            'mean_recovered_ratio': mean(rr_output),
                            'std_recovered_ratio': std(rr_output),
                            'mean_infected_ratio': mean(ir_output),
                            'std_infected_ratio': std(ir_output)})
    return df
