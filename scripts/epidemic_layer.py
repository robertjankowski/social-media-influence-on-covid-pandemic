import copy

import networkx as nx
import random

from scripts.age_statistics import generate_from_age_gender_distribution


def initialize_epidemic(g: nx.Graph, infected_fraction: float):
    """
    Initialize `l1` layer with `g.number_of_nodes() * infected_fraction` infected agents and the rest susceptible.

    Also initialize agents with age and gender.
    Age is randomly chosen from Polish population structure and gender with 50% probability

    :param g: nx.Graph l1 layer
    :param infected_fraction: a fraction of infected nodes at the onset
    :return g_copy: nx.Graph l1 layer with initialized agents
    """
    assert (g.number_of_nodes() % 2 == 0)  # odd number
    g_copy = copy.deepcopy(g)

    females_ages = generate_from_age_gender_distribution(g.number_of_nodes(), 'F')
    males_ages = generate_from_age_gender_distribution(g.number_of_nodes(), 'M')
    i = 0
    for node in g_copy.nodes:
        if random.random() < infected_fraction:
            set_infected(g_copy, node)
        else:
            set_susceptible(g_copy, node)

        if random.random() < 0.5:
            age = females_ages[i]
            gender = 'F'
        else:
            age = males_ages[i]
            gender = 'M'
        set_age(g_copy, node, age)
        set_gender(g_copy, node, gender)
        i += 1

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


def set_age(g: nx.Graph, node, age: int):
    g.nodes[node]['age'] = age


def set_gender(g: nx.Graph, node, gender: str):
    g.nodes[node]['gender'] = gender


def get_status(g: nx.Graph, node):
    return g.nodes[node]['l1_status']


def get_age(g: nx.Graph, node):
    return g.nodes[node]['age']


def get_gender(g: nx.Graph, node):
    return g.nodes[node]['gender']
