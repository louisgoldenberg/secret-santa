import networkx as nx
import random as rd


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
        raise RuntimeError("Reached maximum number of steps without having found an authorized configuration. Consider re-running the algorithm.")
    