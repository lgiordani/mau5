from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mau.parsers.document_parser import DocumentParser


from mau.nodes.include import IncludeImageNode, IncludeMauNode, IncludeNode
from mau.nodes.node import NodeInfo
from mau.nodes.node_arguments import NodeArguments
from mau.parsers.arguments_parser import (
    process_arguments_with_variables,
)
from mau.parsers.base_parser import create_parser_exception
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

    arguments: NodeArguments | None = parser.arguments_buffer.pop()

    if parser.tm.peek_token_is(TokenType.LITERAL, ":"):
        # In this case arguments are inline

        # Check if boxed arguments have been defined.
        # In that case we need to stop with an error.
        if arguments:
            raise create_parser_exception(
                "Syntax error. You cannot specify both boxed and inline arguments.",
                context,
            )

        # Get the colon.
        parser.tm.get_token(TokenType.LITERAL, ":")

        # Get the inline arguments.
        arguments_token = parser.tm.get_token(TokenType.TEXT)

        arguments = process_arguments_with_variables(
            arguments_token, parser.message_handler, parser.environment
        ).arguments

    if not arguments:
        raise create_parser_exception(
            "Syntax error. You need to specify a list of URIs.",
            context,
        )

    # Check the stored control
    if control := parser.control_buffer.pop():
        # If control is False, we need to stop
        # processing here and return without
        # saving any node.
        if not control.process(parser.environment):
            return True

    node: IncludeImageNode | IncludeNode

    match content_type.value:
        case "image":
            node = _parse_image(parser, arguments, context)
        case "mau":
            node = _parse_mau(parser, arguments, context)
        case _:
            node = _parse_generic(parser, content_type.value, arguments, context)

    # Build the node info.
    node.info = NodeInfo(context=context)
    node.arguments = NodeArguments(**arguments.asdict())

    # Extract labels from the buffer and
    # store them in the node data.
    parser.pop_labels(node)

    parser._save(node)

    return True


def _parse_generic(
    parser: DocumentParser,
    content_type: str,
    arguments: NodeArguments,
    context: Context,
) -> IncludeNode:
    # Get the URIs list and empty the unnamed arguments
    uris = arguments.unnamed_args[:]
    arguments.unnamed_args = []

    if not uris:
        raise create_parser_exception(
            "Syntax error. You need to specify a list of URIs.",
            context,
        )

    return IncludeNode(content_type, uris)


def _parse_image(
    parser: DocumentParser, arguments: NodeArguments, context: Context
) -> IncludeImageNode:
    arguments.set_names(["uri", "alt_text", "classes"])

    uri = arguments.named_args.pop("uri")

    alt_text = arguments.named_args.pop("alt_text", None)
    classes_arg = arguments.named_args.pop("classes", None)

    classes = []
    if classes_arg:
        classes.extend(classes_arg.split(","))

    content = IncludeImageNode(
        uri,
        alt_text,
        classes,
    )

    return content


def _parse_mau(
    parser: DocumentParser, arguments: NodeArguments, context: Context
) -> IncludeImageNode:
    arguments.set_names(["uri"])

    uri = arguments.named_args.pop("uri")

    with open(uri, "r", encoding="utf-8") as f:
        text = f.read()

    # The parsing environment is
    # that of the external parser.
    environment = parser.environment

    # Unpack the token initial position.
    start_line, start_column = context.start_position

    # Get the token source.
    source_filename = uri

    content_parser = parser.lex_and_parse(
        text=text,
        message_handler=parser.message_handler,
        environment=environment,
        start_line=start_line,
        start_column=start_column,
        source_filename=source_filename,
    )
    content_parser.finalise()

    # TODO
    # if update:
    #     # The footnote mentions and definitions
    #     # found in this block are part of the
    #     # main document. Import them.
    #     parser.footnotes_manager.update(content_parser.footnotes_manager)

    #     # The internal links and headers
    #     # found in this block are part of the
    #     # main document. Import them.
    #     parser.toc_manager.update(content_parser.toc_manager)

    return IncludeMauNode(
        uri,
        content=content_parser.nodes,
    )
