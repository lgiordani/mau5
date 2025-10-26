from importlib import metadata
from pathlib import Path

import yaml

__version__ = metadata.version("mau")

from mau.environment.environment import Environment
from mau.lexers.base_lexer import BaseLexer
from mau.lexers.document_lexer import DocumentLexer
from mau.text_buffer import TextBuffer

BASE_NAMESPACE = "mau"

DEFAULT_ENVIRONMENT_FILES_NAMESPACE = "envfiles"
DEFAULT_ENVIRONMENT_VARIABLES_NAMESPACE = "envvars"

# TODO Add help to each node and use it in exceptions


class ConfigurationError(ValueError):
    """Used to signal an error in the configuration"""


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
        environment.update(flat_environment_files, namespace)


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
        environment.update(flat_environment_variables, namespace)


class Mau:  # pragma: no cover
    def __init__(
        self,
        input_file_name: str,
        text: str,
        environment: Environment | None = None,
    ):
        # The text buffer that manages the main input file.
        self.text_buffer = TextBuffer(text, source_filename=input_file_name)

        # This will contain all the variables declared
        # in the text and in the configuration
        self.environment = environment or Environment()

    def run_lexer(self) -> BaseLexer:
        lexer = DocumentLexer(self.text_buffer, self.environment)

        lexer.process()

        return lexer
