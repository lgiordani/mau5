from importlib import metadata

__version__ = metadata.version("mau")

from mau.environment.environment import Environment
from mau.lexers.base_lexer import BaseLexer
from mau.lexers.document_lexer import DocumentLexer
from mau.text_buffer import TextBuffer


class ConfigurationError(ValueError):
    """Used to signal an error in the configuration"""


class Mau:
    def __init__(
        self,
        input_file_name: str,
        text: str,
        environment: Environment | None = None,
    ):
        # The text buffer that manages the main input file.
        self.text_buffer = TextBuffer(text, input_file_name)

        # This will contain all the variables declared
        # in the text and in the configuration
        self.environment = environment or Environment()

    def run_lexer(self) -> BaseLexer:
        lexer = DocumentLexer(self.text_buffer, self.environment)

        lexer.process()

        return lexer
