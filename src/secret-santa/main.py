import json
import networkx as nx
import os
import random as rd
import warnings
from argparse import ArgumentParser
from collections.abc import Sequence


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


def get_non_visited_nodes(graph: nx.DiGraph):
    """Returns a list of non-visited nodes."""
    return [node for node in graph.nodes if graph.in_degree(node) == 0]


def generate_authorized_digraph(forbidden_graph: nx.Graph, max_steps: int = 1000):
    """Generates a random authorized permutation."""
    solution = nx.create_empty_copy(forbidden_graph).to_directed()

    nodes = get_non_visited_nodes(solution)
    source = None
    step = 0

    while len(nodes) > 0 and step < max_steps:
        # pick random node among non-visited ones
        random_node = nodes[rd.randint(0, len(nodes) - 1)]

        if source is None:
            # declare source but no new edge
            source = random_node

        elif random_node != source and not forbidden_graph.has_edge(source, random_node):
            # declare new edge if not forbidden or 0-cycle
            solution.add_edge(source, random_node)

            if solution.out_degree(random_node) == 1:
                # if node already has out-going edge (i.e. was the first of a cycle)
                source = None
            else:
                # not the end of a cycle
                source = random_node

        else:
            # forbidden edge
            pass
        
        # update nodes and step
        nodes = get_non_visited_nodes(solution)
        step += 1

    if len(get_non_visited_nodes(solution)) == 0:
        # graph is fully visited
        return solution
    else:
        raise ValueError("Reached maximum number of steps without having found an authorized configuration. Consider re-running the algorithm.")


def pretty_print(solution: nx.DiGraph):
    """Prints the solution to the console."""

    print("This is the returned solution!\n")
    for node_index in solution.nodes:
        neighbors = list(solution.adj[node_index])
        if len(neighbors) != 1:
            raise ValueError("Expected single destinator!")
        print(f"{solution.nodes[node_index]['name']} -> {solution.nodes[neighbors[0]]['name']}")
    

def secret_santa():
    parser = ArgumentParser()
    parser.add_argument("--input", type=str, help="Input file.")
    parser.add_argument("--output", type=str, help="Output directory.")
    args = parser.parse_args()

    filename, extension = os.path.splitext(args.input)
    if extension == ".json":
        warnings.warn("Reading JSON file as a list of list, encoding subfamilies which will be constructed as cliques.")
        with open(args.input, "r") as f:
            family = json.load(f)["family"]
        graph = create_family_graph(family=family)
        nx.write_gml(graph, os.path.join(args.output, f"{filename}.gml"))

    elif extension == ".gml":
        graph = nx.read_gml(args.input, label="id")

    else:
        print(extension)

    # print(graph.nodes)
    # print(nx.get_node_attributes(graph, name="name"))
    # for node in graph.nodes:
    #     print(graph.nodes[node])    

    solution = generate_authorized_digraph(forbidden_graph=graph, max_steps=1000)
    pretty_print(solution=solution)

    # print(solution.nodes)
    # for node in solution.nodes:
    #     print(solution.nodes[node])


if __name__ == "__main__":
    secret_santa()