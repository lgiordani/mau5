from unittest.mock import patch

from mau.lexers.document_lexer import DocumentLexer
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


@patch("mau.parsers.managers.toc_manager.default_header_internal_id")
def test_default_engine_adds_headers_to_global_toc(mock_header_internal_id):
    mock_header_internal_id.return_value = "XXYY"

    source = """
    ----
    = Block header
    ----
    """

    parser = runner(source)

    assert len(parser.toc_manager.headers) == 1


def test_default_engine_adds_footnotes_to_global_toc():
    source = """
    ----
    Some text with a [footnote](note).

    [footnote=note]
    ####
    Some text.
    ####
    ----
    """

    parser = runner(source)

    assert len(parser.footnotes_manager.footnotes) == 1
    assert len(parser.footnotes_manager.bodies) == 1
    assert "note" in parser.footnotes_manager.bodies
