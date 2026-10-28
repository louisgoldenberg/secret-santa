from collections.abc import Sequence

import networkx as nx


def build_clique(subfamily: Sequence[str]) -> nx.Graph:
    """Builds a complete graph whose nodes are members of the subfamily."""

    names = {i: {"name": name} for i, name in enumerate(subfamily)}
    clique = nx.complete_graph(n=len(subfamily))
    nx.set_node_attributes(clique, names)
    return clique


def build_family_graph(family: Sequence[Sequence[str]]) -> nx.Graph:
    """Builds the full constraint graph for the family."""

    cliques = [build_clique(subfamily=subfamily) for subfamily in family]
    graph = nx.disjoint_union_all(cliques)

    return graph
