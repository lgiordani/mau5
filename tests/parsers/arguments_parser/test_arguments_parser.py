import pytest

from mau.lexers.arguments_lexer import ArgumentsLexer
from mau.nodes.node import Node, NodeInfo, ValueNodeContent
from mau.parsers.arguments_parser import Arguments, ArgumentsParser
from mau.parsers.base_parser import MauParserException
from mau.test_helpers import generate_context, parser_runner_factory

runner = parser_runner_factory(ArgumentsLexer, ArgumentsParser)


def test_single_unnamed_argument_no_spaces():
    source = "value1"

    expected_nodes = [
        Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_unnamed_argument_with_spaces():
    source = "value with spaces"

    expected_nodes = [
        Node(
            content=ValueNodeContent("value with spaces"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_unnamed_arguments_no_spaces():
    source = "value1,value2"

    expected_nodes = [
        Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        Node(
            content=ValueNodeContent("value2"),
            info=NodeInfo(context=generate_context(0, 7)),
        ),
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_unnamed_arguments_with_spaces():
    source = "value1 with spaces,value2 with more spaces"

    expected_nodes = [
        Node(
            content=ValueNodeContent("value1 with spaces"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        Node(
            content=ValueNodeContent("value2 with more spaces"),
            info=NodeInfo(context=generate_context(0, 19)),
        ),
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_unnamed_arguments_space_after_comma_is_removed():
    source = "value1 with spaces, value2 with more spaces"

    expected_nodes = [
        Node(
            content=ValueNodeContent("value1 with spaces"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        Node(
            content=ValueNodeContent("value2 with more spaces"),
            info=NodeInfo(context=generate_context(0, 20)),
        ),
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_unnamed_arguments_multiple_spaces_after_comma_is_removed():
    source = "value1 with spaces,    value2 with more spaces"

    expected_nodes = [
        Node(
            content=ValueNodeContent("value1 with spaces"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        Node(
            content=ValueNodeContent("value2 with more spaces"),
            info=NodeInfo(context=generate_context(0, 23)),
        ),
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_unnamed_argument_with_quotes_no_spaces():
    source = '"value1"'

    expected_nodes = [
        Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 1)),
        )
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_unnamed_argument_with_quotes_with_spaces():
    source = '"value with spaces"'

    expected_nodes = [
        Node(
            content=ValueNodeContent("value with spaces"),
            info=NodeInfo(context=generate_context(0, 1)),
        )
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_unnamed_argument_comma_is_ignored_between_quotes():
    source = '"value1,value2"'

    expected_nodes = [
        Node(
            content=ValueNodeContent("value1,value2"),
            info=NodeInfo(context=generate_context(0, 1)),
        )
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_unnamed_arguments_with_quotes_no_spaces():
    source = '"value1","value2"'

    expected_nodes = [
        Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 1)),
        ),
        Node(
            content=ValueNodeContent("value2"),
            info=NodeInfo(context=generate_context(0, 10)),
        ),
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_unnamed_arguments_with_quotes_with_spaces():
    source = '"value1 with spaces","value2 with more spaces"'

    expected_nodes = [
        Node(
            content=ValueNodeContent("value1 with spaces"),
            info=NodeInfo(context=generate_context(0, 1)),
        ),
        Node(
            content=ValueNodeContent("value2 with more spaces"),
            info=NodeInfo(context=generate_context(0, 22)),
        ),
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_unnamed_argument_with_non_delimiting_quotes():
    source = r'value "with quotes"'

    expected_nodes = [
        Node(
            content=ValueNodeContent(
                'value "with quotes"',
            ),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_unnamed_argument_with_escaped_quotes():
    source = r'"value \"with escaped quotes\""'

    expected_nodes = [
        Node(
            content=ValueNodeContent(
                'value "with escaped quotes"',
            ),
            info=NodeInfo(context=generate_context(0, 1)),
        )
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_named_argument():
    source = "name=value1"

    expected_nodes = {
        "name": Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_named_argument_with_spaces():
    source = "name=value with spaces"

    expected_nodes = {
        "name": Node(
            content=ValueNodeContent("value with spaces"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_named_arguments():
    source = "name1=value1,name2=value2"

    expected_nodes = {
        "name1": Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        "name2": Node(
            content=ValueNodeContent("value2"),
            info=NodeInfo(context=generate_context(0, 13)),
        ),
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_named_arguments_with_spaces():
    source = "name1=value1 with spaces,name2=value2 with spaces"

    expected_nodes = {
        "name1": Node(
            content=ValueNodeContent("value1 with spaces"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        "name2": Node(
            content=ValueNodeContent("value2 with spaces"),
            info=NodeInfo(context=generate_context(0, 25)),
        ),
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_named_arguments_space_after_comma_is_removed():
    source = "name1=value1, name2=value2"

    expected_nodes = {
        "name1": Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        "name2": Node(
            content=ValueNodeContent("value2"),
            info=NodeInfo(context=generate_context(0, 14)),
        ),
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_named_arguments_multiple_spaces_after_comma_is_removed():
    source = "name1=value1,    name2=value2"

    expected_nodes = {
        "name1": Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        "name2": Node(
            content=ValueNodeContent("value2"),
            info=NodeInfo(context=generate_context(0, 17)),
        ),
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_named_argument_with_quotes_no_spaces():
    source = 'name="value1"'

    expected_nodes = {
        "name": Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_named_argument_with_quotes_with_spaces():
    source = 'name="value with spaces"'

    expected_nodes = {
        "name": Node(
            content=ValueNodeContent("value with spaces"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_named_argument_comma_is_ignored_between_quotes():
    source = 'name="value1,value2"'

    expected_nodes = {
        "name": Node(
            content=ValueNodeContent("value1,value2"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_named_arguments_with_quotes_no_spaces():
    source = 'name1="value1",name2="value2"'

    expected_nodes = {
        "name1": Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        "name2": Node(
            content=ValueNodeContent("value2"),
            info=NodeInfo(context=generate_context(0, 15)),
        ),
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_multiple_named_arguments_with_quotes_with_spaces():
    source = 'name1="value1 with spaces",name2="value2 with more spaces"'

    expected_nodes = {
        "name1": Node(
            content=ValueNodeContent("value1 with spaces"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        "name2": Node(
            content=ValueNodeContent("value2 with more spaces"),
            info=NodeInfo(context=generate_context(0, 27)),
        ),
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_named_argument_with_non_delimiting_quotes():
    source = r'name=value "with quotes"'
    expected_nodes = {
        "name": Node(
            content=ValueNodeContent('value "with quotes"'),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_single_named_argument_with_escaped_quotes():
    source = r'name="value \"with escaped quotes\""'

    expected_nodes = {
        "name": Node(
            content=ValueNodeContent('value "with escaped quotes"'),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == []
    assert parser.named_argument_nodes == expected_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_unnamed_and_named_arguments():
    source = "value1, name=value2"

    expected_unnamed_nodes = [
        Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    expected_named_nodes = {
        "name": Node(
            content=ValueNodeContent("value2"),
            info=NodeInfo(context=generate_context(0, 8)),
        ),
    }

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_unnamed_nodes
    assert parser.named_argument_nodes == expected_named_nodes
    assert parser.tag_nodes == []
    assert parser.subtype is None


def test_named_arguments_followed_by_unnamed():
    source = "name=value2, value1"

    with pytest.raises(MauParserException):
        runner(source)


def test_process_arguments_subtype():
    source = "value1, *value2"

    expected_unnamed_nodes = [
        Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    ]

    expected_subtype = Node(
        content=ValueNodeContent("value2"),
        info=NodeInfo(context=generate_context(0, 8)),
    )

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_unnamed_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == []
    assert parser.subtype == expected_subtype


def test_process_arguments_tags():
    source = "value1, #tag1, value2, #tag2"

    expected_unnamed_nodes = [
        Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        Node(
            content=ValueNodeContent("value2"),
            info=NodeInfo(context=generate_context(0, 15)),
        ),
    ]
    expected_tag_nodes = [
        Node(
            content=ValueNodeContent("tag1"),
            info=NodeInfo(context=generate_context(0, 8)),
        ),
        Node(
            content=ValueNodeContent("tag2"),
            info=NodeInfo(context=generate_context(0, 23)),
        ),
    ]

    parser = runner(source)

    assert parser.unnamed_argument_nodes == expected_unnamed_nodes
    assert parser.named_argument_nodes == {}
    assert parser.tag_nodes == expected_tag_nodes
    assert parser.subtype is None


def test_process_arguments_multiple_subtypes():
    source = "*value1, *value2"

    with pytest.raises(MauParserException):
        runner(source)


def test_set_names_use_positional_names():
    source = "value1, value2"

    expected_unnamed_nodes = []

    expected_named_nodes = {
        "attr1": Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        "attr2": Node(
            content=ValueNodeContent("value2"),
            info=NodeInfo(context=generate_context(0, 8)),
        ),
    }

    parser = runner(source)
    parser.set_names(["attr1", "attr2"])

    assert parser.unnamed_argument_nodes == expected_unnamed_nodes
    assert parser.named_argument_nodes == expected_named_nodes


def test_set_names_named_wins_over_positional():
    # Named and unnamed arguments clash.
    # Here, attr1 is given as a named argument,
    # which wins over the positional arguments. So,
    # the only remaining positional name is attr2
    # which receives the first positional value (value1),
    # leaving value2 as a flag.

    source = "value1, value2, value3, attr1=value4"

    expected_unnamed_nodes = [
        Node(
            content=ValueNodeContent("value3"),
            info=NodeInfo(context=generate_context(0, 16)),
        ),
    ]

    expected_named_nodes = {
        "attr1": Node(
            content=ValueNodeContent("value4"),
            info=NodeInfo(context=generate_context(0, 24)),
        ),
        "attr2": Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
        "attr3": Node(
            content=ValueNodeContent("value2"),
            info=NodeInfo(context=generate_context(0, 8)),
        ),
    }

    parser = runner(source)
    parser.set_names(["attr1", "attr2", "attr3"])

    assert parser.unnamed_argument_nodes == expected_unnamed_nodes
    assert parser.named_argument_nodes == expected_named_nodes


def test_set_names_not_enough_positional_values():
    # Here, we give two positional names,
    # but there is only one value, so the
    # second name cannot be assigned.

    source = "value1"

    expected_unnamed_nodes = []

    expected_named_nodes = {
        "attr1": Node(
            content=ValueNodeContent("value1"),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    }

    parser = runner(source)
    parser.set_names(["attr1", "attr2"])

    assert parser.unnamed_argument_nodes == expected_unnamed_nodes
    assert parser.named_argument_nodes == expected_named_nodes


def test_arguments():
    source = "value1, #tag1, *subtype1, name=value2"

    parser = runner(source)

    assert parser.arguments == Arguments(
        ["value1"], {"name": "value2"}, ["tag1"], "subtype1"
    )


def test_arguments_empty():
    source = ""

    parser = runner(source)

    assert parser.arguments == Arguments([], {}, [], None)
