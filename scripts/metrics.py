import networkx as nx
import numpy as np


def _get_degrees(g: nx.Graph) -> list:
    return list(dict(g.degree).values())


def pearson_coefficient_between_layers(g1: nx.Graph, g2: nx.Graph) -> float:
    """
    Return person correlation between layers for given two graphs

    r_{\alpha\beta} \in <-1, 1>

    :param g1: nx.Graph
    :param g2: nx.Graph
    :return: r_{\alpha\beta}
    """
    g1_degrees = _get_degrees(g1)
    g2_degrees = _get_degrees(g2)
    g1_sigma = np.std(g1_degrees)
    g2_sigma = np.std(g2_degrees)

    k_1_2 = np.mean([k1 * k2 for k1, k2 in zip(g1_degrees, g2_degrees)])
    k_1 = np.mean(g1_degrees)
    k_2 = np.mean(g2_degrees)
    top = k_1_2 - k_1 * k_2
    bottom = g1_sigma * g2_sigma
    return top / bottom
