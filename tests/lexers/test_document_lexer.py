from unittest.mock import mock_open, patch

from mau.lexers.base_lexer import TokenType
from mau.lexers.document_lexer import DocumentLexer
from mau.test_helpers import dedent, init_lexer_factory, lexer_runner_factory
from mau.text_buffer.text_buffer import TextBuffer
from mau.tokens.token import Token

init_lexer = init_lexer_factory(DocumentLexer)

runner = lexer_runner_factory(DocumentLexer)


def test_horizontal_rule():
    lex = runner("---")

    assert lex.tokens == [
        Token(TokenType.HORIZONTAL_RULE, "---"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escape_line():
    lex = runner(r"\[name]")

    assert lex.tokens == [
        Token(TokenType.TEXT, r"\[name]"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escape_line_beginning_with_backslash():
    lex = runner(r"\\[name]")

    assert lex.tokens == [
        Token(TokenType.TEXT, r"\\[name]"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_arguments():
    lex = runner("[name]")

    assert lex.tokens == [
        Token(TokenType.ARGUMENTS, "["),
        Token(TokenType.TEXT, "name"),
        Token(TokenType.LITERAL, "]"),
        Token(TokenType.EOL, ""),
        Token(TokenType.EOF, ""),
    ]


def test_attributes_no_closing_bracket():
    lex = runner("[name")

    assert lex.tokens == [
        Token(TokenType.TEXT, "[name"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_attributes_marker_in_text():
    lex = runner("Not [attributes]")

    assert lex.tokens == [
        Token(TokenType.TEXT, "Not [attributes]"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_variable_definition():
    lex = runner(":variable:value123")

    assert lex.tokens == [
        Token(TokenType.VARIABLE, ":"),
        Token(TokenType.TEXT, "variable"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.TEXT, "value123"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_variable_flag_true():
    lex = runner(":+variable:")

    assert lex.tokens == [
        Token(TokenType.VARIABLE, ":"),
        Token(TokenType.TEXT, "+variable"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_variable_flag_false():
    lex = runner(":-variable:")

    assert lex.tokens == [
        Token(TokenType.VARIABLE, ":"),
        Token(TokenType.TEXT, "-variable"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_variable_marker_in_text():
    lex = runner("Not a :variable:")

    assert lex.tokens == [
        Token(TokenType.TEXT, "Not a :variable:"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_variable_marker_with_space():
    lex = runner(": not a variable:")

    assert lex.tokens == [
        Token(TokenType.TEXT, ": not a variable:"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_variable_definition_accepted_characters():
    lex = runner(":abcAB.C0123-_:value123")

    assert lex.tokens == [
        Token(TokenType.VARIABLE, ":"),
        Token(TokenType.TEXT, "abcAB.C0123-_"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.TEXT, "value123"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_multiple_lines():
    lex = runner(
        dedent(
            """
            This is text
            split into multiple lines

            with an empty line
            """
        )
    )

    assert lex.tokens == [
        Token(TokenType.TEXT, "This is text"),
        Token(TokenType.EOL),
        Token(TokenType.TEXT, "split into multiple lines"),
        Token(TokenType.EOL),
        Token(TokenType.EOL),
        Token(TokenType.TEXT, "with an empty line"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_title():
    lex = runner(".A title")

    assert lex.tokens == [
        Token(TokenType.TITLE, "."),
        Token(TokenType.TEXT, "A title"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_title_with_space():
    lex = runner(".  A title")

    assert lex.tokens == [
        Token(TokenType.TITLE, "."),
        Token(TokenType.TEXT, "A title"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_command():
    lex = runner("::command:arg0,arg1")

    assert lex.tokens == [
        Token(TokenType.COMMAND, "::"),
        Token(TokenType.TEXT, "command"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.TEXT, "arg0,arg1"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_command_without_arguments():
    lex = runner("::command:")

    assert lex.tokens == [
        Token(TokenType.COMMAND, "::"),
        Token(TokenType.TEXT, "command"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_command_with_space():
    lex = runner("::  command:")

    assert lex.tokens == [
        Token(TokenType.COMMAND, "::"),
        Token(TokenType.TEXT, "command"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_comment():
    lex = runner("// Some comment")

    assert lex.tokens == [
        Token(TokenType.COMMENT, "// Some comment"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_multiline_comment():
    lex = runner(
        dedent(
            """
            ////
            Some comment

               another line
            ////
            """
        )
    )

    assert lex.tokens == [
        Token(TokenType.MULTILINE_COMMENT, "////"),
        Token(TokenType.EOL),
        Token(TokenType.TEXT, "Some comment"),
        Token(TokenType.EOL),
        Token(TokenType.EOL),
        Token(TokenType.TEXT, "   another line"),
        Token(TokenType.EOL),
        Token(TokenType.MULTILINE_COMMENT, "////"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_include_content():
    lex = runner("<<type:/path/to/it.jpg")

    assert lex.tokens == [
        Token(TokenType.CONTENT, "<<"),
        Token(TokenType.TEXT, "type"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.TEXT, "/path/to/it.jpg"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_include_content_without_arguments():
    lex = runner("<<type:")

    assert lex.tokens == [
        Token(TokenType.CONTENT, "<<"),
        Token(TokenType.TEXT, "type"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_include_content_with_space():
    lex = runner("<<  type:/path/to/it.jpg")

    assert lex.tokens == [
        Token(TokenType.CONTENT, "<<"),
        Token(TokenType.TEXT, "type"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.TEXT, "/path/to/it.jpg"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_unordered_list():
    lex = runner("* Item")

    assert lex.tokens == [
        Token(TokenType.LIST, "*"),
        Token(TokenType.TEXT, "Item"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_unordered_list_leading_space():
    text_buffer = TextBuffer("  * Item")
    lex = init_lexer(text_buffer)
    lex.process()

    assert lex.tokens == [
        Token(TokenType.LIST, "*"),
        Token(TokenType.TEXT, "Item"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_unordered_list_trailing_space():
    lex = runner("*  Item")

    assert lex.tokens == [
        Token(TokenType.LIST, "*"),
        Token(TokenType.TEXT, "Item"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_unordered_list_multiple_stars():
    lex = runner("*** Item")

    assert lex.tokens == [
        Token(TokenType.LIST, "***"),
        Token(TokenType.TEXT, "Item"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_ordered_list():
    lex = runner("# Item")

    assert lex.tokens == [
        Token(TokenType.LIST, "#"),
        Token(TokenType.TEXT, "Item"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_ordered_list_multiple_stars():
    lex = runner("### Item")

    assert lex.tokens == [
        Token(TokenType.LIST, "###"),
        Token(TokenType.TEXT, "Item"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_header():
    lex = runner("=Header")

    assert lex.tokens == [
        Token(TokenType.HEADER, "="),
        Token(TokenType.TEXT, "Header"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_header_with_space():
    lex = runner("=  Header")

    assert lex.tokens == [
        Token(TokenType.HEADER, "="),
        Token(TokenType.TEXT, "Header"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_empty_header():
    lex = runner("=")

    assert lex.tokens == [
        Token(TokenType.TEXT, "="),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_multiple_header_markers():
    lex = runner("=== Header")

    assert lex.tokens == [
        Token(TokenType.HEADER, "==="),
        Token(TokenType.TEXT, "Header"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_header_marker_in_header_text():
    lex = runner("= a=b")

    assert lex.tokens == [
        Token(TokenType.HEADER, "="),
        Token(TokenType.TEXT, "a=b"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_header_markers_in_text():
    lex = runner("Definitely not a === header")

    assert lex.tokens == [
        Token(TokenType.TEXT, "Definitely not a === header"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


@patch("mau.lexers.document_lexer.DocumentLexer._run_directive")
def test_directive(mock_run_directive):
    runner("::#name:/path/to/file")

    mock_run_directive.assert_called_with("name", "/path/to/file")


@patch("builtins.open", new_callable=mock_open, read_data="just some data")
def test_import_directive(mock_file):  # pylint: disable=unused-argument
    lex = runner("::#include:/path/to/file")

    assert lex.tokens == [
        Token(TokenType.TEXT, "just some data"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_block():
    lex = runner(
        dedent(
            """
            ----
            Some comment

               another line
            ----
            """
        )
    )

    assert lex.tokens == [
        Token(TokenType.BLOCK, "----"),
        Token(TokenType.EOL),
        Token(TokenType.TEXT, "Some comment"),
        Token(TokenType.EOL),
        Token(TokenType.EOL),
        Token(TokenType.TEXT, "   another line"),
        Token(TokenType.EOL),
        Token(TokenType.BLOCK, "----"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_block_four_characters():
    lex = runner(
        dedent(
            """
            ####
            Some comment

               another line
            ####
            """
        )
    )

    assert lex.tokens == [
        Token(TokenType.BLOCK, "####"),
        Token(TokenType.EOL),
        Token(TokenType.TEXT, "Some comment"),
        Token(TokenType.EOL),
        Token(TokenType.EOL),
        Token(TokenType.TEXT, "   another line"),
        Token(TokenType.EOL),
        Token(TokenType.BLOCK, "####"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_block_with_comment():
    lex = runner(
        dedent(
            """
            ----
            // Comment
            ----
            """
        )
    )

    assert lex.tokens == [
        Token(TokenType.BLOCK, "----"),
        Token(TokenType.EOL),
        Token(TokenType.COMMENT, "// Comment"),
        Token(TokenType.EOL),
        Token(TokenType.BLOCK, "----"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_block_has_to_begin_with_four_identical_characters():
    lex = runner(
        dedent(
            """
            abcd
            """
        )
    )

    assert lex.tokens == [
        Token(TokenType.TEXT, "abcd"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_conditional():
    lex = runner("@if:somevar:=value")

    assert lex.tokens == [
        Token(TokenType.CONTROL, "@"),
        Token(TokenType.TEXT, "if"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.TEXT, "somevar:=value"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_conditional_with_space():
    lex = runner("@  if:somevar:=value")

    assert lex.tokens == [
        Token(TokenType.CONTROL, "@"),
        Token(TokenType.TEXT, "if"),
        Token(TokenType.LITERAL, ":"),
        Token(TokenType.TEXT, "somevar:=value"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]
