from importlib import metadata
from pathlib import Path

import yaml

__version__ = metadata.version("mau")

from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.parsers.document_parser import DocumentParser
from mau.text_buffer import TextBuffer
from mau.token import Token
from mau.visitors.base_visitor import BaseVisitor
from mau.visitors.html_visitor import HtmlVisitor
from mau.visitors.jinja_visitor import JinjaVisitor

BASE_NAMESPACE = "mau"

DEFAULT_ENVIRONMENT_FILES_NAMESPACE = "envfiles"
DEFAULT_ENVIRONMENT_VARIABLES_NAMESPACE = "envvars"


class ConfigurationError(ValueError):
    """Used to signal an error in the configuration"""


def load_visitors():
    """
    This function loads all the visitors belonging to
    the group "mau.visitors". This code has been isolated
    in a function to allow visitor modules to import the
    Mau package without creating a cycle.
    """

    import sys

    if sys.version_info < (3, 10):
        from importlib_metadata import entry_points
    else:
        from importlib.metadata import entry_points

    discovered_plugins = entry_points(group="mau.visitors")

    # Load the available visitors
    visitors = [i.load() for i in discovered_plugins]
    visitors.append(BaseVisitor)
    visitors.append(JinjaVisitor)
    visitors.append(HtmlVisitor)

    return visitors


def load_environment_files(
    environment: Environment,
    files: list[str],
    namespace: str | None = None,
):
    """Load each environment file into the environment."""

    # Set the namespace.
    namespace = namespace or DEFAULT_ENVIRONMENT_FILES_NAMESPACE

    # Add the base namespace as a prefix.
    namespace = f"{BASE_NAMESPACE}.{namespace}"

    # A flat dictionary that will contain all the environment files.
    flat_environment_files: dict[str, str] = {}

    for filename in files:
        # Files can be specified as path or as key=path.
        # If it's just path, the file content is stored under
        #
        # DEFAULT_ENVIRONMENT_FILES_NAMESPACE.filename
        #
        # If the key is specified the file content is stored under
        #
        # DEFAULT_ENVIRONMENT_FILES_NAMESPACE.key.filename

        try:
            # Assume the filename is in the form "key=path".
            key, value = filename.split("=")

            # Create a Path from the file path.
            filepath = Path(value)
        except ValueError:
            # Create a Path from the file path.
            filepath = Path(filename)

            # The key is the name of the
            # file without extension.
            key = filepath.stem

        try:
            # Assume this is YAML.
            with filepath.open("r", encoding="utf-8") as f:
                content = yaml.safe_load(f)
                flat_environment_files[key] = content
        except Exception as exc:
            raise ConfigurationError(f"Error processing {filename}") from exc

    if flat_environment_files:
        environment.dupdate(flat_environment_files, namespace)


def load_environment_variables(
    environment: Environment,
    variables: list[str],
    namespace: str | None = None,
):
    """Load each environment variable into the environment."""

    # Set the namespace.
    namespace = namespace or DEFAULT_ENVIRONMENT_VARIABLES_NAMESPACE

    # Add the base namespace as a prefix.
    namespace = f"{BASE_NAMESPACE}.{namespace}"

    # Build a flat dictionary with all the environment variables.
    flat_environment_variables: dict[str, str] = {}

    for variable in variables:
        # Variables must be specified as key=value.
        # They are stored under
        #
        # DEFAULT_ENVIRONMENT_VARIABLES_NAMESPACE.key.value

        # Parse the environment variable syntax.
        key, value = variable.split("=")

        # Store the value.
        flat_environment_variables[key] = value

    if flat_environment_variables:
        environment.dupdate(flat_environment_variables, namespace)


class Mau:  # pragma: no cover
    def __init__(
        self,
        environment: Environment | None = None,
    ):
        # This will contain all the variables declared
        # in the text and in the configuration.
        self.environment = environment or Environment()

        # This will contain the lexer tokens.
        self.tokens: list[Token] = []

    def init_text_buffer(self, text: str, source_filename: str) -> TextBuffer:
        # The text buffer that manages the input file.
        return TextBuffer(text, source_filename=source_filename)

    def run_lexer(self, text_buffer: TextBuffer) -> DocumentLexer:
        lexer = DocumentLexer(text_buffer, self.environment)
        lexer.process()

        return lexer

    def run_parser(self, tokens: list[Token]) -> DocumentParser:
        parser = DocumentParser(tokens, self.environment)
        parser.parse()
        parser.finalise()

        return parser

    def init_visitor(self, visitor_class) -> BaseVisitor:
        return visitor_class(
            environment=self.environment,
        )

    def run_visitor(self, visitor, node) -> dict:
        # Visit the given node and all its children.
        return visitor.visit(node)

    def process(self, text: str, source_filename: str):
        # The text buffer that manages the input file.
        text_buffer = self.init_text_buffer(text, source_filename)

        # Run the lexer on the text buffer.
        lexer = self.run_lexer(text_buffer)

        # Parse the lexer tokens.
        self.run_parser(lexer.tokens)

        # TODO add run_visitor
