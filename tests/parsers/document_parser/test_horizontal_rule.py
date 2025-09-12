from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.document import HorizontalRuleNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_horizontal_rule():
    source = "---"

    expected_nodes = [
        Node(
            content=HorizontalRuleNodeContent(),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source)

    assert parser.nodes == expected_nodes


def test_horizontal_rule_with_arguments():
    source = """
    [*break, arg1, key1=value1]
    ---
    """

    expected_nodes = [
        Node(
            content=HorizontalRuleNodeContent(),
            info=NodeInfo(
                unnamed_args=["arg1"],
                named_args={
                    "key1": "value1",
                },
                tags=[],
                subtype="break",
                context=generate_context(2, 0),
            ),
        )
    ]

    parser = runner(source)

    assert parser.nodes == expected_nodes
