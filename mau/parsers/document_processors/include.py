from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mau.parsers.document_parser import DocumentParser


from mau.nodes.include import IncludeImageNodeData, IncludeNodeData
from mau.nodes.node import Node, NodeInfo
from mau.parsers.arguments_parser import Arguments, ArgumentsParser
from mau.parsers.base_parser import MauParserException
from mau.text_buffer import Context
from mau.token import TokenType


def include_processor(parser: DocumentParser):
    # Parse content in the form
    #
    # << content_type:URI

    # Get the mandatory prefix.
    prefix = parser.tm.get_token(TokenType.INCLUDE)

    # Get the content type.
    content_type = parser.tm.get_token(TokenType.TEXT)

    # Find the final context.
    context = Context.merge_contexts(prefix.context, content_type.context)

    arguments: Arguments | None = parser.arguments_buffer.pop()

    if parser.tm.peek_token_is(TokenType.LITERAL, ":"):
        # In this case arguments are inline

        # Check if boxed arguments have been defined.
        # In that case we need to stop with an error.
        if arguments:
            raise MauParserException(
                "Syntax error. You cannot specify both boxed and inline arguments.",
                context,
                IncludeNodeData.long_help,
            )

        # Get the colon.
        parser.tm.get_token(TokenType.LITERAL, ":")

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

    if not arguments:
        raise MauParserException(
            "Syntax error. You need to specify a list of URIs.",
            context,
            IncludeNodeData.long_help,
        )

    # Check the stored control
    if control := parser.control_buffer.pop():
        # If control is False, we need to stop
        # processing here and return without
        # saving any node.
        if not control.process(parser.environment):
            return True

    content: IncludeImageNodeData | IncludeNodeData

    if content_type.value == "image":
        content = _parse_image(arguments, context)
    else:
        content = _parse_generic(content_type.value, arguments, context)

    # Build the node info.
    info = NodeInfo(context=context, **arguments.asdict())

    node = Node(data=content, info=info)

    # Extract labels from the buffer and
    # store them in the node data.
    if labels := parser.label_buffer.pop():
        content.labels = labels

    parser._save(node)

    return True


def _parse_generic(
    content_type: str, arguments: Arguments, context: Context
) -> IncludeNodeData:
    # Get the URIs list and empty the unnamed arguments
    uris = arguments.unnamed_args[:]
    arguments.unnamed_args = []

    if not uris:
        raise MauParserException(
            "Syntax error. You need to specify a list of URIs.",
            context,
            IncludeNodeData.long_help,
        )

    return IncludeNodeData(content_type, uris)


def _parse_image(arguments: Arguments, context: Context) -> IncludeImageNodeData:
    arguments.set_names(["uri", "alt_text", "classes"])

    uri = arguments.named_args.pop("uri")

    alt_text = arguments.named_args.pop("alt_text", None)
    classes_arg = arguments.named_args.pop("classes", None)

    classes = []
    if classes_arg:
        classes.extend(classes_arg.split(","))

    content = IncludeImageNodeData(
        uri,
        alt_text,
        classes,
    )

    return content
