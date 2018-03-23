import os
import copy
import random
import subprocess as sub
import pandas as pd
import networkx as nx
import recordlinkage as rl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

############################################
# Helper Functions
############################################


def make_indexviz_data(matches_df: pd.DataFrame, s1: pd.Series, s2: pd.Series, c1: tuple, c2: tuple):
    """
    :param matches_df: Index.to_frame dataframe.
    :param s1: Data values.
    :param s2: Data values.
    :param c1: An RGB colour tuple (int, int, int).
    :param c2: An RGB colour tuple (int, int, int).
    :return:
    """
    assert (list(matches_df.columns) == [0, 1])

    # Node labels
    labs = {}

    # Initialize graph
    graph = nx.Graph()

    # Populate graph with nodes from df_a
    for i in range(0, len(s1)):
        # Inject information into node names
        id_str = 'df_a: ' + str(i) + ' : ' + str(s1.iloc[i])
        graph.add_node(id_str,
                       {'index': i,
                        'label': s1.iloc[i],
                        'colour': 'c1'})
        labs[id_str] = s1.iloc[i]

    # Populate graph with nodes from df_b
    for i in range(0, len(s2)):
        # Inject information into node names
        id_str = 'df_b: ' + str(i) + ' : ' + str(s2.iloc[i])
        graph.add_node(id_str,
                       {'index': i,
                        'label': s2.iloc[i],
                        'colour': 'c2'})
        labs[id_str] = s2.iloc[i]

    # Get edgelist
    edges = copy.deepcopy(matches_df)

    # Inject information into node names in edgelist
    edges[0] = edges[0].apply(lambda i: 'df_a: ' + str(i) + ' : ' + str(s1.iloc[i]))
    edges[1] = edges[1].apply(lambda i: 'df_b: ' + str(i) + ' : ' + str(s2.iloc[i]))

    # Add edges
    for i in range(len(edges)):
        graph.add_edge(edges[0].iloc[i], edges[1].iloc[i])

    # Create a colour mapping for nodes
    value_map = {'c1': c1, 'c2': c2}
    vals = []
    for n in graph.nodes():
        value = graph.node[n]['colour']
        mapping = value_map[value]
        vals.append(mapping)

    handles = [mpatches.Patch(color=c1, label='df_a'),
                      mpatches.Patch(color=c2, label='df_b')]

    return graph, labs, vals, handles


def indexviz(graph: nx.Graph, labs: dict, vals: list,  handles: list, fname: str):
    f = plt.figure(figsize=(4, 4))
    plt.axis('off')
    nx.draw_networkx(
        graph,
        pos=nx.circular_layout(graph),
        labels=labs,
        node_color=vals
    )
    plt.legend(handles=handles, loc=2, borderaxespad=-2)
    f.savefig(fname)


def visualize_index(s1: pd.Series, s2: pd.Series, indexator: rl.BaseIndexator, viz_fname: str):

    df_a = pd.DataFrame(s1, columns=['data'])
    df_b = pd.DataFrame(s2, columns=['data'])

    matches = indexator.index(df_a, df_b)

    G, labels, values, legend_handles = make_indexviz_data(
        matches.to_frame(),
        df_a['data'],
        df_b['data'],
        plt.get_cmap('tab20c').colors[2],
        plt.get_cmap('tab20c').colors[6]
    )

    indexviz(G, labels, values, legend_handles, viz_fname)


############################################
# Setup
############################################

names_1 = ['alfred', 'bob', 'calvin', 'hobbes', 'rusty']
names_2 = ['alfred', 'danny', 'callum', 'hobie', 'rusty']

############################################
# Full Index
############################################

visualize_index(
    pd.Series(names_1, name='data'),
    pd.Series(names_2, name='data'),
    rl.FullIndex(),
    'full_index_network.svg'
)

############################################
# Random Index
############################################

visualize_index(
    pd.Series(names_1, name='data'),
    pd.Series(names_2, name='data'),
    rl.RandomIndex(10),
    'random_index_network.svg'
)

############################################
# Block Index
############################################

visualize_index(
    pd.Series(names_1, name='data'),
    pd.Series(names_2, name='data'),
    rl.BlockIndex(on='data'),
    'block_index_network.svg'
)

############################################
# Sorted Neighborhood Index
############################################

visualize_index(
    pd.Series(names_1, name='data'),
    pd.Series(names_2, name='data'),
    rl.SortedNeighbourhoodIndex(on='data'),
    'sorted_neighborhood_network.svg'
)

############################################
# Small Neighborhood
############################################

visualize_index(
    pd.Series(['alfred']*5, name='data'),
    pd.Series(['beth']*5, name='data'),
    rl.SortedNeighbourhoodIndex(on='data'),
    'small_neighborhood_network.svg'
)

############################################
# Segregated Neighborhood
############################################

visualize_index(
    pd.Series(['alfred', 'agnes', 'amy', 'alexander', 'alice'], name='data'),
    pd.Series(['bruce', 'beth', 'bob', 'brittany', 'bill'], name='data'),
    rl.SortedNeighbourhoodIndex(on='data'),
    'segregated_neighborhood_network.svg'
)

############################################
# Randomly Selected Neighborhood
############################################

visualize_index(
    pd.Series(['alexander', 'bob', 'bruce', 'bruce', 'alexander'], name='data'),
    pd.Series(['alice', 'beth', 'amy', 'beth', 'brittany'], name='data'),
    rl.SortedNeighbourhoodIndex(on='data', window=5),
    'window_neighborhood_network.svg'
)

############################################
# Open
############################################

files = os.listdir('.')
for fname in files:
    if '_network.svg' in fname:
        sub.call(['open', fname])
