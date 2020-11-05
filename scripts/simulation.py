import networkx as nx
import random

from scripts.parameters import *
import scripts.epidemic_layer as l1
import scripts.virtual_layer as l2


def run(l1_layer: nx.Graph,
        l2_layer: nx.Graph,
        steps: int,
        l1_params: PhysicalLayerParameters,
        l2_params: VirtualLayerParameters,
        l2_voter_params: QVoterParameters,
        l2_social_media_params: SocialMediaParameters):
    for step in range(steps):
        _single_step(step, l1_layer, l2_layer, l1_params, l2_params, l2_voter_params, l2_social_media_params)
        # TODO: calculate metrics of each layer

    # return metrics ??


def _single_step(step,
                 l1_layer: nx.Graph,
                 l2_layer: nx.Graph,
                 l1_params: PhysicalLayerParameters,
                 l2_params: VirtualLayerParameters,
                 l2_voter_params: QVoterParameters,
                 l2_social_media_params: SocialMediaParameters):
    N = l1_layer.number_of_nodes()
    random_node = random.randint(N)
    _virtual_layer_step(step, random_node, l2_layer, l2_params, l2_voter_params, l2_social_media_params)
    _epidemic_layer_step(random_node, l1_layer, l2_layer, l1_params)


def _virtual_layer_step(step,
                        random_node,
                        l2_layer: nx.Graph,
                        l2_params: VirtualLayerParameters,
                        l2_voter_params: QVoterParameters,
                        l2_social_media_params: SocialMediaParameters):
    l2_node_status = l2.get_status(l2_layer, random_node)

    if l2_social_media_params.n % step == 0:  # the social media can influence agent
        if random.random() < l2_social_media_params.p_xi and l2_node_status == 'U':
            l2.set_aware(l2_layer, random_node)

    if l2_node_status == 'U':
        if random.random() < l2_params.p_lambda:
            l2.set_aware(l2_layer, random_node)
    elif l2_node_status == 'A':
        if random.random() < l2_params.p_delta:
            l2.set_unaware(l2_layer, random_node)
        else:
            # TODO - perform q voter model
            pass


def _epidemic_layer_step(random_node, l1_layer: nx.Graph, l2_layer: nx.Graph, l1_params: PhysicalLayerParameters):
    l1_node_status = l1.get_status(l1_layer, random_node)

    if l1_node_status == 'S':
        # Check if any neighbour is infected
        for neighbour in l1_layer.neighbors(random_node):
            if l1.get_status(l1_layer, neighbour) == 'I':
                # TODO: add age, gender, ... to probability S -> I state !!!
                if random.random() < l1_params.p_beta:
                    l1.set_infected(l1_layer, random_node)
                    break
    elif l1_node_status == 'I':
        if l2.get_status(l2_layer, random_node) == 'U':
            l2.set_aware(l2_layer, random_node)

        if random.random() < l1_params.p_gamma:
            l1.set_quarantined(l2_layer, random_node)
    elif l1_node_status == 'Q':
        # TODO: add age, gender, ... to probability Q -> R|D state !!!
        if random.random() < l1_params.p_mu:
            l1.set_recovered(l2_layer, random_node)
        else:
            l1.set_dead(l2_layer, random_node)
