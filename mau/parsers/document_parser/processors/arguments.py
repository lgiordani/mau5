from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.parsers.arguments_parser.parser import ArgumentsParser
from mau.parsers.preprocess_variables_parser.parser import PreprocessVariablesParser
from mau.tokens.token import TokenType


def arguments_processor(parser: DocumentParser):
    # Parse arguments in the form
    # [unnamed1, unnamed2, ..., named1=value1, named2=value2, ...]

    # Check that the token is the opening square bracket.
    parser.tm.get_token(TokenType.ARGUMENTS, "[")

    # Get the text token between brackets.
    text_token = parser.tm.get_token(TokenType.TEXT)

    # Check that the token is the closing square bracket.
    parser.tm.get_token(TokenType.LITERAL, "]")

    # Replace variables in the text.
    preprocess_parser = PreprocessVariablesParser.lex_and_parse(
        text_token.value,
        text_token.context,
        parser.environment,
    )

    # If there are no arguments there is nothing
    # to save in the stack.
    if not preprocess_parser.nodes:
        return True

    # The preprocess parser outputs a single node.
    text = preprocess_parser.nodes[0]

    # Parse the arguments.
    arguments_parser = ArgumentsParser.lex_and_parse(
        text.content.value,
        text.info.context,
        parser.environment,
    )

    # Store the arguments.
    parser.arguments_buffer.push(arguments_parser.arguments)

    return True
