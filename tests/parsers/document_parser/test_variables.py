from mau.lexers.document_lexer import DocumentLexer
from mau.parsers.document_parser import DocumentParser
from mau.nodes.node import Node, NodeInfo
from mau.nodes.inline import TextNodeContent, StyleNodeContent
from mau.nodes.paragraph import ParagraphNodeContent
from mau.test_helpers import (
    init_parser_factory,
    parser_runner_factory,
    generate_context,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_parse_variable_definition_without_value_is_empty():
    source = ":attr:"

    parser = runner(source)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr": ""}


def test_parse_variable_definition_with_plus_is_true():
    source = ":+attr:"

    parser = runner(source)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr": True}


def test_parse_variable_definition_with_minus_is_false():
    source = ":-attr:"

    parser = runner(source)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr": False}


def test_parse_variable_definition_flag_plus_ignores_value():
    source = ":+attr:42"

    parser = runner(source)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr": True}


def test_parse_variable_definition_flag_minus_ignores_value():
    source = ":-attr:42"

    parser = runner(source)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr": False}


def test_parse_variable_definition_with_value_is_loaded():
    source = ":attr:42"

    parser = runner(source)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"attr": "42"}


def test_parse_variable_definition_value_can_be_any_text():
    source = ":attr:[footnote](http://some.domain/path)"

    parser = runner(source)

    assert parser.nodes == []
    assert parser.environment.asdict() == {
        "attr": "[footnote](http://some.domain/path)",
    }


def test_parse_variable_definition_with_namespace():
    source = ":meta.attr:42"

    parser = runner(source)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"meta": {"attr": "42"}}


def test_parse_variable_definition_with_multiple_dots():
    source = ":meta.category.attr:42"

    parser = runner(source)

    assert parser.nodes == []
    assert parser.environment.asdict() == {"meta": {"category": {"attr": "42"}}}


def test_variable_replacement():
    source = """
    :answer:42

    The answer is {answer}
    """

    parser = runner(source)

    assert parser.nodes == [
        Node(
            children={
                "content": [
                    Node(
                        content=TextNodeContent("The answer is 42"),
                        info=NodeInfo(context=generate_context(3, 0)),
                    )
                ]
            },
            content=ParagraphNodeContent(),
            info=NodeInfo(context=generate_context(3, 0)),
        )
    ]


def test_variable_replacement_with_namespace():
    source = """
    :mau.answer:42

    The answer is {mau.answer}
    """

    parser = runner(source)

    assert parser.nodes == [
        Node(
            children={
                "content": [
                    Node(
                        content=TextNodeContent("The answer is 42"),
                        info=NodeInfo(context=generate_context(3, 0)),
                    )
                ]
            },
            content=ParagraphNodeContent(),
            info=NodeInfo(context=generate_context(3, 0)),
        )
    ]


def test_variable_definition_escape():
    source = r"""
    \:answer:42
    """

    parser = runner(source)

    assert parser.nodes == [
        Node(
            children={
                "content": [
                    Node(
                        content=TextNodeContent(":answer:42"),
                        info=NodeInfo(context=generate_context(1, 0)),
                    )
                ]
            },
            content=ParagraphNodeContent(),
            info=NodeInfo(context=generate_context(1, 0)),
        )
    ]


def test_skip_variable_replacement():
    source = r"""
    :answer:42

    The answer is \{answer\}
    """

    parser = runner(source)

    assert parser.nodes == [
        Node(
            children={
                "content": [
                    Node(
                        content=TextNodeContent("The answer is {answer}"),
                        info=NodeInfo(context=generate_context(3, 0)),
                    )
                ]
            },
            content=ParagraphNodeContent(),
            info=NodeInfo(context=generate_context(3, 0)),
        )
    ]


def test_variables_are_preprocessed():
    source = r"""
    :important:*IMPORTANT*

    This is {important}
    """

    parser = runner(source)

    assert parser.nodes == [
        Node(
            children={
                "content": [
                    Node(
                        content=TextNodeContent("This is "),
                        info=NodeInfo(context=generate_context(3, 0)),
                    ),
                    Node(
                        content=StyleNodeContent("star"),
                        info=NodeInfo(context=generate_context(3, 8)),
                        children={
                            "content": [
                                Node(
                                    content=TextNodeContent("IMPORTANT"),
                                    info=NodeInfo(context=generate_context(3, 9)),
                                ),
                            ]
                        },
                    ),
                ]
            },
            content=ParagraphNodeContent(),
            info=NodeInfo(context=generate_context(3, 0)),
        )
    ]


def test_variable_replacement_in_variable():
    source = """
    :answer:42
    :sentence:The answer is {answer}

    {sentence}
    """

    parser = runner(source)

    assert parser.nodes == [
        Node(
            children={
                "content": [
                    Node(
                        content=TextNodeContent("The answer is 42"),
                        info=NodeInfo(context=generate_context(4, 0)),
                    )
                ]
            },
            content=ParagraphNodeContent(),
            info=NodeInfo(context=generate_context(4, 0)),
        )
    ]
