# class BaseLexer:
#     """
#     The base class for lexers.
#     The lexer decomposes the input text into a list of tokens
#     and provides basic navigation functions in the
#     output results.

#     This class provides the base machinery for a lexer,
#     running a sequence of functions until one of them
#     successfully identifies a token.
#     """

#     def __init__(self, text_buffer: TextBuffer, environment: Environment | None = None):
#         self.text_buffer: TextBuffer = text_buffer

#         # This is the list of the tokens that
#         # the lexer extracts.
#         self.tokens: list[Token] = []

#         # The last visited context. Used to detect loops.
#         self.last_visited_context: Context | None = None

#         # The configuration environment.
#         self.environment: Environment = environment or Environment()
