# 
# from mau.environment.environment import Environment
# from mau.lexers.base_lexer import BaseLexer
# from mau.nodes.node import Node
# from mau.text_buffer import Context, TextBuffer
# from mau.token import Token, TokenType
# 
# from .managers.tokens_manager import TokensManager
# 
# 
# class MauParserException(ValueError):
#     def __init__(
#         self, message: str, context: Context | None = None, long_help: str | None = None
#     ):
#         self.message = message
#         self.context = context
#         self.long_help = long_help
# 
# 
# class BaseParser:
#     text_buffer_class = TextBuffer
#     lexer_class = BaseLexer
# 
#     def __init__(
#         self,
#         tokens: list[Token],
#         environment: Environment | None = None,
#         parent_node=None,
#     ):
#         self.tm = TokensManager(tokens)
# 
#         # These are the nodes created by the parsing.
#         self.nodes: list[Node] = []
# 
#         # The last processed token. Used to detect loops.
#         self.last_processed_token: Token = Token(TokenType.EOF, "", Context.empty())
# 
#         # The configuration environment
#         self.environment: Environment = environment or Environment()
# 
#         # This is the parent node of all the nodes
#         # created by this parser
#         self.parent_node = parent_node
# 
#     def _save(self, node):
#         # Store the node.
#         node.set_parent(self.parent_node)
# 
#         self.nodes.append(node)
# 
#     def _process_functions(self):
#         # The parse functions available in this parser
#         return []
# 
#     def parse(self):
#         """
#         Run the parser on the lexed tokens.
#         """
# 
#         # Loop on all lexed tokens until we reach EOF.
# 
#         while not self.tm.peek_token_is(TokenType.EOF):
#             # This detects infinite loops created by incomplete
#             # parsing functions. Those functions keep trying
#             # to parse the same token, so if we spot that
#             # we are doing it we should raise an error.
#             next_token = self.tm.peek_token()
# 
#             if (
#                 next_token == self.last_processed_token
#                 and next_token.context == self.last_processed_token.context
#             ):
#                 raise MauParserException(
#                     f"Loop detected, cannot parse token {next_token}",
#                     next_token.context,
#                 )  # pragma: no cover
#             else:
#                 self.last_processed_token = next_token
# 
#             # Here we run all parsing functions provided by
#             # the parser until one returns a sensible result.
#             result = False
#             for process_function in self._process_functions():
#                 # The context manager wraps the function so that
#                 # any exception leaves the parsed tokens as they
#                 # were at the beginning of the function execution.
#                 #
#                 # If the parse function is successful it returns
#                 # True. If the function raises an exception the
#                 # variable result is not set and the value is False.
#                 # Any other result returned by the function
#                 # is ignored.
#                 with self.tm:
#                     result = process_function()
# 
#                 if result is True:
#                     # True means the function was successful
#                     # and we can stop the loop.
#                     break
# 
#             # If we get here and result is still False
#             # we didn't find any function to parse the
#             # current token.
#             if result is False:
#                 raise MauParserException(
#                     "Cannot parse token",
#                     self.tm.peek_token().context,
#                 )
# 
#     @classmethod
#     def lex_and_parse(
#         cls,
#         text: str,
#         environment: Environment | None,
#         start_line: int = 0,
#         start_column: int = 0,
#         source_filename: str | None = None,
#         **kwargs,
#     ):  # pragma: no cover
#         text_buffer = cls.text_buffer_class(
#             text, start_line, start_column, source_filename
#         )
# 
#         lexer = cls.lexer_class(text_buffer, environment)
#         lexer.process()
# 
#         parser = cls(lexer.tokens, environment, **kwargs)
#         parser.parse()
#         parser.finalise()
# 
#         return parser
# 
#     def finalise(self):  # pragma: no cover
#         pass
