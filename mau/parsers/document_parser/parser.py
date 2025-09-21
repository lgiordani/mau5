# pylint: disable=too-many-lines

from __future__ import annotations

import hashlib
import re
from functools import partial

from mau.environment.environment import Environment

# from mau.lexers.base_lexer.lexer import TokenTypes as TokenType
from mau.lexers.document_lexer.lexer import DocumentLexer

# from mau.lexers.document_lexer.lexer import TokenTypes as TokenType
# from mau.nodes.block import BlockGroupNode, BlockNode
# from mau.nodes.content import ContentImageNode, ContentNode
from mau.nodes.node import Node, NodeContent

# from mau.nodes.page import ContainerNode
# from mau.nodes.paragraph import ParagraphNode
from mau.parsers.base_parser.parser import BaseParser

# from mau.parsers.footnotes import FootnotesManager
from mau.parsers.preprocess_variables_parser.parser import PreprocessVariablesParser
from mau.parsers.text_parser.parser import TextParser
from mau.tokens.token import Token, TokenType

from .managers.arguments_manager import ArgumentsManager
from .managers.header_links_manager import HeaderLinksManager
from .managers.title_buffer import TitleBuffer
from .managers.toc_manager import TocManager
from .processors.arguments import arguments_processor
from .processors.block import block_processor
from .processors.command import command_processor
from .processors.header import header_processor
from .processors.horizontal_rule import horizontal_rule_processor
from .processors.include import include_processor
from .processors.list import list_processor
from .processors.paragraph import paragraph_processor
from .processors.title import title_processor
from .processors.variable_definition import variable_definition_processor

# TODO check if we really want to use the current context
# TODO self.tm.peek_token(with arguments) is basically self.tm.peek_token_is()


def header_anchor(text, level):  # pragma: no cover
    """
    Return a sanitised anchor for a header.
    """

    # Everything lowercase
    sanitised_text = text.lower()

    # Get only letters, numbers, dashes, spaces, and dots
    sanitised_text = "".join(re.findall("[a-z0-9-\\. ]+", sanitised_text))

    # Remove multiple spaces
    sanitised_text = "-".join(sanitised_text.split())

    hashed_value = hashlib.md5(f"{level} {text}".encode("utf-8")).hexdigest()[:4]

    return f"{sanitised_text}-{hashed_value}"


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
        parent_position=None,
    ):
        super().__init__(tokens, environment, parent_node, parent_position)

        self.header_links_manager: HeaderLinksManager = HeaderLinksManager()
        #     self.footnotes_manager = FootnotesManager(self)
        self.toc_manager: TocManager = TocManager()
        self.arguments_manager: ArgumentsManager = ArgumentsManager()
        self.title_buffer: TitleBuffer = TitleBuffer()

        #     # These are the default block aliases
        #     # If subtype is not set it will be the alias itself.
        #     self.block_aliases = {
        #         "source": {
        #             "subtype": None,
        #             "mandatory_args": ["language"],
        #             "defaults": {"engine": "source", "language": "text"},
        #         },
        #         "footnote": {
        #             "subtype": None,
        #             "mandatory_args": ["name"],
        #             "defaults": {"engine": "footnote"},
        #         },
        #         "admonition": {
        #             "mandatory_args": ["class", "icon"],
        #         },
        #     }

        #     # Iterate through block definitions passed as variables
        #     self.block_aliases.update(
        #         self.environment.getvar(
        #             "mau.parser.block_definitions", Environment()
        #         ).asdict()
        #     )

        #     # This is a buffer for a control
        #     self.control = (None, None, None)

        # This is the function used to create the header
        # anchors.
        self.header_anchor = self.environment.getvar(
            "mau.parser.header_anchor_function", header_anchor
        )

        # The last index in the latest ordered list,
        # used to calculate the beginning value of them
        # next one when start=auto
        self.latest_ordered_list_index = 0

    #     # This is the dictionary of block groups
    #     # defineed in the document
    #     self.grouped_blocks = {}

    #     # This is the final output of the parser
    #     self.output = {}

    def _process_functions(self):
        # All the functions that this parser provides.

        return [
            self._process_eol,
            partial(horizontal_rule_processor, self),
            partial(variable_definition_processor, self),
            partial(command_processor, self),
            partial(title_processor, self),
            #         self._process_control,
            partial(arguments_processor, self),
            partial(header_processor, self),
            partial(block_processor, self),
            partial(include_processor, self),
            partial(list_processor, self),
            partial(paragraph_processor, self),
        ]

    # def _push_control(self, operator, statement, context):
    #     self.control = (operator, statement, context)

    # def _pop_control(self):
    #     # This return the title and resets the
    #     # cached one, so no other block will
    #     # use it.
    #     operator, statement, context = self.control
    #     self._reset_control()

    #     if operator is None:
    #         return True

    #     if operator != "if":
    #         self._error(f"Control operator '{operator}' is not supported")

    #     try:
    #         variable, test = statement.split(":", 1)
    #     except ValueError:
    #         self._error(f"Statement '{statement}' is not in the form variable:test")

    #     variable_value = self.environment.getvar(variable, None)

    #     if variable_value is None:
    #         self._error(f"Variable '{variable}' has not been defined")

    #     if test.startswith("="):
    #         value = test[1:]
    #         return variable_value == value

    #     if test.startswith("!="):
    #         value = test[2:]

    #         return variable_value != value

    #     if test.startswith("&"):
    #         value = test[1:]

    #         if value not in ["true", "false"]:
    #             self._error(f"Boolean value '{value}' is invalid")

    #         # pylint: disable=simplifiable-if-expression
    #         value = True if value == "true" else False

    #         return variable_value and value

    #     self._error(f"Test '{test}' is not supported")

    # def _reset_control(self):
    #     self.control = (None, None, None)

    # def _collect_text_content(self):
    #     # Collects all adjacent text tokens
    #     # into a single string

    #     if not self.tm.peek_token_is(TokenType.TEXT):  # pragma: no cover
    #         return None

    #     values = []

    #     # Get all tokens
    #     while self.tm.peek_token_is(TokenType.TEXT):
    #         values.append(self.tm.get_token().value)
    #         self.tm.get_token(TokenType.EOL)

    #     return " ".join(values)

    def _parse_text(self, text, context=None) -> list[Node[NodeContent]]:
        # This parses a piece of text.
        # It runs the text through the preprocessor to
        # replace variables, then parses it storing
        # footnotes and internal links, and finally
        # returns the nodes.

        # Find the context of the parsing.
        current_context = context or self.tm.current_token.context

        # Replace variables
        preprocess_parser = PreprocessVariablesParser.lex_and_parse(
            text,
            current_context,
            self.environment,
        )

        # If the preprocessor doesn't return any
        # node we can stop here.
        if not preprocess_parser.nodes:
            return []

        # The preprocess parser outputs a single node.
        text = preprocess_parser.nodes[0].content.value

        # Parse the text
        text_parser = TextParser.lex_and_parse(
            text,
            current_context,
            self.environment,
        )

        # Extract the footnote mentions
        # found in this piece of text
        # TODO
        # self.footnotes_manager.update_mentions(text_parser.footnotes)

        # Extract the header links found in this piece of text.
        self.header_links_manager.add_links(text_parser.header_links)

        return text_parser.nodes

    def _process_eol(self) -> bool:
        # This simply ignores the end of line.

        self.tm.get_token(TokenType.EOL)

        return True

    # def _process_control(self):
    #     # Parse a control statement in the form
    #     #
    #     # @operator:control_statement

    #     # Parse the mandatory @
    #     at = self.tm.get_token(TokenType.CONTROL, "@")

    #     # Get the operator
    #     operator = self.tm.get_token(TokenType.TEXT).value

    #     # Discard the :
    #     self.tm.get_token(TokenType.LITERAL, ":")

    #     # Get the statement
    #     statement = self.tm.get_token(TokenType.TEXT).value

    #     self.tm.get_token(TokenType.EOL)

    #     self._push_control(operator, statement, at.context)

    #     return True

    def _collect_lines(self, stop_tokens: list[Token]) -> list[str]:
        # This collects several lines of text in a list
        # until it gets to a line that begins with one
        # of the tokens listed in stop_tokens.
        # It is useful for block or other elements that
        # are clearly surrounded by delimiters.
        lines = []

        while self.tm.peek_token() not in stop_tokens:
            lines.append(self.tm.collect_join([Token(TokenType.EOL)]))
            self.tm.get_token(TokenType.EOL)

        return lines

    # def _parse_group_engine(self, block):
    #     block.args, block.kwargs = self._set_names_and_defaults(
    #         block.args,
    #         block.kwargs,
    #         ["group", "position"],
    #     )

    #     group_name = block.kwargs.pop("group")
    #     position = block.kwargs.pop("position")

    #     group = self.grouped_blocks.setdefault(group_name, {})

    #     if position in group:
    #         self._error(
    #             f"Block with position {position} already defined in group {group_name}"
    #         )

    #     group[position] = block

    #     self._parse_block_content_update(block)

    # def _parse_footnote_engine(self, block):
    #     # The current block contains footnote data.
    #     # Extract the content and store it in
    #     # the footnotes manager.
    #     name = block.kwargs.pop("name")

    #     content_parser = DocumentParser.analyse(
    #         "\n".join(block.children),
    #         self._current_token.context,
    #         self.environment,
    #         parent_node=block,
    #     )

    #     self.footnotes_manager.add_data(name, content_parser.nodes)

    # def _parse_content_image(self, uris, subtype, args, kwargs, tags):
    #     # Parse a content image in the form
    #     #
    #     # << image:uri,alt_text,classes
    #     #
    #     # alt_text is the alternate text to use is the image is not reachable
    #     # and classes is a comma-separated list of classes

    #     # Consume the arguments
    #     args, kwargs = self._set_names_and_defaults(
    #         args,
    #         kwargs,
    #         ["alt_text", "classes"],
    #         {"alt_text": None, "classes": None},
    #     )

    #     uri = uris[0]
    #     alt_text = kwargs.pop("alt_text")
    #     classes = kwargs.pop("classes")

    #     if classes:
    #         classes = classes.split(",")

    #     node = ContentImageNode(
    #         uri=uri,
    #         alt_text=alt_text,
    #         classes=classes,
    #         subtype=subtype,
    #         args=args,
    #         kwargs=kwargs,
    #         tags=tags,
    #     )

    #     node.title = self._pop_title(node)
    #     self._save(node)

    #     return True

    # def _parse_standard_content(self, content_type, uris, subtype, args, kwargs, tags):
    #     # This is the fallback for an unknown content type

    #     node = ContentNode(
    #         content_type=content_type,
    #         uris=uris,
    #         subtype=subtype,
    #         args=args,
    #         kwargs=kwargs,
    #         tags=tags,
    #     )

    #     node.title = self._pop_title(node)
    #     self._save(node)

    #     return True

    def finalise(self):
        super().finalise()

        #     # This processes all footnotes stored in
        #     # the manager merging mentions and data
        #     # and updating the nodes that contain
        #     # a list of footnotes
        #     self.footnotes_manager.process_footnotes()

        # This processes all links stored in
        # the manager linking them to the
        # correct headers
        self.header_links_manager.process()

        # Process ToC nodes.
        self.toc_manager.process()

    #     # The content wrappers are cloned to avoid
    #     # storing the whole parsed document in the
    #     # environment.
    #     content_wrapper = self.environment.getvar(
    #         "mau.parser.content_wrapper", ContainerNode()
    #     ).clone()
    #     content_wrapper.children = self.nodes

    #     toc_wrapper = self.environment.getvar(
    #         "mau.parser.toc_wrapper", ContainerNode()
    #     ).clone()
    #     toc_wrapper.add_children([toc])

    #     self.output.update(
    #         {
    #             "content": content_wrapper,
    #             "toc": toc_wrapper,
    #         }
    #     )
