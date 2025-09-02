import pytest

from mau.environment.environment import Environment
from mau.lexers.preprocess_variables_lexer import PreprocessVariablesLexer
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.parsers.preprocess_variables_parser import PreprocessVariablesParser
from mau.test_helpers import (
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(PreprocessVariablesLexer, PreprocessVariablesParser)
runner = parser_runner_factory(PreprocessVariablesLexer, PreprocessVariablesParser)


def test_plain_text_with_no_variables():
    source = "This is text"

    expected_nodes = [
        Node(
            content=TextNodeContent("This is text"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source)

    assert parser.nodes == expected_nodes


def test_plain_text_with_variables():
    environment = Environment.from_dict({"attr": "5"})
    source = "This is text"

    expected_nodes = [
        Node(
            content=TextNodeContent("This is text"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_replace_variable():
    environment = Environment.from_dict({"attr": "5"})
    source = "This is number {attr}"

    expected_nodes = [
        Node(
            content=TextNodeContent("This is number 5"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_manage_unclosed_curly_braces():
    environment = Environment.from_dict({"attr": "5"})
    source = "This is {attr"

    expected_nodes = [
        Node(
            content=TextNodeContent("This is {attr"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_replace_variable_with_namespace():
    environment = Environment.from_dict({"app": {"attr": "5"}})
    source = "This is number {app.attr}"

    expected_nodes = [
        Node(
            content=TextNodeContent("This is number 5"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_replace_boolean():
    environment = Environment.from_dict({"flag": True})
    source = "This flag is {flag}"

    expected_nodes = [
        Node(
            content=TextNodeContent("This flag is "),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_escape_curly_braces():
    environment = Environment.from_dict({"attr": "5"})
    source = r"This is \{attr\}"

    expected_nodes = [
        Node(
            content=TextNodeContent("This is {attr}"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_curly_braces_in_verbatim():
    environment = Environment.from_dict({"attr": "5"})
    source = "This is `{attr}`"

    expected_nodes = [
        Node(
            content=TextNodeContent("This is `{attr}`"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_open_verbatim():
    environment = Environment.from_dict({"attr": "5"})
    source = "This is `{attr}"

    expected_nodes = [
        Node(
            content=TextNodeContent("This is `5"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_escape_curly_braces_in_verbatim():
    environment = Environment.from_dict({"attr": "5"})
    source = r"This is `\{attr\}`"

    expected_nodes = [
        Node(
            content=TextNodeContent(r"This is `\{attr\}`"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_escape_other_chars():
    environment = Environment.from_dict({"attr": "5"})
    source = r"This \_is\_ \text"

    expected_nodes = [
        Node(
            content=TextNodeContent(r"This \_is\_ \text"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_curly_braces_in_escaped_verbatim():
    environment = Environment.from_dict({"attr": "5"})
    source = r"This is \`{attr}\`"

    expected_nodes = [
        Node(
            content=TextNodeContent(r"This is \`5\`"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_variable_not_existing():
    environment = Environment()
    source = "This is number {attr}"

    with pytest.raises(MauParserException) as exc:
        runner(source, environment)

    assert exc.value.context == generate_context(0, 15)


def test_variables_can_contain_markers():
    environment = Environment.from_dict(
        {"bold": "*bold*", "dictdef": "`adict = {'a':5}`"}
    )
    source = "A very {bold} text. Some code: {dictdef}"

    expected_nodes = [
        Node(
            content=TextNodeContent("A very *bold* text. Some code: `adict = {'a':5}`"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source, environment)

    assert parser.nodes == expected_nodes


def test_escape_backtick():
    source = r"This is `\``"

    expected_nodes = [
        Node(
            content=TextNodeContent(r"This is `\``"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source)

    assert parser.nodes == expected_nodes
