import matplotlib.pyplot as plt
import networkx as nx
import sys
import seaborn as sns

sys.path.append("../")

from scripts.network import degree_node_size

DEFAULT_CONFIG = {
    'font.size': 15,
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans']
}


def load_matplotlib():
    plt.rcParams.update(DEFAULT_CONFIG)
    plt.rc('text', usetex=True)
    plt.rc('figure', figsize=(8, 6))


def save_figure(filename: str):
    """
    Save matplotlib figure in correct extension
    :param filename: Name of output plot
    """
    extension = filename.split('.')[-1]
    if extension == "png":
        plt.savefig(filename, bbox_inches='tight', dpi=300)
    elif extension == "pdf" or extension == "svg":
        plt.savefig(filename, bbox_inches='tight')
    else:
        print('Error. Cannot save figure, unsupported extension: [{}]'.format(extension))


def draw_network(g: nx.Graph, ax=None, pos=None, node_size_list=None, node_size_scale=10,
                 edge_alpha=0.1, node_border_color='black', node_border_width=0.5):
    """
    Draw nx.Graph on matplotlib axis
    :param g: nx.Graph
    :param ax: matplotlib canvas
    :param pos: position of nodes (e.g. from nx.spring_layout(g))
    :param node_size_list: list of node sizes
    :param edge_alpha: float
    :param node_border_color: float
    :param node_border_width: float
    """
    if pos is None:
        pos = nx.spring_layout(g)
    if node_size_list is None:
        node_size_list = degree_node_size(g, node_size_scale)
    nx.draw_networkx_edges(g, ax=ax, alpha=edge_alpha, pos=pos, connectionstyle='arc3, rad = 0.1')
    nx.draw_networkx_nodes(g, node_size=node_size_list, ax=ax, pos=pos,
                           edgecolors=node_border_color, linewidths=node_border_width)


def draw_epidemic_layer(g: nx.Graph, ax=None, pos=None, node_size_scale=10, edge_alpha=0.1,
                        node_border_color='black', node_border_width=0.5):
    if pos is None:
        pos = nx.spring_layout(g)

    susceptible_nodes = []
    infected_nodes = []
    quarantined_nodes = []
    recovered_nodes = []
    dead_nodes = []
    for node in g.nodes:
        node_status = g.nodes[node]['l1_status']
        if node_status is None:
            print('Node should have `l1_status` field. Exiting...')
            return

        if node_status == 'S':
            susceptible_nodes.append(node)
        elif node_status == 'I':
            infected_nodes.append(node)
        elif node_status == 'Q':
            quarantined_nodes.append(node)
        elif node_status == 'R':
            recovered_nodes.append(node)
        elif node_status == 'D':
            dead_nodes.append(node)

    sizes = dict(g.degree)
    susceptible_nodes_sizes = [node_size_scale * sizes[node] for node in susceptible_nodes]
    infected_nodes_sizes = [node_size_scale * sizes[node] for node in infected_nodes]
    quarantined_nodes_sizes = [node_size_scale * sizes[node] for node in quarantined_nodes]
    recovered_nodes_sizes = [node_size_scale * sizes[node] for node in recovered_nodes]
    dead_nodes_sizes = [node_size_scale * sizes[node] for node in dead_nodes]

    nx.draw_networkx_edges(g, ax=ax, alpha=edge_alpha, pos=pos, connectionstyle='arc3,rad=0.1',
                           arrowstyle='<->')
    # Susceptible nodes
    nx.draw_networkx_nodes(g, nodelist=susceptible_nodes, node_size=susceptible_nodes_sizes,
                           node_color='orange', ax=ax, pos=pos, edgecolors=node_border_color,
                           linewidths=node_border_width, label='susceptible')
    # Infected nodes
    nx.draw_networkx_nodes(g, nodelist=infected_nodes, node_size=infected_nodes_sizes,
                           node_color='lightblue', ax=ax, pos=pos, edgecolors=node_border_color,
                           linewidths=node_border_width, label='infected')

    # Quarantined nodes
    nx.draw_networkx_nodes(g, nodelist=quarantined_nodes, node_size=quarantined_nodes_sizes,
                           node_color='brown', ax=ax, pos=pos, edgecolors=node_border_color,
                           linewidths=node_border_width, label='quarantined')

    # Recovered nodes
    nx.draw_networkx_nodes(g, nodelist=recovered_nodes, node_size=recovered_nodes_sizes,
                           node_color='green', ax=ax, pos=pos, edgecolors=node_border_color,
                           linewidths=node_border_width, label='recovered')

    # Dead nodes
    nx.draw_networkx_nodes(g, nodelist=dead_nodes, node_size=dead_nodes_sizes,
                           node_color='black', ax=ax, pos=pos, edgecolors=node_border_color,
                           linewidths=node_border_width, label='dead')


def draw_virtual_layer(g: nx.Graph, ax=None, pos=None, node_size_scale=10, edge_alpha=0.1,
                       node_border_color='black', node_border_width=0.5):
    if pos is None:
        pos = nx.spring_layout(g)

    aware_nodes = []
    unaware_nodes = []
    nodes_opinions = {k: v['l2_opinion'] for k, v in dict(g.nodes(data=True)).items()}

    for node in g.nodes:
        node_status = g.nodes[node]['l2_status']
        if node_status is None:
            print('Node should have `l2_status` field. Exiting...')
            return

        if node_status == 'A':
            aware_nodes.append(node)
        elif node_status == 'U':
            unaware_nodes.append(node)

    sizes = dict(g.degree)
    aware_nodes_sizes = [node_size_scale * sizes[node] for node in aware_nodes]
    unaware_nodes_sizes = [node_size_scale * sizes[node] for node in unaware_nodes]

    nx.draw_networkx_edges(g, ax=ax, alpha=edge_alpha, pos=pos, connectionstyle='arc3,rad=0.1',
                           arrowstyle='<->', edgelist=g.out_edges)
    # Susceptible nodes
    nx.draw_networkx_nodes(g, nodelist=aware_nodes, node_size=aware_nodes_sizes,
                           node_color='violet', ax=ax, pos=pos, edgecolors=node_border_color,
                           linewidths=node_border_width, label='aware')
    # Infected nodes
    nx.draw_networkx_nodes(g, nodelist=unaware_nodes, node_size=unaware_nodes_sizes,
                           node_color='lime', ax=ax, pos=pos, edgecolors=node_border_color,
                           linewidths=node_border_width, label='unaware')

    # Opinions of the nodes
    nx.draw_networkx_labels(g, pos=pos, ax=ax, labels=nodes_opinions, font_weight='bold', font_size=13)


def plot_heatmap(array, xtickslabels: list, ytickslabels: list, colorscale_label: str, title_label: str):
    """
    Plot heatmap from 2d array with x and y ticks labels

    :param array: 2d array
    :param xtickslabels:
    :param ytickstlabels:
    :param colorscale_label:
    :param title_label:
    """
    xticks_labels = ['{:.2f}'.format(l) for l in xtickslabels]
    yticks_labels = ['{:.2f}'.format(b) for b in ytickslabels]
    sns.heatmap(array, annot=False, cmap="YlGnBu",
                yticklabels=yticks_labels, xticklabels=xticks_labels,
                vmin=0, vmax=1, cbar_kws={'label': colorscale_label})
    plt.title(title_label)
