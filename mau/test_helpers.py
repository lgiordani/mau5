import textwrap
from collections.abc import MutableSequence

from mau.environment.environment import Environment
from mau.nodes.node import (
    Node,
    NodeContentMixin,
    NodeInfo,
    NodeLabelsMixin,
)
from mau.text_buffer import Context, TextBuffer
from mau.visitors.base_visitor import BaseVisitor

TEST_CONTEXT_SOURCE = "test.py"


def dedent(text):
    return textwrap.dedent(text).strip()


def generate_context(line: int, column: int, end_line: int, end_column: int):
    return Context(line, column, end_line, end_column, TEST_CONTEXT_SOURCE)


def compare_asdict_object(obj_left, obj_right):
    assert obj_left.asdict() == obj_right.asdict()


def compare_asdict_list(objs_left: MutableSequence, objs_right: MutableSequence):
    assert [i.asdict() for i in objs_left] == [i.asdict() for i in objs_right]


def check_visit_node(node, expected):
    bv = BaseVisitor()

    result = bv.visit(node)

    assert result == expected


def check_node_with_content(node):
    node.content = [Node(), Node()]

    bv = BaseVisitor()

    result = bv.visit(node)

    assert result["content"] == [
        {
            "_type": "none",
            "_info": {
                "context": {
                    "end_column": 0,
                    "end_line": 0,
                    "source": None,
                    "start_column": 0,
                    "start_line": 0,
                },
                "named_args": {},
                "subtype": None,
                "tags": [],
                "unnamed_args": [],
            },
        },
        {
            "_type": "none",
            "_info": {
                "context": {
                    "end_column": 0,
                    "end_line": 0,
                    "source": None,
                    "start_column": 0,
                    "start_line": 0,
                },
                "named_args": {},
                "subtype": None,
                "tags": [],
                "unnamed_args": [],
            },
        },
    ]


def check_node_with_labels(node):
    node.labels = {"label1": [Node(), Node()], "label2": [Node()]}

    bv = BaseVisitor()

    result = bv.visit(node)

    assert result["labels"] == {
        "label1": [
            {
                "_type": "none",
                "_info": {
                    "context": {
                        "end_column": 0,
                        "end_line": 0,
                        "source": None,
                        "start_column": 0,
                        "start_line": 0,
                    },
                    "named_args": {},
                    "subtype": None,
                    "tags": [],
                    "unnamed_args": [],
                },
            },
            {
                "_type": "none",
                "_info": {
                    "context": {
                        "end_column": 0,
                        "end_line": 0,
                        "source": None,
                        "start_column": 0,
                        "start_line": 0,
                    },
                    "named_args": {},
                    "subtype": None,
                    "tags": [],
                    "unnamed_args": [],
                },
            },
        ],
        "label2": [
            {
                "_type": "none",
                "_info": {
                    "context": {
                        "end_column": 0,
                        "end_line": 0,
                        "source": None,
                        "start_column": 0,
                        "start_line": 0,
                    },
                    "named_args": {},
                    "subtype": None,
                    "tags": [],
                    "unnamed_args": [],
                },
            },
        ],
    }


# def compare_text_lines(left: str, right: str):
#     assert left.split("\n") == right.split("\n")


def init_lexer_factory(lexer_class):
    """
    A factory that returns a lexer initialiser.
    The returned function initialises the lexer
    and returns it.
    """

    def _init_lexer(text_buffer: TextBuffer, environment: Environment | None = None):
        return lexer_class(text_buffer, environment)

    return _init_lexer


def lexer_runner_factory(lexer_class, *args, **kwds):
    """
    A factory that returns a lexer runner.
    The returned function initialises and
    runs the lexer on the given source.
    """

    init_lexer = init_lexer_factory(lexer_class)

    def _run(text, environment: Environment | None = None, **kwargs):
        kwds.update(kwargs)

        environment = environment or Environment()

        text_buffer = TextBuffer(
            textwrap.dedent(text),
            source_filename=TEST_CONTEXT_SOURCE,
        )

        lexer = init_lexer(text_buffer, environment, *args, **kwds)
        lexer.process()

        return lexer

    return _run


def init_tokens_manager_factory(lexer_class, tokens_manager_class):
    def _init_tokens_manager(text: str, environment):
        text_buffer = TextBuffer(text, source_filename=TEST_CONTEXT_SOURCE)

        lex = lexer_class(text_buffer, environment)
        lex.process()

        tm = tokens_manager_class(lex.tokens)

        return tm

    return _init_tokens_manager


def init_parser_factory(lexer_class, parser_class):
    """
    A factory that returns a parser initialiser.
    The returned function initialises and runs the lexer,
    initialises the parser and returns it.
    """

    def _init_parser(source: str, environment=None, *args, **kwargs):
        text_buffer = TextBuffer(
            textwrap.dedent(source),
            source_filename=TEST_CONTEXT_SOURCE,
        )

        lex = lexer_class(text_buffer, environment)
        lex.process()

        par = parser_class(lex.tokens, environment, *args, **kwargs)

        return par

    return _init_parser


def parser_runner_factory(lexer_class, parser_class, *args, **kwds):
    """
    A factory that returns a parser runner.
    The returned function runs the parser on the given source.
    """

    init_parser = init_parser_factory(lexer_class, parser_class)

    def _run(source, environment=None, **kwargs):
        kwds.update(kwargs)

        environment = environment or Environment()

        parser = init_parser(source, environment, *args, **kwds)
        parser.parse()
        parser.finalise()

        return parser

    return _run


class ATestNode(Node, NodeLabelsMixin, NodeContentMixin):
    type = "test"

    def __init__(
        self,
        value: str,
        content: list[Node] | None = None,
        labels: dict[str, list[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        self.value = value

        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "value": self.value,
        }

        NodeLabelsMixin.content_asdict(self, base)
        NodeContentMixin.content_asdict(self, base)

        return base
