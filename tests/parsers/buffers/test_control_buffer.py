import pytest

from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.buffers.control_buffer import ControlBuffer, Control
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_control_buffer():
    cb = ControlBuffer()

    assert cb.pop() is None


def test_control_buffer_push_and_pop():
    cb = ControlBuffer()
    test_control = Control(
        "if",
        "answer",
        "==",
        "42",
        generate_context(0, 1),
    )

    cb.push(test_control)

    assert cb.pop() == test_control
    assert cb.pop() is None


def test_control_buffer_push_twice():
    cb = ControlBuffer()
    test_control1 = Control(
        "if",
        "answer",
        "==",
        "42",
        generate_context(0, 1),
    )
    test_control2 = Control(
        "if",
        "answer",
        "!=",
        "43",
        generate_context(0, 1),
    )

    cb.push(test_control1)
    cb.push(test_control2)

    assert cb.pop() == test_control2
    assert cb.pop() is None


def test_control_process_wrong_operator():
    with pytest.raises(MauParserException) as exc:
        Control("notanoperator", "answer", "==", "42", context=generate_context(1, 2))

    assert exc.value.context == generate_context(1, 2)


def test_control_process_if_operator_variable_not_defined_equality():
    environment = Environment()

    c = Control("if", "answer", "==", "42", generate_context(0, 0))

    assert c.process(environment) is False


def test_control_process_if_operator_variable_defined_equality():
    environment = Environment.from_dict({"answer": "42"})

    c = Control("if", "answer", "==", "42", generate_context(0, 0))

    assert c.process(environment) is True


def test_control_process_if_operator_variable_not_defined_inequality():
    environment = Environment()

    c = Control("if", "answer", "!=", "42", generate_context(0, 0))

    assert c.process(environment) is True


def test_control_process_if_operator_variable_defined_inequality():
    environment = Environment.from_dict({"answer": "42"})

    c = Control("if", "answer", "!=", "42", generate_context(0, 0))

    assert c.process(environment) is False
