import copy
import random

import networkx as nx


def create_bilayer_network(agents: int, additional_virtual_links: int, m=3, p=None):
    """
    Create bilayer network with additional `additional_virtual_links` in virtual layer.
    If p is None create simple BA network, otherwise use Holme and Kim algorithm with triad formation [1].

    [1] P. Holme and B. J. Kim, “Growing scale-free networks with tunable clustering”, Phys. Rev. E, 65, 026107, 2002.

    :param agents: number of individuals
    :param additional_virtual_links: number of additional edges in virtual layer
    :param m: starting number of nodes in the BA model
    :param p: probability of adding a triangle after adding a random edge
    :return: tuple (layer1, layer2)
    """
    if p is None:
        l1_layer = nx.barabasi_albert_graph(agents, m=m)
    else:
        l1_layer = nx.powerlaw_cluster_graph(agents, m=m, p=p)
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
    return degree_selected_nodes_size(g, dict(g.degree).values(), scale)


def degree_selected_nodes_size(g: nx.Graph, nodes, scale=10):
    sizes = dict(g.degree)
    return [scale * sizes[node] for node in nodes]
