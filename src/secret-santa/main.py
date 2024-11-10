import json
import networkx as nx
import os
import warnings
from argparse import ArgumentParser

from create_family_graph import create_family_graph
from secret_santa_core import generate_authorized_digraph


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Input file.")
    parser.add_argument("-o", "--output", required=False, default=None, type=str, help="Output directory.")
    return parser

def pretty_print(solution: nx.DiGraph):
    """Prints the solution to the console."""

    print("This is the returned solution!\n")
    for node_index in solution.nodes:
        neighbors = list(solution.adj[node_index])
        if len(neighbors) != 1:
            raise ValueError("Expected single destinator!")
        print(f"{solution.nodes[node_index]['name']} -> {solution.nodes[neighbors[0]]['name']}")

def secret_santa():
    args = get_argument_parser().parse_args()

    filename, extension = os.path.splitext(args.input)
    if extension == ".json":
        warnings.warn("Reading JSON file as a list of list, encoding subfamilies which will be constructed as cliques.")
        with open(args.input, "r") as f:
            family = json.load(f)["family"]
        graph = create_family_graph(family=family)
        if args.output is not None:
            nx.write_gml(graph, os.path.join(args.output, f"{filename}.gml"))

    elif extension == ".gml":
        graph = nx.read_gml(args.input, destringizer=int)

    else:
        print(extension)

    # print(graph.nodes)
    # print(nx.get_node_attributes(graph, name="name"))
    # for node in graph.nodes:
    #     print(graph.nodes[node]) 

    attempt = 0
    max_attempts = 10
    while attempt < max_attempts:
        try:
            solution = generate_authorized_digraph(forbidden_graph=graph, max_steps=100)
            pretty_print(solution=solution)
            break
        except RuntimeError:
            attempt += 1

        


if __name__ == "__main__":
    secret_santa()