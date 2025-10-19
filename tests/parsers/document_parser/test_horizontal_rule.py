from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.document import HorizontalRuleNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_horizontal_rule():
    source = """
    ---
    """

    expected_nodes = [
        Node(
            content=HorizontalRuleNodeContent(),
            info=NodeInfo(context=generate_context(1, 0, 1, 3)),
        )
    ]

    parser = runner(source)

    compare_nodes(parser.nodes, expected_nodes)


def test_horizontal_rule_with_arguments():
    source = """
    [arg1,#tag1,*subtype1,key1=value1]
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
                tags=["tag1"],
                subtype="subtype1",
                context=generate_context(2, 0, 2, 3),
            ),
        )
    ]

    parser = runner(source)

    compare_nodes(parser.nodes, expected_nodes)
