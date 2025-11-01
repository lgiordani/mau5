import argparse
import logging
import sys

from rich.traceback import install

from mau import Mau, __version__, load_environment_files, load_environment_variables
from mau.environment.environment import Environment
from mau.formatter.raw_formatter import RawFormatter
from mau.formatter.rich_formatter import RichFormatter
from mau.parsers.base_parser import MauParserException
from mau.lexers.base_lexer import MauLexerException

default_formatter = RichFormatter.type
available_formatters = {
    formatter.type: formatter for formatter in [RawFormatter, RichFormatter]
}

install(show_locals=True)

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-i",
        "--input-file",
        action="store",
        required=True,
        help="Input file",
    )

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
        "-e",
        "--environment-file",
        action="append",
        required=False,
        help=(
            "Optional text/YAML file in the form key=path (can be specified "
            "multiple times). The key can be dotted to add namespaces."
        ),
    )

    parser.add_argument(
        "--environment-files-namespace",
        action="store",
        default="envfiles",
        required=False,
        help="Optional namespace for environment files (default: envfiles)",
    )

    parser.add_argument(
        "-v",
        "--environment-variable",
        action="append",
        required=False,
        help=(
            "Optional environment variable in the form key=value (can be specified "
            "multiple times). The key can be dotted to add namespaces."
        ),
    )

    parser.add_argument(
        "--environment-variables-namespace",
        action="store",
        default="envvars",
        required=False,
        help="Optional namespace for environment variables (default: envvars)",
    )

    parser.add_argument(
        "--formatter",
        action="store",
        choices=available_formatters.keys(),
        default=default_formatter,
        help="Formatter object to use",
    )

    parser.add_argument(
        "--lexer-only",
        dest="lexer_only",
        help="stop after lexing",
        action="store_true",
    )

    parser.add_argument(
        "--parser-only",
        dest="parser_only",
        help="stop after parsing",
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


def main():
    # Get arguments and logging set up.
    args = parse_args()
    setup_logging(args.loglevel)

    # Initialise the formatter.
    formatter = available_formatters[args.formatter]

    # Read the input file
    with open(args.input_file, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    # Start with a clean environment.
    environment = Environment()

    # The list of environment files passed on the command line.
    environment_files = args.environment_file or []

    # Load the files inside the environment.
    load_environment_files(
        environment,
        environment_files,
        namespace=args.environment_files_namespace,
    )

    # The list of environment variables passed on the command line.
    environment_variables = args.environment_variable or []

    # Load the variables inside the environment.
    load_environment_variables(
        environment,
        environment_variables,
        namespace=args.environment_variables_namespace,
    )

    # The Mau object configured with what we figured out above.
    mau = Mau(args.input_file, text)

    # Run the lexer on the input data.
    logger.info("* Lexing %s", args.input_file)

    # Run the lexer.
    try:
        tokens = mau.run_lexer()
    except MauLexerException as exc:
        formatter.print_lexer_exception(exc)
        sys.exit(1)

    # The user wants us to run the lexer
    # only, so we print the resulting tokens
    # and quit.
    if args.lexer_only:
        # Print the tokens collected by the lexer.
        formatter.print_tokens(tokens)
        sys.exit(0)

    # Run the parser.
    try:
        nodes = mau.run_parser()
    except MauParserException as exc:
        formatter.print_parser_exception(exc)
        sys.exit(1)

    # The user wants us to run the parser
    # only, so we print the resulting nodes
    # and quit.
    if args.parser_only:
        # Print the nodes collected by the parser.
        formatter.print_nodes(nodes)
        sys.exit(0)


if __name__ == "__main__":
    main()
