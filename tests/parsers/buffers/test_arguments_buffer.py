from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.parsers.arguments_parser.parser import Arguments
from mau.parsers.document_parser.buffers.arguments_buffer import ArgumentsBuffer
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_arguments_buffer():
    ab = ArgumentsBuffer()

    assert ab.pop() is None
    assert ab.pop_or_default() == Arguments()


def test_arguments_buffer_push_and_pop():
    ab = ArgumentsBuffer()
    test_arguments = Arguments(unnamed_args=["42"])

    ab.push(test_arguments)

    assert ab.pop() is test_arguments
    assert ab.pop() is None


def test_arguments_buffer_pop_or_default():
    ab = ArgumentsBuffer()
    test_arguments = Arguments(unnamed_args=["42"])

    ab.push(test_arguments)

    assert ab.pop_or_default() is test_arguments
    assert ab.pop_or_default() == Arguments()
