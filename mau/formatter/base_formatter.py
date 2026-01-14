# from abc import ABC, abstractmethod
# 
# from mau.lexers.base_lexer import MauLexerException
# from mau.text_buffer import Context, Position
# from mau.token import Token
# 
# 
# class BaseFormatter(ABC):
#     type = "base"
# 
#     @classmethod
#     def _adjust_context(cls, context: Context):
#         return context.move_to(1, 1)
# 
#     @classmethod
#     def _adjust_position(cls, position: Position):
#         return (position[0] + 1, position[1] + 1)
# 
#     @classmethod
#     def print_tokens(cls, tokens: list[Token]):
#         for token in tokens:
#             print(token)
# 
#     @classmethod
#     @abstractmethod
#     def print_lexer_exception(cls, exc: MauLexerException): ...
