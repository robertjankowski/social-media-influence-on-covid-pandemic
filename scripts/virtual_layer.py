import copy

import networkx as nx
import random


def initialize_virtual(g: nx.Graph, negative_opinion_fraction: float = 0.5):
    """
    Initialize `l2` layer with `g.number_of_nodes() * aware_fraction` aware agents and the rest unaware.

    Opinions are chosen randomly from uniform distribution

    :param g: nx.Graph l2 layer
    :param negative_opinion_fraction: a fraction of negative opinions (default 50/50)
    :return g_copy: nx.Graph l2 layer with initialized agents
    """
    g_copy = copy.deepcopy(g)
    for node in g_copy.nodes:
        if random.random() < negative_opinion_fraction:
            set_negative_opinion(g_copy, node)
        else:
            set_positive_opinion(g_copy, node)
    return g_copy


def _set_opinion(g: nx.Graph, node, opinion: int):
    g.nodes[node]['l2_opinion'] = opinion


def set_positive_opinion(g: nx.Graph, node):
    _set_opinion(g, node, 1)


def set_negative_opinion(g: nx.Graph, node):
    _set_opinion(g, node, -1)


def get_opinion(g: nx.Graph, node):
    return g.nodes[node]['l2_opinion']


def flip_opinion(g: nx.Graph, node):
    opinion = get_opinion(g, node)
    if opinion == 1:
        set_negative_opinion(g, node)
    else:
        set_positive_opinion(g, node)
