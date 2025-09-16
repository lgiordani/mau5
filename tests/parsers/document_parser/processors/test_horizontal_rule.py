from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.document import HorizontalRuleNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.arguments_parser.parser import Arguments
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.horizontal_rule import (
    horizontal_rule_processor,
)
from mau.test_helpers import (
    compare_nodes,
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

    parser: DocumentParser = init_parser(source)
    horizontal_rule_processor(parser)

    compare_nodes(parser.nodes, expected_nodes)


def test_horizontal_rule_with_arguments():
    source = "---"

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
                context=generate_context(0, 0),
            ),
        )
    ]

    parser: DocumentParser = init_parser(source)
    parser.arguments_manager.push(
        Arguments(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
        )
    )

    horizontal_rule_processor(parser)

    compare_nodes(parser.nodes, expected_nodes)


def test_horizontal_rule_full_parse():
    source = "---"

    expected_nodes = [
        Node(
            content=HorizontalRuleNodeContent(),
            info=NodeInfo(context=generate_context(0, 0)),
        )
    ]

    parser = runner(source)

    compare_nodes(parser.nodes, expected_nodes)
