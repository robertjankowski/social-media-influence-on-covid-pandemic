import math
import random
import networkx as nx
import numpy as np
import copy

import scripts.epidemic_layer as l1
import scripts.virtual_layer as l2
from scripts.age_statistics import death_rate_ratio
from scripts.network import create_bilayer_network
from scripts.parameters import *


def init_run_simulation(n_agents: int,
                        n_additional_virtual_links: int,
                        steps: int,
                        l1_params: PhysicalLayerParameters,
                        l2_voter_params: QVoterParameters,
                        l2_social_media_params: SocialMediaParameters,
                        metrics: dict,
                        infected_fraction: float = 0.1,
                        negative_opinion_fraction: float = 0.5,
                        network_m: int = 3,
                        network_p: int = 0.8,
                        verbose=False):
    """
    Perform COVID-19 simulation on multilayer networks

    :param n_agents: number of agents in each layer
    :param n_additional_virtual_links: number of additional links in virtual layer
    :param steps: number of simulation steps
    :param l1_params: parameters for l1_layer
    :param l2_voter_params: parameters for voter model in l2_layer
    :param l2_social_media_params: parameters for social media in l2_layer
    :param metrics: format e.g.:
                {'aware_ratio': ('l1_layer': aware_ratio), 'infected_ratio': ('l2_layer', infected_ratio), ... }
    :param infected_fraction: Fraction of infected agents
    :param negative_opinion_fraction: Fraction of agents with negative opinion
    :param network_m: The number of random edges to add for each new node
    :param network_p: Probability of adding the triangle after adding a random edge
    :param verbose: print simulation status
    :return: output_metrics: format: {'aware_ratio': [0.45, 0.4, ...], 'infected_ratio': [0.4, 0.55, 0.7, ...], ...}
             l1_layer and l2_layer
    """
    l1_layer, l2_layer = create_bilayer_network(n_agents, n_additional_virtual_links, m=network_m, p=network_p)
    l1_layer_init = l1.initialize_epidemic(l1_layer)
    l2_layer_init = l2.initialize_virtual(l2_layer, negative_opinion_fraction)
    l1_layer_init, l2_layer_init = initialize_bilayer_network(l1_layer_init, l2_layer_init, infected_fraction)
    return run(l1_layer_init,
               l2_layer_init,
               steps,
               l1_params,
               l2_voter_params,
               l2_social_media_params,
               metrics,
               verbose)


def initialize_bilayer_network(l1_layer, l2_layer, infected_fraction):
    """
    Create only one infected and aware agent!

    :param l1_layer:
    :param l2_layer:
    :param infected_fraction:
    :return: l1_layer, l2_layer
    """
    l1_layer_copy = copy.deepcopy(l1_layer)
    l2_layer_copy = copy.deepcopy(l2_layer)

    N = nx.number_of_nodes(l1_layer)
    infected_size = math.floor(N * infected_fraction)
    infected_nodes = np.random.choice(N, size=infected_size)
    for i in infected_nodes:
        l1.set_infected(l1_layer_copy, i)
    # infected_node = random.choice(list(range(1, nx.number_of_nodes(l1_layer_copy))))
    return l1_layer_copy, l2_layer_copy


def run(l1_layer: nx.Graph,
        l2_layer: nx.Graph,
        steps: int,
        l1_params: PhysicalLayerParameters,
        l2_voter_params: QVoterParameters,
        l2_social_media_params: SocialMediaParameters,
        metrics: dict,
        verbose=False):
    """
    Run `steps` of COVID-19 simulation on both physical (`l1_layer`) and virtual (`l2_layer`) layers.

    :param l1_layer: physical layer
    :param l2_layer: virtual layer
    :param steps: number of simulation steps
    :param l1_params: parameters for l1_layer
    :param l2_voter_params: parameters for voter model in l2_layer
    :param l2_social_media_params: parameters for social media in l2_layer
    :param metrics: format e.g.:
                {'aware_ratio': ('l1_layer': aware_ratio), 'infected_ratio': ('l2_layer', infected_ratio), ... }
    :param verbose: print simulation status
    :return: output_metrics: format: {'aware_ratio': [0.45, 0.4, ...], 'infected_ratio': [0.4, 0.55, 0.7, ...], ...}
             l1_layer and l2_layer
    """
    output_metrics = {m: [] for m in metrics.keys()}
    for step in range(steps):
        _single_step(step, l1_layer, l2_layer, l1_params, l2_voter_params, l2_social_media_params)

        if verbose:
            _print_simulation_status(step, steps)

        for metrics_name, (layer, metrics_function) in metrics.items():
            if layer == 'l1_layer':
                output_metrics[metrics_name].append(metrics_function(l1_layer))
            elif layer == 'l2_layer':
                output_metrics[metrics_name].append(metrics_function(l2_layer))
            else:
                print('Unsupported layer name')
                return

    return output_metrics, l1_layer, l2_layer


def _print_simulation_status(step: int, steps: int, num=10):
    if step % (steps / num) == 0:
        print('Step: {} / {}'.format(step, steps))


def _single_step(step,
                 l1_layer: nx.Graph,
                 l2_layer: nx.Graph,
                 l1_params: PhysicalLayerParameters,
                 l2_voter_params: QVoterParameters,
                 l2_social_media_params: SocialMediaParameters):
    N = l1_layer.number_of_nodes()
    random_node = random.randint(0, N - 1)
    _social_media_layer_step(step, l2_layer, l2_social_media_params)
    _virtual_layer_step(random_node, l2_layer, l2_voter_params)
    _epidemic_layer_step(random_node, l1_layer, l2_layer, l1_params)


def _social_media_layer_step(step, l2_layer: nx.Graph, l2_social_media_params: SocialMediaParameters):
    # Social media can influence every agent
    if step % l2_social_media_params.n == 0:
        for n in l2_layer.nodes:
            if random.random() < l2_social_media_params.p_xi:
                pass  # TODO: implement influence on opinion


def _virtual_layer_step(random_node,
                        l2_layer: nx.Graph,
                        l2_voter_params: QVoterParameters):
    if random.random() < l2_voter_params.p_p:
        _voter_act_non_conformity(random_node, l2_layer)
    else:
        _voter_act_conformity(random_node, l2_layer, l2_voter_params)


def _voter_act_non_conformity(random_node, l2_layer: nx.Graph):
    if random.random() < 0.5:
        l2.flip_opinion(l2_layer, random_node)


def _voter_act_conformity(random_node, l2_layer: nx.Graph, l2_voter_params: QVoterParameters):
    neighbours = list(l2_layer.neighbors(random_node))
    if len(neighbours) < 1:  # when the selected node is isolated
        return
    # Add the same neighbours if `random_node` does not have more than `q` neighbours
    while len(neighbours) < l2_voter_params.q:
        neighbours.append(random.choice(neighbours))
    neighbours_opinions = sum([l2.get_opinion(l2_layer, n) for n in neighbours])
    if neighbours_opinions == len(neighbours):
        l2.set_positive_opinion(l2_layer, random_node)
    elif neighbours_opinions == -len(neighbours):
        l2.set_negative_opinion(l2_layer, random_node)


def _epidemic_layer_step(random_node, l1_layer: nx.Graph, l2_layer: nx.Graph, l1_params: PhysicalLayerParameters):
    l1_node_status = l1.get_status(l1_layer, random_node)
    age = l1.get_age(l1_layer, random_node)
    opinion = l2.get_opinion(l2_layer, random_node)
    is_disease_A = l1.get_comorbid_disease_A(l1_layer, random_node)
    is_disease_B = l1.get_comorbid_disease_B(l1_layer, random_node)

    if l1_node_status == 'S':
        # Check whether any neighbour is infected
        for neighbour in l1_layer.neighbors(random_node):
            if l1.get_status(l1_layer, neighbour) == 'I':
                if random.random() < _get_combined_beta_probability(l1_params.p_beta, opinion):
                    l1.set_infected(l1_layer, random_node)
                    break
    elif l1_node_status == 'I':
        l1.increment_infected_time(l1_layer, random_node, opinion)
        if l1.get_infected_time(l1_layer, random_node) >= l1_params.max_infected_time:
            if random.random() < _get_combined_gamma_probability(l1_params.p_gamma):  # I -> Q
                l1.set_quarantined(l1_layer, random_node)
                # remove all links in both layers if agent goes into quarantined state
                links = list(l1_layer.edges(random_node))
                l1_layer.remove_edges_from(links)
                links = list(l2_layer.edges(random_node))
                l2_layer.remove_edges_from(links)
            elif random.random() < _get_combined_kappa_probability(l1_params.p_kappa, age):  # I -> R
                l1.set_recovered(l1_layer, random_node)
            elif random.random() < _get_combined_mu_probability(l1_params.p_mu, age, is_disease_A,
                                                                is_disease_B):  # I -> D
                l1.set_dead(l1_layer, random_node)

    elif l1_node_status == 'Q':
        if random.random() < _get_combined_mu_probability(l1_params.p_mu, age, is_disease_A, is_disease_B):
            l1.set_recovered(l1_layer, random_node)
        elif random.random() < _get_combined_kappa_probability(l1_params.p_kappa, age):
            l1.set_dead(l1_layer, random_node)


def _get_combined_beta_probability(p_beta: float, opinion):
    """
    :param p_beta:
    :param opinion: positive opinion reduce the probability of infection
    :return: combined infected probability
    """
    opinion_rate = 1
    if opinion == 1:
        opinion_rate /= 2

    return p_beta * opinion_rate


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

    # TODO: For not we neglect the comorbidity
    comoribidities_rate = 1.0
    if is_disease_A and is_disease_B:
        comoribidities_rate *= 1
    elif is_disease_A:
        comoribidities_rate *= 1
    elif is_disease_B:
        comoribidities_rate *= 1

    return p_mu * (1 - death_rate) / comoribidities_rate


def _get_combined_kappa_probability(p_kappa, age):
    """
    I -> R, Q -> R

    :param p_kappa:
    """
    death_rate = death_rate_ratio(age)
    return p_kappa * death_rate
