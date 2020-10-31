import copy

import networkx as nx
import random


def initialize_epidemic(g: nx.Graph, infected_fraction: float):
    """
    Initialize `l1` layer with `g.number_of_nodes() * infected_fraction` infected agents and the rest susceptible

    :param g: nx.Graph l1 layer
    :param infected_fraction: a fraction of infected nodes at the onset
    :return g_copy: nx.Graph l1 layer with initialized agents
    """
    g_copy = copy.deepcopy(g)
    for node in g_copy.nodes:
        if random.random() < infected_fraction:
            set_infected(g_copy, node)
        else:
            set_susceptible(g_copy, node)
    return g_copy


def _set_status(g: nx.Graph, node, status: str):
    g.nodes[node]['l1_status'] = status


def set_susceptible(g: nx.Graph, node):
    _set_status(g, node, 'S')


def set_infected(g: nx.Graph, node):
    _set_status(g, node, 'I')


def set_quarantined(g: nx.Graph, node):
    _set_status(g, node, 'Q')


def set_recovered(g: nx.Graph, node):
    _set_status(g, node, 'R')


def set_dead(g: nx.Graph, node):
    _set_status(g, node, 'D')
