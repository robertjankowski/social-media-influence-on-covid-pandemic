import copy

import networkx as nx
import random


def initialize_virtual(g: nx.Graph, aware_fraction: float):
    """
    Initialize `l2` layer with `g.number_of_nodes() * aware_fraction` aware agents and the rest unaware.

    Opinions are chosen randomly from uniform distribution

    :param g: nx.Graph l2 layer
    :param aware_fraction: a fraction of aware nodes at the onset
    :return g_copy: nx.Graph l2 layer with initialized agents
    """
    g_copy = copy.deepcopy(g)
    for node in g_copy.nodes:
        if random.random() < aware_fraction:
            set_aware(g_copy, node)
        else:
            set_unaware(g_copy, node)

        if random.random() < 0.5:
            set_negative_opinion(g_copy, node)
        else:
            set_positive_opinion(g_copy, node)

    return g_copy


def _set_status(g: nx.Graph, node, status: str):
    g.nodes[node]['l2_status'] = status


def _set_opinion(g: nx.Graph, node, opinion: int):
    g.nodes[node]['l2_opinion'] = opinion


def set_aware(g: nx.Graph, node):
    _set_status(g, node, 'A')


def set_unaware(g: nx.Graph, node):
    _set_status(g, node, 'U')


def set_positive_opinion(g: nx.Graph, node):
    _set_opinion(g, node, 1)


def set_negative_opinion(g: nx.Graph, node):
    _set_opinion(g, node, -1)


def get_status(g: nx.Graph, node):
    return g.nodes[node]['l2_status']


def get_opinion(g: nx.Graph, node):
    return g.nodes[node]['l2_opinion']


def flip_opinion(g: nx.Graph, node):
    opinion = get_opinion(g, node)
    if opinion == 1:
        set_negative_opinion(g, node)
    else:
        set_positive_opinion(g, node)
