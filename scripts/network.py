import copy
import random

import networkx as nx


def create_bilayer_network(agents: int, additional_virtual_links: int, m=5):
    """
    Create bilayer BA network with additional `additional_virtual_links` in virtual layer

    :param agents: number of individuals
    :param additional_virtual_links: number of additional edges in virtual layer
    :param m: starting number of nodes in the BA model
    :return: dict with two layers
    """
    l1_layer = nx.barabasi_albert_graph(agents, m=5)
    l2_layer = copy.deepcopy(l1_layer)
    l2_layer = add_edges_randomly(l2_layer, additional_virtual_links)
    return l1_layer, l2_layer


def add_edges_randomly(g: nx.Graph, n_edges: int):
    """
    Add randomly `n_edges` in `g` graph

    :param g: nx.Graph
    :param n_edges:
    :return: modified graph
    """
    new_edges = []
    for node in g.nodes:
        connected = [to for (fr, to) in g.edges(node)]
        unconnected = [n for n in g.nodes if n not in connected]

        if len(unconnected):
            if len(new_edges) < n_edges:
                new = random.choice(unconnected)
                g.add_edge(node, new)
                new_edges.append((node, new))
            else:
                break
    return g


def degree_node_size(g: nx.Graph, scale=10):
    """
    Create list of degree-based node sizes list
    :param g: nx.Graph
    :param scale: float
    :return:
    """
    d = dict(g.degree)
    return [scale * v for v in d.values()]
