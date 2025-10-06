import argparse
import logging
import sys
from importlib import metadata

import yaml
from rich.traceback import install

from mau import Mau
from mau.environment.environment import Environment
from mau.lexers.base_lexer.lexer import (
    MauLexerException,
    format_lexer_error,
)
from mau.nodes.node import format_node
from mau.parsers.base_parser.parser import (
    MauParserException,
    format_parser_error,
    recursive_list_nodes,
)
from mau.tokens.token import format_token

install(show_locals=True)

# from mau.nodes.page import DocumentNode
# from tabulate import tabulate

__version__ = metadata.version("mau")
logger = logging.getLogger(__name__)

# visitor_classes = load_visitors()
# visitors = {i.format_code: i for i in visitor_classes}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-file",
        action="store",
        required=True,
        help="Input file",
    )

    parser.add_argument(
        "-o",
        "--output-file",
        action="store",
        required=False,
        help="Optional output file ('-' for standard output)",
    )

    parser.add_argument(
        "-c",
        "--config-file",
        action="store",
        required=False,
        help="Optional YAML config file",
    )

    # parser.add_argument(
    #     "-f",
    #     "--format",
    #     action="store",
    #     required=True,
    #     choices=visitors.keys(),
    #     help="Output format",
    # )

    parser.add_argument(
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )

    parser.add_argument(
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    parser.add_argument(
        "--lexer-only",
        dest="lexer_only",
        help="stop after lexing",
        action="store_true",
    )

    parser.add_argument(
        "--lexer-show-tokens",
        dest="lexer_show_tokens",
        help="print the lexer tokens",
        action="store_true",
    )

    parser.add_argument(
        "--parser-only",
        dest="parser_only",
        help="performs only parsing and prints nodes",
        action="store_true",
    )

    parser.add_argument(
        "--parser-show-nodes",
        dest="parser_show_nodes",
        help="print the parser nodes",
        action="store_true",
    )

    parser.add_argument(
        "--profile",
        dest="profile",
        help="runs the profiler",
        action="store_true",
    )

    parser.add_argument(
        "--version", action="version", version=f"Mau version {__version__}"
    )

    return parser.parse_args()


def setup_logging(loglevel):
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def write_output(output, output_file, transform=None):
    if transform:
        output = transform(output)

    # The output file can be "-" which means
    # the standard output
    if output_file == "-":
        print(output)

        return

    # We need to write on an actual file
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(output)
        out.write("\n")


def main():  # pylint: disable=too-many-statements
    # Get arguments and logging set up
    args = parse_args()
    setup_logging(args.loglevel)

    # Read the input file
    with open(args.input_file, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    # Load the YAML configuration file into a dictionary
    config = {}
    if args.config_file:
        with open(args.config_file, "r", encoding="utf-8") as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)

    environment = Environment()
    environment.update(config, "mau")

    # # Select the visitor class according to the target
    # # format specified on the command line
    # # This is always successful as the list of arguments
    # # is generated from the list of plugins
    # visitor_class = visitors[args.format]
    # environment.setvar("mau.visitor.class", visitor_class)
    # environment.setvar("mau.visitor.format", args.format)

    # # Find out the name of the output file
    # output_file = args.output_file or args.input_file.replace(
    #     ".mau", visitor_class.extension
    # )

    # # Wrap the content with a DocumentNode
    # # so that the output can be rendered as
    # # a stand-alone document
    # environment.setvar("mau.parser.content_wrapper", DocumentNode())

    # The Mau object configured with what we figured out above.
    mau = Mau(
        args.input_file,
        text,
        environment=environment,
    )

    # if args.profile:
    #     import cProfile
    #     import pstats

    #     profiler = cProfile.Profile()
    #     profiler.enable()

    # Run the lexer on the input data
    logger.info("* Lexing %s", args.input_file)
    try:
        # Run the lexer
        lexer = mau.run_lexer()
    except MauLexerException as exception:
        formatted_error = format_lexer_error(exception)

        print(formatted_error)
        sys.exit(1)

    if args.lexer_show_tokens:
        for token in lexer.tokens:
            print(format_token(token))

    if args.lexer_only:
        sys.exit(1)

    # Run the parser on the lexed tokens
    logger.info("* Parsing tokens")
    try:
        # Run the parser
        parser = mau.run_parser(lexer.tokens)
    except MauParserException as exception:
        formatted_error = format_parser_error(exception)

        print(formatted_error)
        sys.exit(1)

    if args.parser_show_nodes:
        for node in parser.nodes:
            print(format_node(node))
            print()
        # print(yaml.dump(nodes, Dumper=yaml.Dumper))

    print("RECURSIVE LIST: macro var")

    l = recursive_list_nodes(
        parser.nodes,
        lambda node: node.content.type == "macro" and node.content.name == "var",
    )

    print(l)

    print("RECURSIVE LIST: orphans")

    l = recursive_list_nodes(parser.nodes, lambda node: node.parent is None)

    print(l)

    print("DOCUMENT AST:")

    print(parser.output)

    if args.parser_only:
        sys.exit(1)

    # if args.parseonly:
    #     output = "\n".join([str(node) for node in mau.parser.nodes])
    #     write_output(output, output_file)

    #     sys.exit(1)

    # logger.info(f"* Rendering {args.input_file}")
    # output = mau.run_visitor(mau.parser.output["content"])

    # except ConfigurationError as exception:
    #     print(f"Configuration error: {exception}")
    #     sys.exit(1)
    # except MauErrorException as exception:
    #     print_error(exception.error)
    #     sys.exit(1)
    # except Exception:  # pylint: disable=broad-exception-caught,try-except-raise
    #     raise

    # write_output(output, output_file, transform=visitor_class.transform)

    # if args.profile:
    #     profiler.disable()
    #     stats = pstats.Stats(profiler).sort_stats("cumtime")
    #     stats.print_stats(0.1)


if __name__ == "__main__":
    main()
