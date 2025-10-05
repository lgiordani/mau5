from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.text_buffer.context import Context
from mau.nodes.footnotes import FootnotesListNodeContent
from mau.nodes.include import IncludeNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.toc import TocNodeContent
from mau.parsers.arguments_parser.parser import Arguments, ArgumentsParser
from mau.parsers.base_parser.parser import MauParserException
from mau.tokens.token import TokenType


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
                IncludeNodeContent.long_help,  # TODO This is not IncludeNodeContent, it should be a generic CommandNodeContent
            )

        # Get the colon.
        parser.tm.get_token(TokenType.LITERAL, ":")

        if parser.tm.peek_token().type != TokenType.TEXT:
            raise MauParserException(
                f"Syntax error. If you use the colon after {name.value} you need to specify arguments.",
                context,
                IncludeNodeContent.long_help,
            )

        # Get the inline arguments.
        arguments_token = parser.tm.get_token(TokenType.TEXT)

        # Parse the arguments.
        with parser.tm:
            arguments_parser = ArgumentsParser.lex_and_parse(
                arguments_token.value, arguments_token.context, parser.environment
            )

        arguments = arguments_parser.arguments

    arguments = arguments or Arguments()

    # Build the node info.
    info = NodeInfo(context=context, **arguments.asdict())

    if name.value == "defblock":
        # if len(command_args) < 1:
        #     parser._error("Block definitions require at least the alias")

        # alias = command_args.pop(0)

        # parser.block_aliases[alias] = {
        #     "subtype": command_subtype,
        #     "mandatory_args": command_args,
        #     "defaults": command_kwargs,
        # }
        pass
    elif name.value == "toc":
        toc_node: Node[TocNodeContent] = Node(content=TocNodeContent(), info=info)

        parser._save(toc_node)

        parser.toc_manager.add_toc_node(toc_node)

    elif name.value == "footnotes":
        footnotes_node: Node[FootnotesListNodeContent] = Node(
            content=FootnotesListNodeContent(), info=info
        )

        parser._save(footnotes_node)

        parser.footnotes_manager.add_footnotes_list_node(footnotes_node)

    elif name.value == "blockgroup":
        arguments.set_names(["group"])
        group_name = arguments.named_args.pop("group")

        group_node = parser.block_group_manager.create_group_node(group_name, context)
        parser._save(group_node)

    return True
