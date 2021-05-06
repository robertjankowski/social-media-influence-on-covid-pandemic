import math
import random
import networkx as nx
import numpy as np
import copy

import scripts.epidemic_layer as l1
from scripts.age_statistics import death_rate_ratio
from scripts.network import create_bilayer_network
from scripts.parameters import *


def init_run_simulation(n_agents: int,
                        steps: int,
                        l1_params: PhysicalLayerParameters,
                        metrics: dict,
                        infected_fraction: float = 0.1,
                        comorbid_disease_A_fraction: float = 0.1,
                        comorbid_disease_B_fraction: float = 0.1,
                        network_m: int = 3,
                        network_p: int = 0.8,
                        verbose=False):
    """
    Perform COVID-19 simulation on single layer network

    :param n_agents: number of agents in each layer
    :param steps: number of simulation steps
    :param l1_params: parameters for l1_layer
    :param metrics: format e.g.: {'infected_ratio': ('l2_layer', infected_ratio), ... }
    :param infected_fraction: Fraction of infected agents
    :param comorbid_disease_A_fraction: fraction of agents having comorbidities B
    :param comorbid_disease_B_fraction: fraction of agents having comorbidities A
    :param network_m: The number of random edges to add for each new node
    :param network_p: Probability of adding the triangle after adding a random edge
    :param verbose: print simulation status
    :return: output_metrics: format: {'infected_ratio': [0.4, 0.55, 0.7, ...], ...}
    """
    l1_layer, _ = create_bilayer_network(n_agents, 0, m=network_m, p=network_p)
    l1_layer_init = l1.initialize_epidemic(l1_layer, comorbid_disease_A_fraction, comorbid_disease_B_fraction)
    l1_layer_init = initialize_bilayer_network(l1_layer_init, infected_fraction)
    return run(l1_layer_init,
               steps,
               l1_params,
               metrics,
               verbose)


def initialize_bilayer_network(l1_layer, infected_fraction):
    """
    Initialize infected fraction of agents

    :param l1_layer:
    :param infected_fraction:
    :return: l1_layer
    """
    l1_layer_copy = copy.deepcopy(l1_layer)
    N = nx.number_of_nodes(l1_layer)
    infected_size = math.floor(N * infected_fraction)
    infected_nodes = np.random.choice(N, size=infected_size)
    for i in infected_nodes:
        l1.set_infected(l1_layer_copy, i)
    return l1_layer_copy


def run(l1_layer: nx.Graph,
        steps: int,
        l1_params: PhysicalLayerParameters,
        metrics: dict,
        verbose=False):
    """
    Run `steps` of COVID-19 simulation on the physical (`l1_layer`) layer.

    :param l1_layer: physical layer
    :param l2_layer: virtual layer
    :param steps: number of simulation steps
    :param l1_params: parameters for l1_layer
    :param l2_voter_params: parameters for voter model in l2_layer
    :param l2_social_media_params: parameters for social media in l2_layer
    :param metrics: format e.g.:
                {'aware_ratio': ('l1_layer': aware_ratio), 'infected_ratio': ('l2_layer', infected_ratio), ... }
    :param verbose: print simulation status
    :return: output_metrics: format: {'infected_ratio': [0.4, 0.55, 0.7, ...], ...}
    """
    output_metrics = {m: [] for m in metrics.keys()}
    for step in range(steps):
        _single_step(l1_layer, l1_params)

        if verbose:
            _print_simulation_status(step, steps)

        for metrics_name, (layer, metrics_function) in metrics.items():
            if layer == 'l1_layer':
                output_metrics[metrics_name].append(metrics_function(l1_layer))
            else:
                print('Unsupported layer name')
                return

    return output_metrics, l1_layer


def _print_simulation_status(step: int, steps: int, num=10):
    if step % (steps / num) == 0:
        print('Step: {} / {}'.format(step, steps))


def _single_step(l1_layer: nx.Graph,
                 l1_params: PhysicalLayerParameters):
    N = l1_layer.number_of_nodes()
    random_node = random.randint(0, N - 1)
    _epidemic_layer_step(random_node, l1_layer, l1_params)


def _epidemic_layer_step(random_node, l1_layer: nx.Graph, l1_params: PhysicalLayerParameters):
    l1_node_status = l1.get_status(l1_layer, random_node)
    age = l1.get_age(l1_layer, random_node)
    is_disease_A = l1.get_comorbid_disease_A(l1_layer, random_node)
    is_disease_B = l1.get_comorbid_disease_B(l1_layer, random_node)

    if l1_node_status == 'S':
        # Check whether any neighbour is infected
        for neighbour in l1_layer.neighbors(random_node):
            if l1.get_status(l1_layer, neighbour) == 'I':
                if random.random() < _get_combined_beta_probability(l1_params.p_beta):
                    l1.set_infected(l1_layer, random_node)
                    break
    elif l1_node_status == 'I':
        l1.increment_infected_time_comorbid(l1_layer, random_node, is_disease_A, is_disease_B)
        if l1.get_infected_time(l1_layer, random_node) >= l1_params.max_infected_time:
            if random.random() < _get_combined_gamma_probability(l1_params.p_gamma):  # I -> Q
                l1.set_quarantined(l1_layer, random_node)
                # remove all links if agent goes into quarantined state
                links = list(l1_layer.edges(random_node))
                l1_layer.remove_edges_from(links)
            elif random.random() < _get_combined_kappa_probability(l1_params.p_kappa, age, is_disease_A,
                                                                   is_disease_B):  # I -> R
                l1.set_recovered(l1_layer, random_node)
            elif random.random() < _get_combined_mu_probability(l1_params.p_mu, age, is_disease_A,
                                                                is_disease_B):  # I -> D
                l1.set_dead(l1_layer, random_node)

    elif l1_node_status == 'Q':
        if random.random() < _get_combined_mu_probability(l1_params.p_mu, age, is_disease_A, is_disease_B):
            l1.set_recovered(l1_layer, random_node)
        elif random.random() < _get_combined_kappa_probability(l1_params.p_kappa, age, is_disease_A, is_disease_B):
            l1.set_dead(l1_layer, random_node)


def _get_combined_beta_probability(p_beta: float):
    """
    :param p_beta:
    :param opinion: positive opinion reduce the probability of infection
    :return: combined infected probability
    """
    return p_beta


def _get_combined_gamma_probability(p_gamma: float):
    """

    :param p_gamma:
    :return:
    """
    return p_gamma


def _get_combined_mu_probability(p_mu: float, age: int, is_disease_A: bool, is_disease_B: bool):
    """
    Decrease probability of recovery based on age death rate ratio.

    :param p_mu:
    :param age:
    :param opinion:
    :param is_disease_A:
    :param is_disease_B:
    """
    death_rate = death_rate_ratio(age)
    comoribidities_rate = _comorbid_rate(is_disease_A, is_disease_B)
    return p_mu * (1 - death_rate) / comoribidities_rate


def _get_combined_kappa_probability(p_kappa, age, is_disease_A: bool, is_disease_B: bool):
    """
    I -> R, Q -> R

    :param p_kappa:
    """
    comoribidities_rate = _comorbid_rate(is_disease_A, is_disease_B)
    death_rate = death_rate_ratio(age)
    return p_kappa * death_rate * comoribidities_rate


def _comorbid_rate(is_disease_A: bool, is_disease_B: bool):
    comoribidities_rate = 1.0
    if is_disease_A and is_disease_B:
        comoribidities_rate *= 3
    elif is_disease_A:
        comoribidities_rate *= 1.5
    elif is_disease_B:
        comoribidities_rate *= 2
    return comoribidities_rate
