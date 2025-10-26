from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.nodes.node import Node, NodeInfo
from mau.nodes.command import (
    COMMAND_HELP,
    TocNodeContent,
    FootnotesNodeContent,
    BlockGroupNodeContent,
)
from mau.parsers.arguments_parser import Arguments, ArgumentsParser
from mau.parsers.base_parser import MauParserException
from mau.text_buffer import Context
from mau.token import TokenType

# TODO Currently, commands do not support
# * labels
# * control


def command_processor(parser: DocumentParser):
    # Parse a command in the form ::command:arguments

    # Get the opening double colon.
    prefix = parser.tm.get_token(TokenType.COMMAND, "::")

    # Get the name of the command.
    name = parser.tm.get_token(TokenType.TEXT)

    arguments: Arguments | None = parser.arguments_buffer.pop()

    # Find the final context.
    context = Context.merge_contexts(prefix.context, name.context)

    if parser.tm.peek_token_is(TokenType.LITERAL, ":"):
        # In this case arguments are inline

        # Check if boxed arguments have been defined.
        # In that case we need to stop with an error.
        if arguments:
            raise MauParserException(
                "Syntax error. You cannot specify both boxed and inline arguments.",
                context,
                COMMAND_HELP,
            )

        # Get the colon.
        parser.tm.get_token(TokenType.LITERAL, ":")

        if parser.tm.peek_token().type != TokenType.TEXT:
            raise MauParserException(
                f"Syntax error. If you use the colon after {name.value} you need to specify arguments.",
                context,
                COMMAND_HELP,
            )

        # Get the inline arguments.
        arguments_token = parser.tm.get_token(TokenType.TEXT)

        # Parse the arguments.
        with parser.tm:
            arguments_parser = ArgumentsParser.lex_and_parse(
                arguments_token.value,
                parser.environment,
                *arguments_token.context.start_position,
                arguments_token.context.source,
            )

        arguments = arguments_parser.arguments

    arguments = arguments or Arguments()

    # Build the node info.
    info = NodeInfo(context=context, **arguments.asdict())

    if name.value == "toc":
        toc_node: Node[TocNodeContent] = Node(content=TocNodeContent(), info=info)

        parser._save(toc_node)

        parser.toc_manager.add_toc_node(toc_node)

    elif name.value == "footnotes":
        footnotes_node: Node[FootnotesNodeContent] = Node(
            content=FootnotesNodeContent(), info=info
        )

        parser._save(footnotes_node)

        parser.footnotes_manager.add_footnotes_node(footnotes_node)

    elif name.value == "blockgroup":
        arguments.set_names(["group"])
        group_name = arguments.named_args.pop("group")

        group_node = Node(
            content=BlockGroupNodeContent(group_name),
            info=NodeInfo(context=context),
        )

        parser.block_group_manager.add_group_node(group_node)
        parser._save(group_node)

    return True
