from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.nodes.include import IncludeNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.arguments_parser.parser import Arguments, ArgumentsParser
from mau.parsers.base_parser.parser import MauParserException
from mau.tokens.token import TokenType


def include_processor(parser: DocumentParser):
    # Parse content in the form
    #
    # << content_type:URI

    # Get the mandatory prefix.
    prefix = parser.tm.get_token(TokenType.INCLUDE)

    # Get the content type.
    content_type = parser.tm.get_token(TokenType.TEXT).value

    arguments: Arguments | None = parser.arguments_buffer.pop()

    if parser.tm.peek_token_is(TokenType.LITERAL, ":"):
        # In this case arguments are inline

        # Check if boxed arguments have been defined.
        # In that case we need to stop with an error.
        if arguments:
            raise MauParserException(
                "Syntax error. You cannot specify both boxed and inline arguments.",
                prefix.context,
                IncludeNodeContent.long_help,
            )

        # Get the colon.
        parser.tm.get_token(TokenType.LITERAL, ":")

        # Get the inline arguments.
        arguments_token = parser.tm.get_token(TokenType.TEXT)

        # Parse the arguments.
        with parser.tm:
            arguments_parser = ArgumentsParser.lex_and_parse(
                arguments_token.value, arguments_token.context, parser.environment
            )

        arguments = arguments_parser.arguments

    if not arguments:
        raise MauParserException(
            "Syntax error. You need to specify a list of URIs.",
            prefix.context,
            IncludeNodeContent.long_help,
        )

    # Get the URIs list and empty the unnamed arguments
    uris = arguments.unnamed_args[:]
    arguments.unnamed_args = []

    if not uris:
        raise MauParserException(
            "Syntax error. You need to specify a list of URIs.",
            prefix.context,
            IncludeNodeContent.long_help,
        )

    # Build the node info.
    info = NodeInfo(context=prefix.context, **arguments.asdict())

    # # Check the control
    # if self._pop_control() is False:
    #     return True

    # if content_type == "image":
    #     return self._parse_content_image(uris, subtype, args, kwargs, tags)

    node = Node(content=IncludeNodeContent(content_type, uris), info=info)

    if nodes := parser.title_buffer.pop():
        node.add_children({"title": nodes})

    parser._save(node)

    return True
