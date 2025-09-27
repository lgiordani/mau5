from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


# from mau.lexers.base_lexer.lexer import TokenTypes as TokenType
from mau.nodes.footnotes import FootnotesListNodeContent
from mau.nodes.include import IncludeNodeContent

# from mau.lexers.document_lexer.lexer import TokenTypes as TokenType
# from mau.nodes.block import BlockGroupNode, BlockNode
# from mau.nodes.content import ContentImageNode, ContentNode
from mau.nodes.node import Node, NodeInfo
from mau.nodes.toc import TocNodeContent
from mau.parsers.arguments_parser.parser import Arguments, ArgumentsParser

# from mau.nodes.page import ContainerNode
# from mau.nodes.paragraph import ParagraphNode
# from mau.nodes.source import MarkerNode, CalloutsEntryNode, SourceNode, SourceLineNode
from mau.parsers.base_parser.parser import MauParserException
from mau.tokens.token import TokenType


def command_processor(parser: DocumentParser):
    # Parse a command in the form ::command:arguments

    # Get the opening double colon.
    prefix = parser.tm.get_token(TokenType.COMMAND, "::")

    # Get the name of the command.
    name = parser.tm.get_token(TokenType.TEXT).value

    arguments: Arguments | None = parser.arguments_buffer.pop()

    if parser.tm.peek_token_is(TokenType.LITERAL, ":"):
        # In this case arguments are inline

        # Check if boxed arguments have been defined.
        # In that case we need to stop with an error.
        if arguments:
            raise MauParserException(
                "Syntax error. You cannot specify both boxed and inline arguments.",
                prefix.context,
                IncludeNodeContent.long_help,  # TODO This is not IncludeNodeContent, it should be a generic CommandNodeContent
            )

        # Get the colon.
        parser.tm.get_token(TokenType.LITERAL, ":")

        if parser.tm.peek_token().type != TokenType.TEXT:
            raise MauParserException(
                f"Syntax error. If you use the colon after {name} you need to specify arguments.",
                prefix.context,
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
    info = NodeInfo(context=prefix.context, **arguments.asdict())

    if name == "defblock":
        # if len(command_args) < 1:
        #     parser._error("Block definitions require at least the alias")

        # alias = command_args.pop(0)

        # parser.block_aliases[alias] = {
        #     "subtype": command_subtype,
        #     "mandatory_args": command_args,
        #     "defaults": command_kwargs,
        # }
        pass
    elif name == "toc":
        toc_node: Node[TocNodeContent] = Node(content=TocNodeContent(), info=info)

        parser._save(toc_node)

        parser.toc_manager.add_toc_node(toc_node)

    elif name == "footnotes":
        footnotes_node: Node[FootnotesListNodeContent] = Node(
            content=FootnotesListNodeContent(), info=info
        )

        parser._save(footnotes_node)

        parser.footnotes_manager.add_footnotes_list_node(footnotes_node)

    elif name == "blockgroup":
        arguments.set_names(["group"])
        group_name = arguments.named_args.pop("group")

        group_node = parser.block_group_manager.create_group_node(
            group_name, prefix.context
        )
        parser._save(group_node)

    return True
