from mau.text_buffer.context import Context
from mau.tokens.token import Token, TokenType
from mau.test_helpers import generate_context


def test_token_accepts_type_and_value():
    token = Token(TokenType.TEXT, "somevalue")

    assert token.type == TokenType.TEXT
    assert token.value == "somevalue"
    assert token != "somevalue"


def test_token_keeps_value_none():
    token = Token(TokenType.TEXT, None)

    assert token.type == TokenType.TEXT
    assert token.value == ""


def test_token_value_defaults_to_none():
    token = Token(TokenType.TEXT)

    assert token.type == TokenType.TEXT
    assert token.value == ""


def test_token_equality():
    assert Token(TokenType.TEXT, "somevalue") == Token(TokenType.TEXT, "somevalue")


def test_token_length():
    token = Token(TokenType.TEXT, "somevalue")

    assert len(token) == len("somevalue")
    assert bool(token) is True


def test_empty_token_has_length_zero():
    token = Token(TokenType.TEXT)

    assert len(token) == 0
    assert bool(token) is True


def test_token_accepts_context():
    context = generate_context(0, 0, 1, 42)

    token = Token(TokenType.TEXT, "somevalue", context=context)

    assert token.type == TokenType.TEXT
    assert token.value == "somevalue"
    assert token.context == context


def test_token_equality_ignores_context():
    context = generate_context(0, 0, 1, 42)

    assert Token(TokenType.TEXT, "somevalue", context=context) == Token(
        TokenType.TEXT, "somevalue"
    )
    assert Token(TokenType.TEXT, "somevalue") == Token(
        TokenType.TEXT, "somevalue", context=context
    )


def test_token_equality_accepts_none():
    assert Token(TokenType.TEXT, "somevalue") is not None


def test_token_equality_considers_value():
    assert Token(TokenType.TEXT, "somevalue") != Token(TokenType.TEXT)
