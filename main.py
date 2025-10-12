import argparse
import logging
import sys

from rich.traceback import install

from mau import Mau, __version__
from mau.formatter.raw_formatter import RawFormatter
from mau.formatter.rich_formatter import RichFormatter

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

    # The Mau object configured with what we figured out above.
    mau = Mau(args.input_file, text)

    # Run the lexer on the input data.
    logger.info("* Lexing %s", args.input_file)

    # Run the lexer
    lexer = mau.run_lexer()

    formatter.print_tokens(lexer.tokens)


if __name__ == "__main__":
    main()
