from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.parsers.arguments_parser.parser import Arguments
from mau.parsers.document_parser.managers.arguments_manager import ArgumentsManager
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_arguments_manager():
    am = ArgumentsManager()

    assert am.pop() is None
    assert am.pop_or_default() == Arguments()


def test_arguments_manager_push_and_pop():
    am = ArgumentsManager()
    test_arguments = Arguments(unnamed_args=["42"])

    am.push(test_arguments)

    assert am.pop() is test_arguments
    assert am.pop() is None


def test_arguments_manager_pop_or_default():
    am = ArgumentsManager()
    test_arguments = Arguments(unnamed_args=["42"])

    am.push(test_arguments)

    assert am.pop_or_default() is test_arguments
    assert am.pop_or_default() == Arguments()
