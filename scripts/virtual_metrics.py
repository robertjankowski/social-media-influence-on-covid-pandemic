import networkx as nx
import numpy as np


def mean_opinion(g: nx.Graph):
    opinions = nx.get_node_attributes(g, 'l2_opinion').values()
    return np.mean(list(opinions))
