import networkx as nx
from collections.abc import Sequence

"""
Functions used to create a graph of forbidden edges within a subfamily.
"""

def create_subfamily_clique(subfamily: Sequence[str]):
    """Creates a complete graph whose nodes are members of the subfamily."""

    names = {i : {"name" : name} for i, name in enumerate(subfamily)}
    clique = nx.complete_graph(n=len(subfamily))
    nx.set_node_attributes(clique, names)
    return clique


def create_family_graph(family: Sequence[Sequence[str]]):
    """Creates the full graph of forbidden connections for the family."""

    cliques = [create_subfamily_clique(subfamily=subfamily) for subfamily in family]
    graph = nx.disjoint_union_all(cliques)

    return graph