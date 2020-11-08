import networkx as nx


def aware_ratio(g: nx.Graph):
    return _calculate_ratio(g, 'A')


def unaware_ratio(g: nx.Graph):
    return _calculate_ratio(g, 'U')


def mean_opinion(g: nx.Graph):
    size = nx.number_of_nodes(g)
    opinions = nx.get_node_attributes(g, 'l2_opinion').values()
    return sum(opinions) / size


def _calculate_ratio(g: nx.Graph, status: str):
    size = nx.number_of_nodes(g)
    statuses = nx.get_node_attributes(g, 'l2_status').values()
    count = sum([1 for s in statuses if s == status])
    return count / size
