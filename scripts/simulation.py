import random
import networkx as nx

import scripts.epidemic_layer as l1
import scripts.virtual_layer as l2
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
                        verbose=False):
    """
    Perform COVID-19 simulation on multilayer networks

    :param n_agents: number of agents in each layer
    :param n_additional_virtual_links: number of additional links in virtual layer
    :param init_infection_fraction: initial fraction of infected agents in physical layer
    :param init_aware_fraction: initial fraction of awared agents in virtual layer
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
    l1_layer, l2_layer = create_bilayer_network(n_agents, n_additional_virtual_links)
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
    _virtual_layer_step(step, random_node, l2_layer, l2_params, l2_voter_params, l2_social_media_params)
    _epidemic_layer_step(random_node, l1_layer, l2_layer, l1_params)


def _virtual_layer_step(step,
                        random_node,
                        l2_layer: nx.Graph,
                        l2_params: VirtualLayerParameters,
                        l2_voter_params: QVoterParameters,
                        l2_social_media_params: SocialMediaParameters):
    l2_node_status = l2.get_status(l2_layer, random_node)

    if step % l2_social_media_params.n == 0:  # the social media can influence agent
        if random.random() < l2_social_media_params.p_xi and l2_node_status == 'U':
            l2.set_aware(l2_layer, random_node)

    if l2_node_status == 'U':
        if random.random() < l2_params.p_lambda:
            l2.set_aware(l2_layer, random_node)
    elif l2_node_status == 'A':
        if random.random() < l2_params.p_delta:
            l2.set_unaware(l2_layer, random_node)
        else:
            # Voter model
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

    if l1_node_status == 'S':
        # Check if any neighbour is infected
        for neighbour in l1_layer.neighbors(random_node):
            if l1.get_status(l1_layer, neighbour) == 'I':
                # TODO: add age, gender ... to probability S -> I state !!!
                if random.random() < l1_params.p_beta:
                    l1.set_infected(l1_layer, random_node)
                    break
    elif l1_node_status == 'I':
        if l2.get_status(l2_layer, random_node) == 'U':
            l2.set_aware(l2_layer, random_node)
        if random.random() < l1_params.p_gamma:
            # TODO: add opinion ... to probability I -> Q state !!!
            l1.set_quarantined(l1_layer, random_node)
    elif l1_node_status == 'Q':
        # TODO: add age, gender, opinion ... to probability Q -> R|D state !!!
        if random.random() < l1_params.p_mu:
            l1.set_recovered(l1_layer, random_node)
        else:
            l1.set_dead(l1_layer, random_node)
