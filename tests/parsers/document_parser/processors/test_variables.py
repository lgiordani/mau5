import pytest

from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.variable_definition import (
    variable_definition_processor,
)
from mau.test_helpers import (
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_variable_definition_without_value_is_empty():
    source = ":attr:"

    parser: DocumentParser = init_parser(source)

    with pytest.raises(MauParserException) as exc:
        variable_definition_processor(parser)

    assert (
        exc.value.message
        == "Error in variable definition. Variable 'attr' has no value."
    )
    assert exc.value.context == generate_context(0, 0)


def test_variable_definition_with_plus_is_true():
    source = ":+attr:"

    parser: DocumentParser = init_parser(source)
    variable_definition_processor(parser)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr": "true"}


def test_variable_definition_with_minus_is_false():
    source = ":-attr:"

    parser: DocumentParser = init_parser(source)
    variable_definition_processor(parser)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr": "false"}


def test_variable_definition_flag_plus_ignores_value():
    source = ":+attr:42"

    parser: DocumentParser = init_parser(source)
    variable_definition_processor(parser)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr": "true"}


def test_variable_definition_flag_minus_ignores_value():
    source = ":-attr:42"

    parser: DocumentParser = init_parser(source)
    variable_definition_processor(parser)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr": "false"}


def test_variable_definition_with_value_is_loaded():
    source = ":attr:42"

    parser: DocumentParser = init_parser(source)
    variable_definition_processor(parser)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr": "42"}


def test_variable_definition_multiple():
    source = """
    :attr1:42
    :attr2:43
    """

    parser: DocumentParser = runner(source)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr1": "42", "attr2": "43"}


def test_variable_definition_value_can_be_any_text():
    source = ":attr:[footnote](http://some.domain/path)"

    parser: DocumentParser = init_parser(source)
    variable_definition_processor(parser)

    assert parser.nodes == []
    assert parser.environment.asdict() == {
        "attr": "[footnote](http://some.domain/path)",
    }


def test_variable_definition_with_namespace():
    source = ":meta.attr:42"

    parser: DocumentParser = init_parser(source)
    variable_definition_processor(parser)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"meta": {"attr": "42"}}


def test_variable_definition_with_multiple_dots():
    source = ":meta.category.attr:42"

    parser: DocumentParser = init_parser(source)
    variable_definition_processor(parser)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"meta": {"category": {"attr": "42"}}}
