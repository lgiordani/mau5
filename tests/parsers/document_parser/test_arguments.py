import pytest

from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.parsers.arguments_parser import Attributes
from mau.parsers.base_parser import MauParserException
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_arguments():
    source = """
    [attr1, attr2, #tag1, *subtype1, key1=value1]
    """

    parser = runner(source)

    assert parser.attributes_stack.pop() == Attributes(
        ["attr1", "attr2"], {"key1": "value1"}, ["tag1"], "subtype1"
    )


def test_arguments_empty():
    source = """
    []
    """

    parser = runner(source)

    assert len(parser.attributes_stack) == 0


def test_arguments_multiple_subtypes():
    source = """
    [*subtype1, *subtype2]
    """

    with pytest.raises(MauParserException):
        assert runner(source)


def test_arguments_support_variables():
    environment = Environment.from_dict({"arg1": "number1", "value1": "42"})
    source = """
    [{arg1},key1={value1}]
    """

    parser = runner(source, environment)

    assert parser.attributes_stack.pop() == Attributes(
        ["number1"],
        {"key1": "42"},
        [],
        None,
    )
