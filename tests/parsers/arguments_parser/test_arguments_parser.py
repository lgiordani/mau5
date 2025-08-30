import pytest

from mau.lexers.arguments_lexer import ArgumentsLexer
from mau.nodes.arguments import NamedArgumentNodeContent, UnnamedArgumentNodeContent
from mau.nodes.node import Node
from mau.parsers.arguments_parser import ArgumentsParser
from mau.parsers.base_parser import MauParserException
from mau.test_helpers import parser_runner_factory

runner = parser_runner_factory(ArgumentsLexer, ArgumentsParser)


def test_single_unnamed_argument_no_spaces():
    source = "value1"

    assert runner(source).nodes == [Node(content=UnnamedArgumentNodeContent("value1"))]


def test_single_unnamed_argument_with_spaces():
    source = "value with spaces"

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent("value with spaces"))
    ]


def test_multiple_unnamed_arguments_no_spaces():
    source = "value1,value2"

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent("value1")),
        Node(content=UnnamedArgumentNodeContent("value2")),
    ]


def test_multiple_unnamed_arguments_with_spaces():
    source = "value1 with spaces,value2 with more spaces"

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent("value1 with spaces")),
        Node(content=UnnamedArgumentNodeContent("value2 with more spaces")),
    ]


def test_multiple_unnamed_arguments_space_after_comma_is_removed():
    source = "value1 with spaces, value2 with more spaces"

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent("value1 with spaces")),
        Node(content=UnnamedArgumentNodeContent("value2 with more spaces")),
    ]


def test_multiple_unnamed_arguments_multiple_spaces_after_comma_is_removed():
    source = "value1 with spaces,    value2 with more spaces"

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent("value1 with spaces")),
        Node(content=UnnamedArgumentNodeContent("value2 with more spaces")),
    ]


def test_single_unnamed_argument_with_quotes_no_spaces():
    source = '"value1"'

    assert runner(source).nodes == [Node(content=UnnamedArgumentNodeContent("value1"))]


def test_single_unnamed_argument_with_quotes_with_spaces():
    source = '"value with spaces"'

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent("value with spaces"))
    ]


def test_single_unnamed_argument_comma_is_ignored_between_quotes():
    source = '"value1,value2"'

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent("value1,value2"))
    ]


def test_multiple_unnamed_arguments_with_quotes_no_spaces():
    source = '"value1","value2"'

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent("value1")),
        Node(content=UnnamedArgumentNodeContent("value2")),
    ]


def test_multiple_unnamed_arguments_with_quotes_with_spaces():
    source = '"value1 with spaces","value2 with more spaces"'

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent("value1 with spaces")),
        Node(content=UnnamedArgumentNodeContent("value2 with more spaces")),
    ]


def test_single_unnamed_argument_with_non_delimiting_quotes():
    source = r'value "with quotes"'

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent('value "with quotes"'))
    ]


def test_single_unnamed_argument_with_escaped_quotes():
    source = r'"value \"with escaped quotes\""'

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent('value "with escaped quotes"'))
    ]


def test_single_named_argument():
    source = "name=value1"

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name", "value1")),
    ]


def test_single_named_argument_with_spaces():
    source = "name=value with spaces"

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name", "value with spaces")),
    ]


def test_multiple_named_arguments():
    source = "name1=value1,name2=value2"

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name1", "value1")),
        Node(content=NamedArgumentNodeContent("name2", "value2")),
    ]


def test_multiple_named_arguments_with_spaces():
    source = "name1=value1 with spaces,name2=value2 with spaces"

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name1", "value1 with spaces")),
        Node(content=NamedArgumentNodeContent("name2", "value2 with spaces")),
    ]


def test_multiple_named_arguments_space_after_comma_is_removed():
    source = "name1=value1, name2=value2"

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name1", "value1")),
        Node(content=NamedArgumentNodeContent("name2", "value2")),
    ]


def test_multiple_named_arguments_multiple_spaces_after_comma_is_removed():
    source = "name1=value1,    name2=value2"

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name1", "value1")),
        Node(content=NamedArgumentNodeContent("name2", "value2")),
    ]


def test_single_named_argument_with_quotes_no_spaces():
    source = 'name="value1"'

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name", "value1"))
    ]


def test_single_named_argument_with_quotes_with_spaces():
    source = 'name="value with spaces"'

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name", "value with spaces"))
    ]


def test_single_named_argument_comma_is_ignored_between_quotes():
    source = 'name="value1,value2"'

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name", "value1,value2"))
    ]


def test_multiple_named_arguments_with_quotes_no_spaces():
    source = 'name1="value1",name2="value2"'

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name1", "value1")),
        Node(content=NamedArgumentNodeContent("name2", "value2")),
    ]


def test_multiple_named_arguments_with_quotes_with_spaces():
    source = 'name1="value1 with spaces",name2="value2 with more spaces"'

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name1", "value1 with spaces")),
        Node(content=NamedArgumentNodeContent("name2", "value2 with more spaces")),
    ]


def test_single_named_argument_with_non_delimiting_quotes():
    source = r'name=value "with quotes"'
    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name", 'value "with quotes"'))
    ]


def test_single_named_argument_with_escaped_quotes():
    source = r'name="value \"with escaped quotes\""'

    assert runner(source).nodes == [
        Node(content=NamedArgumentNodeContent("name", 'value "with escaped quotes"'))
    ]


def test_unnamed_and_named_arguments():
    source = "value1, name=value2"

    assert runner(source).nodes == [
        Node(content=UnnamedArgumentNodeContent("value1")),
        Node(content=NamedArgumentNodeContent("name", "value2")),
    ]


def test_named_arguments_followed_by_unnamed():
    source = "name=value2, value1"

    with pytest.raises(MauParserException):
        runner(source)


def test_process_arguments_unnamed_arguments():
    source = "value1, value2"
    parser = runner(source)

    args, kwargs, tags, subtype = parser.process_arguments()

    assert args == ["value1", "value2"]
    assert kwargs == {}
    assert tags == []
    assert subtype is None


def test_process_arguments_subtype():
    source = "value1, *value2"
    parser = runner(source)

    args, kwargs, tags, subtype = parser.process_arguments()

    assert args == ["value1"]
    assert kwargs == {}
    assert tags == []
    assert subtype == "value2"


def test_process_arguments_multiple_subtypes():
    source = "*value1, *value2"
    parser = runner(source)

    with pytest.raises(MauParserException):
        parser.process_arguments()
