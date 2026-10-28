from argparse import ArgumentParser


def get_argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input file. If JSON it has to have a 'family' list of list field encoding constraints, if GML it directly is the constraint graph.",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        default=None,
        type=str,
        help="Output directory.",
    )
    parser.add_argument(
        "-m",
        "--mail",
        required=False,
        default=None,
        type=str,
        help="The mail template.",
    )
    return parser
