# pylint: disable=too-many-lines

from __future__ import annotations

from functools import partial

from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.document import ContainerNodeContent, DocumentNodeContent
from mau.nodes.node import Node, NodeContent, NodeInfo
from mau.parsers.base_parser import BaseParser
from mau.parsers.buffers.arguments_buffer import ArgumentsBuffer
from mau.parsers.buffers.control_buffer import ControlBuffer
from mau.parsers.buffers.label_buffer import LabelBuffer
from mau.parsers.document_processors.arguments import arguments_processor
from mau.parsers.document_processors.command import command_processor
from mau.parsers.document_processors.control import control_processor
from mau.parsers.document_processors.header import header_processor
from mau.parsers.document_processors.horizontal_rule import horizontal_rule_processor
from mau.parsers.document_processors.include import include_processor
from mau.parsers.document_processors.label import label_processor
from mau.parsers.document_processors.list import list_processor
from mau.parsers.document_processors.paragraph import paragraph_processor
from mau.parsers.document_processors.variable_definition import (
    variable_definition_processor,
)
from mau.parsers.managers.block_group_manager import BlockGroupManager
from mau.parsers.managers.footnotes_manager import FootnotesManager
from mau.parsers.managers.header_links_manager import HeaderLinksManager
from mau.parsers.managers.toc_manager import TocManager
from mau.parsers.preprocess_variables_parser import PreprocessVariablesParser
from mau.parsers.text_parser import TextParser
from mau.text_buffer import Context
from mau.token import Token, TokenType
from mau.parsers.document_processors.block import block_processor


# The DocumentParser is in charge of parsing
# the whole input, calling other parsers
# to manage single paragraphs or other
# things like variables.
class DocumentParser(BaseParser):
    lexer_class = DocumentLexer

    def __init__(
        self,
        tokens: list[Token],
        environment: Environment | None = None,
        parent_node=None,
    ):
        super().__init__(tokens, environment, parent_node)

        # This is the function used to create internal IDs for headers.
        self.header_internal_id_function = self.environment.get(
            "mau.parser.header_internal_id_function", None
        )

        # This is the function used to create unique IDs for footnotes.
        self.footnote_unique_id_function = self.environment.get(
            "mau.parser.footnote_unique_id_function", None
        )

        self.header_links_manager: HeaderLinksManager = HeaderLinksManager()
        self.block_group_manager = BlockGroupManager()
        self.footnotes_manager = FootnotesManager(self.footnote_unique_id_function)
        self.toc_manager: TocManager = TocManager(self.header_internal_id_function)

        self.arguments_buffer: ArgumentsBuffer = ArgumentsBuffer()
        self.label_buffer: LabelBuffer = LabelBuffer()
        self.control_buffer: ControlBuffer = ControlBuffer()

        # The last index in the latest ordered list,
        # used to calculate the beginning value of them
        # next one when start=auto
        self.latest_ordered_list_index = 0

        # This is the final output of the parser
        self.output = {}

    def _process_functions(self):
        # All the functions that this parser provides.

        return [
            self._process_eol,
            partial(horizontal_rule_processor, self),
            partial(variable_definition_processor, self),
            partial(command_processor, self),
            partial(label_processor, self),
            partial(control_processor, self),
            partial(arguments_processor, self),
            partial(header_processor, self),
            partial(block_processor, self),
            partial(include_processor, self),
            partial(list_processor, self),
            partial(paragraph_processor, self),
        ]

    def _parse_text(self, text: str, context: Context) -> list[Node[NodeContent]]:
        # This parses a piece of text.
        # It runs the text through the preprocessor to
        # replace variables, then parses it storing
        # footnotes and internal links, and finally
        # returns the nodes.

        # Replace variables
        preprocess_parser = PreprocessVariablesParser.lex_and_parse(
            text,
            self.environment,
            *context.start_position,
            context.source,
        )

        # If the preprocessor doesn't return any
        # node we can stop here.
        if not preprocess_parser.nodes:  # pragma: no cover
            return []

        # The preprocess parser outputs a single node.
        text = preprocess_parser.nodes[0].content.value

        # Parse the text
        text_parser = TextParser.lex_and_parse(
            text,
            self.environment,
            *context.start_position,
            context.source,
        )

        # Extract the footnote mentions
        # found in this piece of text.
        self.footnotes_manager.add_mentions(text_parser.footnotes)

        # Extract the header links found in this piece of text.
        self.header_links_manager.add_links(text_parser.header_links)

        return text_parser.nodes

    def _process_eol(self) -> bool:
        # This simply ignores the end of line.

        self.tm.get_token(TokenType.EOL)

        return True

    def finalise(self):
        super().finalise()

        # This processes all footnotes stored in
        # the manager merging mentions and data
        # and updating the nodes that contain
        # a list of footnotes.
        self.footnotes_manager.process()

        # This processes all links stored in
        # the manager linking them to the
        # correct headers.
        self.header_links_manager.process()

        # Process ToC nodes.
        self.toc_manager.process()

        # Process block groups.
        self.block_group_manager.process()

        if not self.nodes:
            return self.output

        document_content_class = self.environment.get(
            "mau.parser.document_wrapper", DocumentNodeContent
        )

        # Find the document context.
        context = Context.merge_contexts(
            self.nodes[0].info.context, self.nodes[-1].info.context
        )

        nodes_wrapper = self.environment.get(
            "mau.parser.nodes_wrapper", ContainerNodeContent
        )

        self.output.update(
            {
                "document": Node(
                    content=document_content_class(),
                    info=NodeInfo(context=context),
                    children={"content": self.nodes},
                ),
                "nested_toc": Node(
                    content=nodes_wrapper("toc"),
                    info=NodeInfo(context=context),
                    children={"content": self.toc_manager.nested_headers},
                ),
                "plain_toc": Node(
                    content=nodes_wrapper("toc"),
                    info=NodeInfo(context=context),
                    children={"content": self.toc_manager.headers},
                ),
            }
        )
