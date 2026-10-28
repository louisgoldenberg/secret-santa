import networkx as nx
import numpy as np


class FeasibilityError(ValueError):
    pass


def build_constraint_matrix(constraint_graph: nx.Graph | nx.DiGraph) -> np.ndarray:
    """Constructs a constraint matrix from the constraint graph."""
    return nx.adjacency_matrix(constraint_graph, format="dense") + np.identity(
        constraint_graph.number_of_nodes()
    )


def build_solution_digraph(
    constraint_graph: nx.Graph | nx.DiGraph,
    matching: np.ndarray,
) -> nx.DiGraph:
    """
    Builds a directed graph from the matching solution.

    Nodes are duplicated from the constraint graph, and come with all given attributes.
    Edges are directed according to the solution (source offers a gift to target).
    """
    sol_graph = nx.create_empty_copy(constraint_graph).to_directed()
    sol_graph.add_edges_from(np.transpose(matching.nonzero()))
    return sol_graph


def assert_validity(matching: np.ndarray, constraint_matrix: np.ndarray) -> None:
    if (matching * constraint_matrix).sum() > 0:
        msg = "Solution has non-zero cost. Problem is infeasible"
        raise FeasibilityError(msg)

    if not np.array_equal(matching.sum(axis=0), np.ones_like(matching[0])):
        msg = "Incorrect first marginal!"
        raise RuntimeError(msg)

    if not np.array_equal(matching.sum(axis=1), np.ones_like(matching[:, 0])):
        msg = "Incorrect second marginal!"
        raise RuntimeError(msg)


def draw_new_edge(
    current_index: int, current_matching: np.ndarray, constraint_matrix: np.ndarray
) -> np.ndarray:
    """
    Main recursion function.

    Draws a new 'edge' (understand a new one in the matching matrix) at random among valid targets and
    recurse to draw next edges or backtrack when reaching an infeasible solution.
    """

    n_rows, _ = constraint_matrix.shape

    # ENDCASE 1: current index is beyond the last row, we have reached a solution
    if current_index >= n_rows:
        return current_matching

    # MAIN RECURSION

    # mask for valid columns given the matching
    column_mask = np.ones(n_rows, dtype=bool)
    column_mask[current_matching.nonzero()[1]] = 0

    # valid targets for both matching and constraints
    target_validity = np.logical_not(constraint_matrix[current_index, :]) * column_mask
    valid_targets = target_validity.nonzero()[0]

    # shuffle the targets to randomize search order
    rng = np.random.default_rng()
    permutation = rng.permutation(len(valid_targets))
    shuffled_targets = valid_targets[permutation].tolist()

    # iterate through targets with recursion
    while len(shuffled_targets) > 0:
        try:
            current_matching_copy = current_matching.copy()
            current_matching_copy[current_index, shuffled_targets.pop()] = 1
            return draw_new_edge(
                current_index=current_index + 1,
                current_matching=current_matching_copy,
                constraint_matrix=constraint_matrix,
            )

        except FeasibilityError:
            # try again with next target
            pass

    # ENDCASE 2: we do not have any node left to recurse on
    msg = "Reached empty list of targets. Temporary infeasibility."
    raise FeasibilityError(msg)


def draw_valid_matching(constraint_matrix: np.ndarray) -> np.ndarray:
    """Draws a random valid matching for the given constraint matrix."""

    try:
        matching = draw_new_edge(
            current_index=0,
            current_matching=np.zeros_like(constraint_matrix),
            constraint_matrix=constraint_matrix,
        )
        assert_validity(matching=matching, constraint_matrix=constraint_matrix)
        return matching

    except FeasibilityError:
        msg = "Failed to find a valid solution in the recursion. Problem is infeasible."
        raise FeasibilityError(msg)
