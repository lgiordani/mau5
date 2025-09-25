from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.preprocess_variables_parser.parser import PreprocessVariablesParser
from mau.tokens.token import TokenType


def variable_definition_processor(parser: DocumentParser):
    # This parses the definition of a variable
    #
    # Simple variables are defined as :name:value
    # as True booleans as just :name:
    # and as False booleas as :!name:
    #
    # Variable names can use a namespace with
    # :namespace.name:value

    # Get the opening colon.
    opening_colon = parser.tm.get_token(TokenType.VARIABLE, ":")

    # Get the mandatory variable name token.
    variable_token = parser.tm.get_token(TokenType.TEXT)

    # Get the closing colon.
    parser.tm.get_token(TokenType.LITERAL, ":")

    # Get the name of the variable.
    variable_name = variable_token.value

    # Get the context from the first value token.
    # If the value is not present, this will
    # get the context from EOL, but at the same
    # time there won't be any need to use the context
    # as the value is empty.
    context = parser.tm.peek_token().context

    # Get the optional variable value.
    value: str = ""
    if parser.tm.peek_token().type == TokenType.TEXT:
        value = parser.tm.get_token().value

    # Process the variable according to its nature.
    if variable_name.startswith("+"):
        # If the name starts with "+" it's a true flag.
        variable_name = variable_name[1:]
        value = "true"
    elif variable_name.startswith("-"):
        # If the name starts with "-" it's a false flag.
        variable_name = variable_name[1:]
        value = "false"
    elif value:
        # The variable value might contain
        # other variables, so we need to
        # replace them.
        preprocess_parser = PreprocessVariablesParser.lex_and_parse(
            value,
            context,
            parser.environment,
        )

        # The preprocess parser returns always
        # a single node.
        value = preprocess_parser.nodes[0].content.value

    if value == "":
        raise MauParserException(
            f"Error in variable definition. Variable '{variable_name}' has no value.",
            opening_colon.context,
        )

    # Now that we have name and value,
    # create or update the variable in
    # the environment.
    parser.environment.setvar(variable_name, value)

    return True
