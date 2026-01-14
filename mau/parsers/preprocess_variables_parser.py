# from mau.lexers.preprocess_variables_lexer import PreprocessVariablesLexer
# from mau.nodes.inline import TextNodeData
# from mau.nodes.node import Node, NodeInfo
# from mau.parsers.base_parser import BaseParser, MauParserException
# from mau.text_buffer import Context
# from mau.token import Token, TokenType
# 
# 
# # The PreprocessVariablesParser processes tokens,
# # scans for variables in the form `{name}`,
# # replaces them, and finally outputs a single
# # node that contains the whole text.
# class PreprocessVariablesParser(BaseParser):
#     lexer_class = PreprocessVariablesLexer
# 
#     def _process_escaped_char(self):
#         # Process escaped characters.
#         # This checks if the escaped character
#         # is the opening or closing curly brace, in
#         # which case it stores it as it is
#         # preventing the variable replacement
#         # process to take place.
# 
#         # Check is the token is an escape backslash.
#         backslash = self.tm.get_token(TokenType.LITERAL, "\\")
# 
#         # Get the following character.
#         char = self.tm.get_token()
# 
#         # If the character is not a curly brace
#         # restore the escape backslash.
#         if char.value not in "{}":
#             char.value = f"\\{char.value}"
# 
#         # Merge the two contexts.
#         context = Context.merge_contexts(backslash.context, char.context)
# 
#         self._save(
#             Node(
#                 data=TextNodeData(char.value),
#                 info=NodeInfo(context=context),
#             )
#         )
# 
#         return True
# 
#     def _process_verbatim(self):
#         # Process text surrounded by backticks.
#         # Such text should be left untouched.
#         # Verbatim is often used for code and
#         # chances are that the syntax `{name}`
#         # might be used as curly braces are
#         # widespread in coding.
# 
#         # Check if the token is the opening backtick.
#         opening_tick = self.tm.get_token(TokenType.LITERAL, "`")
# 
#         # Get everything before the closing backtick.
#         text = self.tm.collect_join(
#             [Token.generate(TokenType.LITERAL, "`")],
#             preserve_escaped_stop_tokens=True,
#         )
# 
#         # Check if the token is the closing backtick.
#         closing_tick = self.tm.get_token(TokenType.LITERAL, "`")
# 
#         # Find the final context.
#         context = Context.merge_contexts(opening_tick.context, closing_tick.context)
# 
#         # Restore the original form of the text
#         # with the surrounding backticks.
#         text_content = f"`{text.value}`"
# 
#         self._save(
#             Node(
#                 data=TextNodeData(text_content),
#                 info=NodeInfo(context=context),
#             )
#         )
# 
#         return True
# 
#     def _process_curly(self):
#         # This is the core of the replacement process.
#         # If the function detects text between curly
#         # braces it uses it as the name of a variable
#         # and replaces it.
# 
#         # Check if the token is the opening curly brace.
#         opening_bracket = self.tm.get_token(TokenType.LITERAL, "{")
# 
#         # Get everything beforethe closing brace.
#         variable_name = self.tm.collect_join(
#             stop_tokens=[Token.generate(TokenType.LITERAL, "}")]
#         )
# 
#         # Check if the token is the closing curly brace.
#         closing_bracket = self.tm.get_token(TokenType.LITERAL, "}")
# 
#         # Find the final context.
#         context = Context.merge_contexts(
#             opening_bracket.context, closing_bracket.context
#         )
# 
#         try:
#             # Extract from the environment the variable
#             # mentioned between curly braces.
#             variable_value = self.environment[variable_name.value]
#         except KeyError as exp:
#             raise MauParserException(
#                 f'Variable "{variable_name}" has not been defined.',
#                 context=context,
#             ) from exp
# 
#         # Boolean variables shouldn't be printed.
#         # Replace them with an empty string.
#         if variable_value in [True, False]:
#             variable_value = ""
# 
#         self._save(
#             Node(
#                 data=TextNodeData(variable_value),
#                 info=NodeInfo(context=context),
#             )
#         )
# 
#         return True
# 
#     def _process_pass(self):
#         # None of the previous functions succeeded,
#         # so we are in front of a pure text token.
#         # Just store it and move on.
#         text_token = self.tm.get_token()
# 
#         self._save(
#             Node(
#                 data=TextNodeData(text_token.value),
#                 info=NodeInfo(context=text_token.context),
#             )
#         )
# 
#         return True
# 
#     def _process_functions(self):
#         return [
#             self._process_escaped_char,
#             self._process_verbatim,
#             self._process_curly,
#             self._process_pass,
#         ]
# 
#     def parse(self):
#         # After having parsed the text and replaced the
#         # variables, this parser should eventually return
#         # a single piece of text.
#         # So, after the standard parsing, we create a
#         # single TEXT node from all the nodes that
#         # we processed.
# 
#         super().parse()
# 
#         if not self.nodes:
#             return
# 
#         text_tokens = [
#             Token(
#                 TokenType.TEXT,
#                 i.data.value,  # type: ignore[attr-defined]
#                 i.info.context,
#             )
#             for i in self.nodes
#         ]
# 
#         token = Token.from_token_list(text_tokens)
# 
#         self.nodes = [
#             Node(
#                 data=TextNodeData(token.value),
#                 info=NodeInfo(context=token.context),
#             )
#         ]
