from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mau.parsers.document_parser import DocumentParser


from mau.nodes.command import (
    BlockGroupNode,
    CommandNode,
    FootnotesNode,
    TocNode,
)
from mau.nodes.node import NodeInfo
from mau.nodes.node_arguments import NodeArguments
from mau.parsers.arguments_parser import ArgumentsParser
from mau.parsers.base_parser import create_parser_exception
from mau.text_buffer import Context
from mau.token import TokenType

# TODO The implementation at lines 81-145 is horrendous.


def command_processor(parser: DocumentParser):
    # Parse a command in the form ::command:arguments

    # Get the opening double colon.
    prefix = parser.tm.get_token(TokenType.COMMAND, "::")

    # Get the name of the command.
    name = parser.tm.get_token(TokenType.TEXT)

    # Get the stored arguments.
    # Commands can receive arguments
    # through the arguments manager or inline..
    arguments: NodeArguments | None = parser.arguments_buffer.pop()

    # Find the final context.
    context = Context.merge_contexts(prefix.context, name.context)

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

        if parser.tm.peek_token().type != TokenType.TEXT:
            raise create_parser_exception(
                f"Syntax error. If you use the colon after {name.value} you need to specify arguments.",
                context,
            )

        # Get the inline arguments.
        arguments_token = parser.tm.get_token(TokenType.TEXT)

        # Unpack the token initial position.
        start_line, start_column = arguments_token.context.start_position

        # Parse the arguments.
        with parser.tm:
            arguments_parser = ArgumentsParser.lex_and_parse(
                text=arguments_token.value,
                message_handler=parser.message_handler,
                environment=parser.environment,
                start_line=start_line,
                start_column=start_column,
                source_filename=arguments_token.context.source,
            )

        arguments = arguments_parser.arguments

    # Build the node info.
    info = NodeInfo(context=context)

    if name.value == "toc":
        toc_node = TocNode(info=info, arguments=arguments)

        # Extract labels from the buffer and
        # store them in the node data.
        parser.pop_labels(toc_node)

        # Check the stored control
        if control := parser.control_buffer.pop():
            # If control is False, we need to stop
            # processing here and return without
            # saving any node.
            if not control.process(parser.environment):
                return True

        parser._save(toc_node)

        parser.toc_manager.add_toc_node(toc_node)

    elif name.value == "footnotes":
        footnotes_node = FootnotesNode(info=info, arguments=arguments)

        # Extract labels from the buffer and
        # store them in the node data.
        parser.pop_labels(footnotes_node)

        # Check the stored control
        if control := parser.control_buffer.pop():
            # If control is False, we need to stop
            # processing here and return without
            # saving any node.
            if not control.process(parser.environment):
                return True

        parser._save(footnotes_node)

        parser.footnotes_manager.add_footnotes_list(footnotes_node)

    elif name.value == "blockgroup":
        arguments.set_names(["group"])

        group_name = arguments.named_args.pop("group")

        block_group_node = BlockGroupNode(group_name, info=info, arguments=arguments)

        # Extract labels from the buffer and
        # store them in the node data.
        parser.pop_labels(block_group_node)

        # Check the stored control
        if control := parser.control_buffer.pop():
            # If control is False, we need to stop
            # processing here and return without
            # saving any node.
            if not control.process(parser.environment):
                return True

        parser._save(block_group_node)

        parser.block_group_manager.add_group(block_group_node)

    else:
        command_node = CommandNode(name=name.value, info=info, arguments=arguments)

        # Extract labels from the buffer and
        # store them in the node data.
        parser.pop_labels(command_node)

        # Check the stored control
        if control := parser.control_buffer.pop():
            # If control is False, we need to stop
            # processing here and return without
            # saving any node.
            if not control.process(parser.environment):
                return True

        parser._save(command_node)

    return True
