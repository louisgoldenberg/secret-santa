from .io import load_graph, pretty_print, save_matching_fig
from .mail import parse_mail_config, send_all_mails, write_all_mails
from .matching import (
    build_constraint_matrix,
    build_solution_digraph,
    draw_valid_matching,
)
from .parser import get_argument_parser


def secret_santa():
    """
    Script that runs the secret santa algorithm.
    """
    args = get_argument_parser().parse_args()
    constraint_graph = load_graph(args)

    # print(graph.nodes)
    # print(nx.get_node_attributes(graph, name="name"))
    # for node in graph.nodes:
    #     print(graph.nodes[node])

    constraint_matrix = build_constraint_matrix(constraint_graph=constraint_graph)
    matching = draw_valid_matching(constraint_matrix=constraint_matrix)
    solution = build_solution_digraph(
        constraint_graph=constraint_graph, matching=matching
    )

    if args.mail is not None:
        mail_config = parse_mail_config(mail_config_file=args.mail)
        msg_list = write_all_mails(digraph=solution, mail_config=mail_config)
        send_all_mails(msg_list=msg_list, mail_config=mail_config)

    else:
        pretty_print(solution=solution)
        save_matching_fig(
            constraint_matrix=constraint_matrix, matching=matching, args=args
        )


if __name__ == "__main__":
    secret_santa()
