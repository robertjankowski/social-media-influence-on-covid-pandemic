import random
import networkx as nx

import scripts.epidemic_layer as l1
import scripts.virtual_layer as l2
from scripts.age_statistics import death_rate_ratio
from scripts.network import create_bilayer_network
from scripts.parameters import *


def init_run_simulation(n_agents: int,
                        n_additional_virtual_links: int,
                        init_infection_fraction: float,
                        init_aware_fraction: float,
                        steps: int,
                        l1_params: PhysicalLayerParameters,
                        l2_params: VirtualLayerParameters,
                        l2_voter_params: QVoterParameters,
                        l2_social_media_params: SocialMediaParameters,
                        metrics: dict,
                        network_m: int = 3,
                        network_p: int = None,
                        verbose=False):
    """
    Perform COVID-19 simulation on multilayer networks

    :param n_agents: number of agents in each layer
    :param n_additional_virtual_links: number of additional links in virtual layer
    :param init_infection_fraction: initial fraction of infected agents in physical layer
    :param init_aware_fraction: initial fraction of aware agents in virtual layer
    :param steps: number of simulation steps
    :param l1_params: parameters for l1_layer
    :param l2_params: parameters for l2_layer
    :param l2_voter_params: parameters for voter model in l2_layer
    :param l2_social_media_params: parameters for social media in l2_layer
    :param metrics: format e.g.:
                {'aware_ratio': ('l1_layer': aware_ratio), 'infected_ratio': ('l2_layer', infected_ratio), ... }
    :param network_m: The number of random edges to add for each new node
    :param network_p: Probability of adding the triangle after adding a random edge
    :param verbose: print simulation status
    :return: output_metrics: format: {'aware_ratio': [0.45, 0.4, ...], 'infected_ratio': [0.4, 0.55, 0.7, ...], ...}
             l1_layer and l2_layer
    """
    l1_layer, l2_layer = create_bilayer_network(n_agents, n_additional_virtual_links, m=network_m, p=network_p)
    l1_layer_init = l1.initialize_epidemic(l1_layer, init_infection_fraction)
    l2_layer_init = l2.initialize_virtual(l2_layer, init_aware_fraction)
    return run(l1_layer_init,
               l2_layer_init,
               steps,
               l1_params,
               l2_params,
               l2_voter_params,
               l2_social_media_params,
               metrics,
               verbose)


def run(l1_layer: nx.Graph,
        l2_layer: nx.Graph,
        steps: int,
        l1_params: PhysicalLayerParameters,
        l2_params: VirtualLayerParameters,
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
    :param l2_params: parameters for l2_layer
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
        _single_step(step, l1_layer, l2_layer, l1_params, l2_params, l2_voter_params, l2_social_media_params)

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
                 l2_params: VirtualLayerParameters,
                 l2_voter_params: QVoterParameters,
                 l2_social_media_params: SocialMediaParameters):
    N = l1_layer.number_of_nodes()
    random_node = random.randint(0, N - 1)
    _social_media_layer_step(step, l2_layer, l2_social_media_params)
    _virtual_layer_step(random_node, l2_layer, l2_params, l2_voter_params)
    _epidemic_layer_step(random_node, l1_layer, l2_layer, l1_params)


def _social_media_layer_step(step, l2_layer: nx.Graph, l2_social_media_params: SocialMediaParameters):
    # Social media can influence every agent
    if step % l2_social_media_params.n == 0:
        for n in l2_layer.nodes:
            if random.random() < l2_social_media_params.p_xi:
                l2.set_aware(l2_layer, n)


def _virtual_layer_step(random_node,
                        l2_layer: nx.Graph,
                        l2_params: VirtualLayerParameters,
                        l2_voter_params: QVoterParameters):
    l2_node_status = l2.get_status(l2_layer, random_node)

    if l2_node_status == 'U':
        # When one neighbour of the agent is aware, he can influence that agent.
        for neighbour in l2_layer.neighbors(random_node):
            if l2.get_status(l2_layer, neighbour) == 'A':
                if random.random() < l2_params.p_lambda:
                    l2.set_aware(l2_layer, random_node)
                    break
    elif l2_node_status == 'A':
        if random.random() < l2_params.p_delta:
            l2.set_unaware(l2_layer, random_node)
    # run Voter model even though the agent is in UNAWARE state
    if random.random() < l2_voter_params.p_p:
        _voter_act_non_conformity(random_node, l2_layer)
    else:
        _voter_act_conformity(random_node, l2_layer, l2_voter_params)


def _voter_act_non_conformity(random_node, l2_layer: nx.Graph):
    if random.random() < 0.5:
        l2.flip_opinion(l2_layer, random_node)


def _voter_act_conformity(random_node, l2_layer: nx.Graph, l2_voter_params: QVoterParameters):
    neighbours = list(l2_layer.neighbors(random_node))
    # Add the same neighbours if `random_node` does not have more than `q` neighbours
    while len(neighbours) < l2_voter_params.q:
        neighbours.append(random.choice(neighbours))
    neighbours_opinions = sum([l2.get_opinion(l2_layer, n) for n in neighbours])
    if neighbours_opinions == len(neighbours):
        l2.set_positive_opinion(l2_layer, random_node)
    elif neighbours_opinions == -len(neighbours):
        l2.set_negative_opinion(l2_layer, random_node)
    else:
        if random.random() < l2_voter_params.p_epsilon:
            l2.flip_opinion(l2_layer, random_node)


def _epidemic_layer_step(random_node, l1_layer: nx.Graph, l2_layer: nx.Graph, l1_params: PhysicalLayerParameters):
    l1_node_status = l1.get_status(l1_layer, random_node)
    age = l1.get_age(l1_layer, random_node)
    gender = l1.get_gender(l1_layer, random_node)
    opinion = l2.get_opinion(l2_layer, random_node)

    if l1_node_status == 'S':
        # Check whether any neighbour is infected
        for neighbour in l1_layer.neighbors(random_node):
            if l1.get_status(l1_layer, neighbour) == 'I':
                if random.random() < _get_combined_beta_probability(l1_params.p_beta, age, gender):
                    l1.set_infected(l1_layer, random_node)
                    break
    elif l1_node_status == 'I':
        if l2.get_status(l2_layer, random_node) == 'U':
            l2.set_aware(l2_layer, random_node)

        if random.random() < _get_combined_gamma_probability(l1_params.p_gamma, opinion):
            l1.set_quarantined(l1_layer, random_node)
    elif l1_node_status == 'Q':
        if random.random() < _get_combined_mu_probability(l1_params.p_mu, age, opinion):
            l1.set_recovered(l1_layer, random_node)
        else:
            l1.set_dead(l1_layer, random_node)


def _get_combined_beta_probability(p_beta: float, age: int, gender: str):
    """
    Based on: https://publications.jrc.ec.europa.eu/repository/bitstream/JRC120680/gender_territory_covid19_online.pdf

    Children are more likely to spread disease (e.g. school, colleagues).
    Women are more likely to get infected due to the fact that more women are working in the health sector.

    :param p_beta:
    :param age:
    :param gender:
    :return: combined infected probability
    """
    if age < 30:
        age_rate = 1.1
    else:
        age_rate = 0.9

    if gender == 'F':
        gender_rate = 1.0  # For now gender does not modify any probability
    elif gender == 'M':
        gender_rate = 1.0

    return p_beta * age_rate * gender_rate


def _get_combined_gamma_probability(p_gamma: float, opinion: int):
    """
    Decrease probability (I -> Q) when agent has negative opinion when it comes to social distancing

    :param p_gamma:
    :param opinion:
    :return:
    """
    if opinion == 1:
        opinion_rate = 1.0
    elif opinion == -1:
        opinion_rate = 0.5

    return p_gamma * opinion_rate


def _get_combined_mu_probability(p_mu: float, age: int, opinion: int):
    """
    Decrease probability of recovery based on age death rate ratio and
    when agent has negative opinion when it comes to staying in quarantine.


    :param p_mu:
    :param age:
    :param opinion:
    """
    death_rate = death_rate_ratio(age)

    if opinion == 1:
        opinion_rate = 1.0
    elif opinion == -1:
        opinion_rate = 0.5
    return p_mu * opinion_rate * (1 - death_rate)
