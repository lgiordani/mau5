# from unittest.mock import Mock

# import pytest

# from mau.lexers.base_lexer.lexer import (
#     BaseLexer,
# )
# from mau.test_helpers import (
#     init_lexer_factory,
#     lexer_runner_factory,
# )
# from mau.text_buffer.context import Context
# from mau.tokens.token import Token, TokenType

# init_lexer = init_lexer_factory(BaseLexer)

# runner = lexer_runner_factory(BaseLexer)


# def test_text_buffer_properties():
#     mock_text_buffer = Mock()
#     lex = BaseLexer(mock_text_buffer, Environment())

#     assert lex._current_char == mock_text_buffer.current_char

#     assert lex._current_line == mock_text_buffer.current_line

#     assert lex._tail == mock_text_buffer.tail

#     lex._nextline()
#     mock_text_buffer.nextline.assert_called()

#     lex._skip("four")
#     mock_text_buffer.skip.assert_called_with(4)
