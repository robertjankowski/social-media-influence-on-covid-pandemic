import networkx as nx


def infected_ratio(g: nx.Graph):
    return _calculate_ratio(g, 'I')


def susceptible_ratio(g: nx.Graph):
    return _calculate_ratio(g, 'S')


def dead_ratio(g: nx.Graph):
    return _calculate_ratio(g, 'D')


def recovered_ratio(g: nx.Graph):
    return _calculate_ratio(g, 'R')


def quarantined_ratio(g: nx.Graph):
    return _calculate_ratio(g, 'Q')


def _calculate_ratio(g: nx.Graph, status: str):
    size = nx.number_of_nodes(g)
    statuses = nx.get_node_attributes(g, 'l1_status').values()
    count = sum([1 for s in statuses if s == status])
    return count / size
