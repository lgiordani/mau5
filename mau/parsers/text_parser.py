# # mypy: disable-error-code="attr-defined"
# 
# import itertools
# import logging
# 
# from mau.environment.environment import Environment
# from mau.lexers.text_lexer import TextLexer
# from mau.nodes.footnotes import FootnoteNodeData
# from mau.nodes.inline import (
#     StyleNodeData,
#     TextNodeData,
#     VerbatimNodeData,
#     WordNodeData,
# )
# from mau.nodes.macros import (
#     MacroClassNodeData,
#     MacroFootnoteNodeData,
#     MacroHeaderNodeData,
#     MacroImageNodeData,
#     MacroLinkNodeData,
#     MacroNodeData,
# )
# from mau.nodes.node import Node, NodeData, NodeInfo
# from mau.parsers.arguments_parser import ArgumentsParser
# from mau.parsers.base_parser import BaseParser, MauParserException
# from mau.text_buffer import Context
# from mau.token import EOF, EOL, Token, TokenType
# 
# logger = logging.getLogger(__name__)
# 
# # This is a simple map to keep track of the official
# # name of styles introduced by special characters.
# MAP_STYLES = {"_": "underscore", "*": "star", "^": "caret", "~": "tilde"}
# 
# 
# # The TextParser is a recursive parser.
# # The parsing always starts with parse_sentence
# # and from there all components of the text are explored.
# class TextParser(BaseParser):
#     lexer_class = TextLexer
# 
#     def __init__(
#         self,
#         tokens: list[Token],
#         environment: Environment | None = None,
#         parent_node=None,
#     ):
#         super().__init__(tokens, environment, parent_node)
# 
#         # These are the footnotes found in this piece of text.
#         self.footnotes: list[FootnoteNodeData] = []
# 
#         # These are the internal links found
#         # in this piece of text.
#         self.header_links: list[Node] = []
# 
#     def _collect_macro_args(self) -> Token:
#         # A helper that reads macro arguments.
#         # We already consumed the opening
#         # round bracket.
#         #
#         # This is not a trivial task. Arguments
#         # might contain a closing round bracket,
#         # but if the argument is between double quotes
#         # we ignore such brackets.
# 
#         all_args: list[Token] = []
# 
#         # Continue until you find a closing round bracket or EOF.
#         while not (
#             self.tm.peek_token_is(TokenType.LITERAL, ")")
#             or self.tm.peek_token_is(TokenType.EOF)
#         ):
#             # If we find double quotes we need to blindly
#             # collect everything until we meet the closing
#             # double quotes or EOL.
#             if self.tm.peek_token_is(TokenType.LITERAL, '"'):
#                 # Consume the double quotes.
#                 opening_quotes = self.tm.get_token(TokenType.LITERAL, '"')
# 
#                 # Collect and join everything.
#                 # Stop at quotes or EOL.
#                 text_token = self.tm.collect_join(
#                     stop_tokens=[
#                         Token.generate(TokenType.LITERAL, '"'),
#                         EOF,
#                     ],
#                 )
# 
#                 # As we stopped, the next token should be
#                 # double quotes. If not, we hit EOL and
#                 # macro arguments are not closed correctly.
#                 closing_quotes = self.tm.get_token(TokenType.LITERAL, '"')
# 
#                 context = Context.merge_contexts(
#                     opening_quotes.context, closing_quotes.context
#                 )
# 
#                 token = Token(
#                     TokenType.TEXT, value=f'"{text_token.value}"', context=context
#                 )
#             else:
#                 # No double quotes, we can proceed,
#                 # until we find the closing round bracket
#                 # or a comma, which is the arguments separator.
#                 token = self.tm.collect_join(
#                     stop_tokens=[
#                         Token.generate(TokenType.LITERAL, ","),
#                         Token.generate(TokenType.LITERAL, ")"),
#                         EOF,
#                     ],
#                 )
# 
#             # We can add the arguments we found to the
#             # global list.
#             all_args.append(token)
# 
#         # Arguments will be processed by the arguments
#         # parser, for now just merge all of them into
#         # a single piece of text.
#         return Token.from_token_list(all_args)
# 
#     def _process_functions(self):
#         # This is a recursive parser, so the list
#         # of processing functions is pretty small.
#         # We check for the EOL to skip empty
#         # lines and then we move on with a sentence.
#         return [self._process_sentence]
# 
#     def _process_sentence(self) -> bool:
#         # A sentence node is a pure container for other
#         # nodes. The parsing starts at _parse_sentence
#         # and recursively explores the other functions.
# 
#         for node in self._parse_sentence():
#             self._save(node)
# 
#         return True
# 
#     def _parse_sentence(self, stop_tokens=None) -> list[Node]:
#         # Parse a sentence, which is made of multiple
#         # elements identified by _parse_text, before
#         # the EOF, the EOL, or a specific set of tokens
#         # passed as argument.
#         #
#         # Custom stop tokens are useful for example when
#         # parsing text like *text*. In this case we need
#         # to stop parsing when we meet the second asterisk.
# 
#         # The list of nodes we find in this process.
#         content = []
# 
#         # The set of tokens that trigger the end of
#         # the process.
#         stop_tokens = stop_tokens or set()
# 
#         # EOF and EOL always act as stoppers.
#         stop_tokens = stop_tokens.union({EOF, EOL})
# 
#         # Try to parse some text.
#         nodes = self._parse_text(stop_tokens)
# 
#         # Continue parsing text until it
#         # stops returning nodes.
#         while nodes:
#             content.extend(nodes)
#             nodes = self._parse_text(stop_tokens)
# 
#         # Group consecutive WordNodeData nodes into a single TextNodeData.
#         # This scans the nodes we found and tries to collect consecutive
#         # word nodes. We want to merge all of them into a single text node.
# 
#         # This iterator yields (key, group) where key is the grouping
#         # key according to the lambda function. In this case it's
#         # either True if the group contains word nodes or False otherwise.
#         grouped_iter = itertools.groupby(
#             content, lambda x: x.data.__class__ == WordNodeData
#         )
# 
#         # The final list of nodes.
#         nodes = []
# 
#         # Here, key is True if the group is made of word nodes,
#         # which means that we need to merge them.
#         for key, group in grouped_iter:
#             # Read the whole group of
#             # tokens into a list.
#             group_nodes = list(group)
# 
#             if key:
#                 # Merge the values.
#                 text = "".join([n.data.value for n in group_nodes])
# 
#                 # Create the merged context.
#                 context = Context.merge_contexts(
#                     group_nodes[0].info.context,
#                     group_nodes[-1].info.context,
#                 )
# 
#                 node = Node(
#                     parent=self.parent_node,
#                     data=TextNodeData(text),
#                     info=NodeInfo(
#                         context=context,
#                     ),
#                 )
# 
#                 nodes.append(node)
#             else:
#                 # This is a group of non-word nodes.
#                 # Just add them to the list.
#                 nodes.extend(group_nodes)
# 
#         return nodes
# 
#     def _parse_text(self, stop_tokens=None) -> list[Node[NodeData]]:
#         # Parse multiple possible elements: escapes, classes,
#         # macros, verbatim, styles, links, words.
#         # This is the non-recursive part of the parser. It tries
#         # each function until one of them returns a node
#         # without raising an exception.
#         # Each function is wrapped in a context manager to
#         # make sure the index is restored to the original
#         # value when a function raises an exception.
# 
#         stop_tokens = stop_tokens or set()
# 
#         if self.tm.peek_token() in stop_tokens:
#             return []
# 
#         with self.tm:
#             return self._parse_backslash_escaped()
# 
#         with self.tm:
#             return self._parse_macro()
# 
#         with self.tm:
#             return self._parse_verbatim()
# 
#         with self.tm:
#             return self._parse_escaped()
# 
#         with self.tm:
#             return self._parse_style()
# 
#         return self._parse_word()
# 
#     def _parse_backslash_escaped(self) -> list[Node[NodeData]]:
#         # This tries to parse a backslash-escaped element.
#         # Backslash escape allows Mau special characters
#         # to be interpreted as simple text.
#         # E.g "\_" or "\[text\]"
# 
#         # Drop the backslash.
#         backslash = self.tm.get_token(TokenType.LITERAL, "\\")
# 
#         # Get the text.
#         text = self.tm.get_token()
# 
#         # Merge the two contexts.
#         context = Context.merge_contexts(backslash.context, text.context)
# 
#         # Create a word node with the next token.
#         node = Node(
#             parent=self.parent_node,
#             data=WordNodeData(text.value),
#             info=NodeInfo(
#                 context=context,
#             ),
#         )
# 
#         return [node]
# 
#     def _parse_macro(self) -> list[Node[NodeData]]:
#         # Parse a macro in the form
#         # [name](arguments)
# 
#         # Extract the macro name getting rid
#         # of the square brackets.
#         # If the processing succeds, we need the
#         # opening bracket to store the context
#         # in the resulting node.
#         opening_bracket = self.tm.get_token(TokenType.LITERAL, "[")
#         macro_name = self.tm.get_token(TokenType.TEXT).value
#         self.tm.get_token(TokenType.LITERAL, "]")
# 
#         # If this is a macro, there should be an
#         # opening round bracket that contains arguments.
#         self.tm.get_token(TokenType.LITERAL, "(")
# 
#         # Get the macro arguments between round brackets.
#         arguments_token = self._collect_macro_args()
# 
#         # If we get here, we stopped because of
#         # closing brackets or EOL. If we can't find
#         # the closing bracket the next token is EOL
#         # and macro arguments are not closed correctly.
#         closing_bracket = self.tm.get_token(TokenType.LITERAL, ")")
# 
#         # Parse the arguments.
#         parser = ArgumentsParser.lex_and_parse(
#             arguments_token.value,
#             self.environment,
#             *arguments_token.context.start_position,
#             arguments_token.context.source,
#         )
# 
#         context = Context.merge_contexts(
#             opening_bracket.context, closing_bracket.context
#         )
# 
#         # Select the specific parsing function
#         # according to the name of the macro.
# 
#         if macro_name.startswith("@"):
#             return self._parse_macro_control(macro_name, parser, context=context)
# 
#         if macro_name == "link":
#             return self._parse_macro_link(parser, context=context)
# 
#         if macro_name == "header":
#             return self._parse_macro_header_link(parser, context=context)
# 
#         if macro_name == "mailto":
#             return self._parse_macro_mailto(parser, context=context)
# 
#         if macro_name == "image":
#             return self._parse_macro_image(parser, context=context)
# 
#         if macro_name == "footnote":
#             return self._parse_macro_footnote(parser, context=context)
# 
#         if macro_name == "class":
#             return self._parse_macro_class(parser, context)
# 
#         # This is a generic macro, there is no
#         # special code for it.
#         node = Node(
#             parent=self.parent_node,
#             data=MacroNodeData(
#                 name=macro_name,
#                 unnamed_args=[
#                     node.data.value for node in parser.unnamed_argument_nodes
#                 ],
#                 named_args={
#                     key: node.data.value
#                     for key, node in parser.named_argument_nodes.items()
#                 },
#             ),
#             info=NodeInfo(
#                 context=context,
#             ),
#         )
# 
#         return [node]
# 
#     def _parse_verbatim(self) -> list[Node[NodeData]]:
#         # Parse verbatim text between backticks.
#         # E.g. `text`.
# 
#         # Get the verbatim marker.
#         opening_marker = self.tm.get_token(TokenType.LITERAL, "`")
# 
#         # Get all tokens from here to the next
#         # verbatim marker or EOL.
#         content = self.tm.collect_join(
#             [Token.generate(TokenType.LITERAL, "`"), EOL],
#         )
# 
#         # Remove the closing marker.
#         closing_marker = self.tm.get_token(TokenType.LITERAL, "`")
# 
#         # Find the final context.
#         context = Context.merge_contexts(opening_marker.context, closing_marker.context)
# 
#         node = Node(
#             parent=self.parent_node,
#             data=VerbatimNodeData(content.value),
#             info=NodeInfo(context=context),
#         )
# 
#         return [node]
# 
#     def _parse_escaped(self) -> list[Node[NodeData]]:
#         # Parse text between dollar or percent signs.
#         # This is useful when we need to escape multiple
#         # character and we don't want to put a backslash
#         # in front of all of them.
#         # E.g. $escaped$ or %escaped%.
# 
#         # Get the escaped marker.
#         opening_marker = self.tm.get_token(
#             TokenType.LITERAL, value_check_function=lambda x: x in "$%"
#         )
# 
#         # Get the content tokens before the
#         # next escaped marker or EOL.
#         content = self.tm.collect_join(
#             [Token.generate(TokenType.LITERAL, opening_marker.value), EOL],
#         )
# 
#         # Remove the closing marker
#         closing_marker = self.tm.get_token(TokenType.LITERAL, opening_marker.value)
# 
#         # Find the final context.
#         context = Context.merge_contexts(opening_marker.context, closing_marker.context)
# 
#         node = Node(
#             parent=self.parent_node,
#             data=TextNodeData(content.value),
#             info=NodeInfo(context=context),
#         )
# 
#         return [node]
# 
#     def _parse_style(self) -> list[Node[NodeData]]:
#         # Parse text surrounded by style markers.
# 
#         # Get the style marker
#         opening_marker = self.tm.get_token(
#             TokenType.LITERAL,
#             value_check_function=lambda x: x in MAP_STYLES,
#         )
# 
#         # Get everything before the next marker
#         content = self._parse_sentence(
#             stop_tokens={Token.generate(TokenType.LITERAL, opening_marker.value)}
#         )
# 
#         # Get the closing marker
#         closing_marker = self.tm.get_token(TokenType.LITERAL, opening_marker.value)
# 
#         # Find the final context.
#         context = Context.merge_contexts(opening_marker.context, closing_marker.context)
# 
#         node = Node(
#             parent=self.parent_node,
#             data=StyleNodeData(MAP_STYLES[opening_marker.value], content=content),
#             info=NodeInfo(context=context),
#         )
# 
#         return [node]
# 
#     def _parse_word(self) -> list[Node[NodeData]]:
#         # Parse a single word.
# 
#         token = self.tm.get_token()
# 
#         node = Node(
#             parent=self.parent_node,
#             data=WordNodeData(token.value),
#             info=NodeInfo(
#                 context=token.context,
#             ),
#         )
# 
#         return [node]
# 
#     def _parse_macro_link(
#         self, parser: ArgumentsParser, context: Context
#     ) -> list[Node[NodeData]]:
#         # Parse a link macro in the form [link](target, text).
# 
#         # Assign names to arguments.
#         parser.set_names(["target", "text"])
# 
#         # Extract the target of the link.
#         try:
#             target = parser.named_argument_nodes["target"]
#         except KeyError as exc:
#             raise MauParserException(
#                 message="Syntax: [link](TARGET, text)", context=context
#             ) from exc
# 
#         # Extract the text of the link if present.
#         text = parser.named_argument_nodes.get("text")
# 
#         # If the text is present we need to parse it
#         # as it might contain Mau syntax.
#         # If the text is not present we use the
#         # link as text.
#         if text is not None:
#             # Unpack the text initial position.
#             start_line, start_column = text.info.context.start_position
# 
#             # Get the text source.
#             source_filename = text.info.context.source
# 
#             # Parse the text.
#             parser = self.lex_and_parse(
#                 text.data.value,
#                 self.environment,
#                 start_line=start_line,
#                 start_column=start_column,
#                 source_filename=source_filename,
#             )
#             nodes = parser.nodes
#         else:
#             nodes = [
#                 Node(
#                     data=TextNodeData(target.data.value),
#                     info=target.info,
#                 )
#             ]
# 
#         node = Node(
#             parent=self.parent_node,
#             data=MacroLinkNodeData(target.data.value, content=nodes),
#             info=NodeInfo(context=context),
#         )
# 
#         return [node]
# 
#     def _parse_macro_header_link(
#         self, parser: ArgumentsParser, context: Context
#     ) -> list[Node[NodeData]]:
#         # Parse a header link macro in the form [header](header_id, text).
#         # This is similar to a macro link but the URI is an internal header ID.
# 
#         # Assign names to arguments.
#         parser.set_names(["header_id", "text"])
# 
#         # Extract the header ID.
#         try:
#             header_id = parser.named_argument_nodes["header_id"]
#         except KeyError as exc:
#             raise MauParserException(
#                 message="Syntax: [header](ID, text)", context=context
#             ) from exc
# 
#         # Extract the text of the link if present.
#         text = parser.named_argument_nodes.get("text")
# 
#         # If the text is present we need to parse it
#         # as it might contain Mau syntax.
#         # If the text is not present we use the
#         # link as text.
#         nodes = []
#         if text is not None:
#             # Unpack the text initial position.
#             start_line, start_column = text.info.context.start_position
# 
#             # Get the text source.
#             source_filename = text.info.context.source
# 
#             # Parse the text
#             parser = self.lex_and_parse(
#                 text.data.value,
#                 self.environment,
#                 start_line=start_line,
#                 start_column=start_column,
#                 source_filename=source_filename,
#             )
#             nodes = parser.nodes
# 
#         node = Node(
#             parent=self.parent_node,
#             data=MacroHeaderNodeData(header_id.data.value, content=nodes),
#             info=NodeInfo(context=context),
#         )
# 
#         self.header_links.append(node)
# 
#         return [node]
# 
#     def _parse_macro_mailto(
#         self, parser: ArgumentsParser, context: Context
#     ) -> list[Node[NodeData]]:
#         # Parse a mailto macro in the form [mailto](email, text).
#         # This is similar to a macro link but the URI is a `mailto:`.
# 
#         # Assign names to arguments.
#         parser.set_names(["email", "text"])
# 
#         # Extract the linked email and add the `mailto:` prefix.
#         try:
#             target = parser.named_argument_nodes["email"]
#         except KeyError as exc:
#             raise MauParserException(
#                 message="Syntax: [mailto](EMAIL, text)", context=context
#             ) from exc
# 
#         # Extract the text of the link if present.
#         text = parser.named_argument_nodes.get("text")
# 
#         # If the text is present we need to parse it
#         # as it might contain Mau syntax.
#         # If the text is not present we use the
#         # link as text.
#         if text is not None:
#             # Unpack the text initial position.
#             start_line, start_column = text.info.context.start_position
# 
#             # Get the text source.
#             source_filename = text.info.context.source
# 
#             # Parse the text
#             parser = self.lex_and_parse(
#                 text.data.value,
#                 self.environment,
#                 start_line=start_line,
#                 start_column=start_column,
#                 source_filename=source_filename,
#             )
#             nodes = parser.nodes
#         else:
#             nodes = [
#                 Node(
#                     data=TextNodeData(target.data.value),
#                     info=target.info,
#                 )
#             ]
# 
#         node = Node(
#             parent=self.parent_node,
#             data=MacroLinkNodeData(f"mailto:{target.data.value}", content=nodes),
#             info=NodeInfo(context=context),
#         )
# 
#         return [node]
# 
#     def _parse_macro_class(
#         self, parser: ArgumentsParser, context: Context
#     ) -> list[Node[NodeData]]:
#         # Parse a class macro in the form [class](text, class1, class2, ...).
# 
#         # Assign names to arguments.
#         parser.set_names(["text"])
# 
#         # Extract the classes.
#         classes = [node.data.value for node in parser.unnamed_argument_nodes]
# 
#         # Extract the text.
#         try:
#             text = parser.named_argument_nodes["text"]
#         except KeyError as exc:
#             raise MauParserException(
#                 message="Syntax: [class](TEXT, class1, class2, ...)", context=context
#             ) from exc
# 
#         # Unpack the text initial position.
#         start_line, start_column = text.info.context.start_position
# 
#         # Get the text source.
#         source_filename = text.info.context.source
# 
#         # Parse the text
#         parser = self.lex_and_parse(
#             text.data.value,
#             self.environment,
#             start_line=start_line,
#             start_column=start_column,
#             source_filename=source_filename,
#         )
# 
#         node = Node(
#             parent=self.parent_node,
#             data=MacroClassNodeData(classes, content=parser.nodes),
#             info=NodeInfo(context=context),
#         )
# 
#         return [node]
# 
#     def _parse_macro_image(
#         self, parser: ArgumentsParser, context: Context
#     ) -> list[Node[NodeData]]:
#         # Parse an inline image macro in the form [image](uri, alt_text, width, height).
# 
#         # Assign names to arguments.
#         parser.set_names(["uri", "alt_text", "width", "height"])
# 
#         # Extract the URI.
#         try:
#             uri = parser.named_argument_nodes["uri"]
#         except KeyError as exc:
#             raise MauParserException(
#                 message="Syntax: [image](URI, alt_text, width, height)", context=context
#             ) from exc
# 
#         # Get the remaining parameters
#         alt_text = parser.named_argument_nodes.get("alt_text")
#         width = parser.named_argument_nodes.get("width")
#         height = parser.named_argument_nodes.get("height")
# 
#         # Extract the value if the parameter is not None.
#         alt_text = alt_text.data.value if alt_text else None
#         width = width.data.value if width else None
#         height = height.data.value if height else None
# 
#         node = Node(
#             parent=self.parent_node,
#             data=MacroImageNodeData(
#                 uri=uri.data.value,
#                 alt_text=alt_text,
#                 width=width,
#                 height=height,
#             ),
#             info=NodeInfo(context=context),
#         )
# 
#         return [node]
# 
#     def _parse_macro_footnote(
#         self, parser: ArgumentsParser, context: Context
#     ) -> list[Node[NodeData]]:
#         # Parse a footnote macro in the form [footnote](name).
# 
#         # Assign names to arguments.
#         parser.set_names(["name"])
# 
#         # Extract the footnote name.
#         try:
#             name_node = parser.named_argument_nodes["name"]
#         except KeyError as exc:
#             raise MauParserException(
#                 message="Syntax: [footnote](NAME)", context=context
#             ) from exc
# 
#         name = name_node.data.value
# 
#         footnote_data = FootnoteNodeData(name=name)
# 
#         node = Node(
#             parent=self.parent_node,
#             data=MacroFootnoteNodeData(footnote=footnote_data),
#             info=NodeInfo(context=context),
#         )
# 
#         self.footnotes.append(footnote_data)
# 
#         return [node]
# 
#     def _process_test(self, test: str, value: str) -> bool:
#         # Check if the given value passes the test.
# 
#         # Checking equality.
#         if test.startswith("="):
#             test_value = test[1:]
#             return value == test_value
# 
#         # Checking inequality.
#         if test.startswith("!="):
#             test_value = test[2:]
#             return value != test_value
# 
#         # Checking a boolean value.
#         if test.startswith("&"):
#             test_value = test[1:]
# 
#             if test_value not in ["true", "false"]:
#                 raise MauParserException(f"Boolean value '{test_value}' is invalid")
# 
#             # pylint: disable=simplifiable-if-expression
#             boolean_test_value = True if test_value == "true" else False
# 
#             # Boolean AND to check if the boolean
#             # value in the test and the provided
#             # value match.
#             return bool(value) and boolean_test_value
# 
#         raise MauParserException(f"Test '{test}' is not supported")
# 
#     def _parse_macro_control(
#         self, macro_name: str, parser: ArgumentsParser, context: Context
#     ) -> list[Node[NodeData]]:
#         # Parse a class macro in the form [@if:variable:test](true, false).
#         #
#         # Example:
#         #
#         # If the value of flag is 42 return "TRUE", otherwise return "FALSE"
#         # [@if:flag:=42]("TRUE", "FALSE")
# 
#         # Skip the initial `@`
#         operator = macro_name[1:]
# 
#         # Check if the operator is supported.
#         if operator not in ["if", "ifeval"]:
#             raise MauParserException(f"Control operator '{operator}' is not supported")
# 
#         # Assign names to arguments.
#         parser.set_names(["variable", "test", "true_case", "false_case"])
# 
#         # Get the mandatory values
#         try:
#             variable = parser.named_argument_nodes["variable"]
#             test = parser.named_argument_nodes["test"]
#             true_case = parser.named_argument_nodes["true_case"]
#         except KeyError as exc:
#             raise MauParserException(
#                 message=f"Syntax: [{macro_name}](VARIABLE, TEST, TRUE_CASE, false_case)",
#                 context=context,
#             ) from exc
# 
#         # The false case is not mandatory, default is None.
#         false_case = parser.named_argument_nodes.get("false_case")
# 
#         variable_value = self.environment.get(
#             variable.data.value,
#             None,
#         )
#         if variable_value is None:
#             raise MauParserException(f"Variable '{variable}' has not been defined")
# 
#         # Check if the variable value passes the test.
#         test_result = self._process_test(
#             test.data.value,
#             variable_value,
#         )
# 
#         # Get the result value according to the test result.
#         result = true_case if test_result is True else false_case
# 
#         # The operator `ifeval` uses the result value
#         # as the name of a variable.
#         if operator == "ifeval":
#             if result is None:
#                 raise MauParserException(
#                     "Test result negative but evaluation variable has not been defined for that case."
#                 )
# 
#             # Find the value of the variable.
#             variable_value = self.environment.get(
#                 result.data.value,
#             )
# 
#             # If the variable wasn't defined yell at the user.
#             if variable_value is None:
#                 raise MauParserException(
#                     f"Variable '{result.data.value}' has not been defined"
#                 )
# 
#             result.data.value = variable_value
# 
#         nodes = []
#         if result is not None:
#             parser = self.lex_and_parse(
#                 result.data.value,
#                 self.environment,
#                 *result.info.context.start_position,
#                 result.info.context.source,
#             )
#             nodes = parser.nodes
# 
#         return nodes
