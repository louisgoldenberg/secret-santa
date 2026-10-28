import json
import os
import warnings

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from .input_graph_construction import build_family_graph


def load_graph(args) -> nx.Graph | nx.DiGraph:
    filename, extension = os.path.splitext(args.input)
    if extension == ".json":
        warnings.warn(
            "Reading JSON file as a list of list, encoding subfamilies which will be constructed as cliques."
        )
        with open(args.input, "r") as f:
            family = json.load(f)["family"]
        graph = build_family_graph(family=family)
        nx.write_gml(graph, f"{filename}.gml")

    elif extension == ".gml":
        graph = nx.read_gml(args.input, destringizer=int)

    else:
        msg = f"Unknown extension {extension=}"
        raise ValueError(msg)

    return graph


def pretty_print(solution: nx.DiGraph):
    """Prints the solution to the console."""

    print("This is the returned solution!\n")
    for node_index in solution.nodes:
        neighbors = list(solution.adj[node_index])
        if len(neighbors) != 1:
            raise ValueError("Expected single destinator!")
        print(
            f"{solution.nodes[node_index]['name']} -> {solution.nodes[neighbors[0]]['name']}"
        )


def save_matching_fig(constraint_matrix: np.ndarray, matching: np.ndarray, args):
    filename, _ = os.path.splitext(args.input)

    _, ax = plt.subplots(1, 3)
    ax[0].imshow(constraint_matrix)
    ax[1].imshow(matching)
    ax[2].imshow(matching * constraint_matrix)
    plt.savefig(f"{filename}.png")
