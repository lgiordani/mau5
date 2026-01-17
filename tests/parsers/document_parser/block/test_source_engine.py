from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockNode
from mau.nodes.node import NodeInfo
from mau.nodes.source import (
    SourceLineNode,
    SourceMarkerNode,
    SourceNode,
)
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_asdict_list,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_source_engine_empty_block():
    source = """
    [engine=source]
    ----
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                info=NodeInfo(context=generate_context(2, 0, 3, 4)),
            ),
        ],
    )


def test_source_engine_empty_block_language():
    source = """
    [python, engine=source]
    ----
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                info=NodeInfo(
                    context=generate_context(2, 0, 3, 4), unnamed_args=["python"]
                ),
            ),
        ],
    )


def test_source_engine_contains_mau_code():
    source = """
    [engine=source]
    ----
    // A comment
    @@@@
    A block
    @@@@
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="// A comment",
                                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                            ),
                            SourceLineNode(
                                line_number="2",
                                line_content="@@@@",
                                info=NodeInfo(context=generate_context(4, 0, 4, 4)),
                            ),
                            SourceLineNode(
                                line_number="3",
                                line_content="A block",
                                info=NodeInfo(context=generate_context(5, 0, 5, 7)),
                            ),
                            SourceLineNode(
                                line_number="4",
                                line_content="@@@@",
                                info=NodeInfo(context=generate_context(6, 0, 6, 4)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 6, 4)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 7, 4)),
            ),
        ],
    )


def test_source_engine_removes_escape_from_directive_like_text():
    source = r"""
    [engine=source]
    ----
    \::#looks like a directive
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="::#looks like a directive",
                                info=NodeInfo(context=generate_context(3, 0, 3, 26)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 26)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 4, 4)),
            ),
        ],
    )


def test_source_engine_with_code():
    source = """
    [python, engine=source]
    ----
    import os

    print(os.environ["HOME"])
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "python",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="import os",
                                info=NodeInfo(context=generate_context(3, 0, 3, 9)),
                            ),
                            SourceLineNode(
                                line_number="2",
                                line_content="",
                                info=NodeInfo(context=generate_context(4, 0, 4, 0)),
                            ),
                            SourceLineNode(
                                line_number="3",
                                line_content='print(os.environ["HOME"])',
                                info=NodeInfo(context=generate_context(5, 0, 5, 25)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 5, 25)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 6, 4)),
            ),
        ],
    )


def test_source_engine_ignores_mau_syntax():
    source = """
    [engine=source]
    ----
    :answer:42
    The answer is {answer}
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content=":answer:42",
                                info=NodeInfo(context=generate_context(3, 0, 3, 10)),
                            ),
                            SourceLineNode(
                                line_number="2",
                                line_content="The answer is {answer}",
                                info=NodeInfo(context=generate_context(4, 0, 4, 22)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 4, 22)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 5, 4)),
            ),
        ],
    )


def test_source_engine_respects_spaces_and_indentation():
    source = """
    [engine=source]
    ----
      //    This is a comment
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="  //    This is a comment",
                                info=NodeInfo(context=generate_context(3, 0, 3, 25)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 25)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 4, 4)),
            ),
        ],
    )


def test_source_engine_callouts_default_delimiter():
    source = """
    [engine=source]
    ----
    import sys
    import os:mark1:
    import enum:mark2:
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="import sys",
                                info=NodeInfo(context=generate_context(3, 0, 3, 10)),
                            ),
                            SourceLineNode(
                                line_number="2",
                                line_content="import os",
                                marker=SourceMarkerNode(
                                    "mark1",
                                    info=NodeInfo(
                                        context=generate_context(4, 9, 4, 16)
                                    ),
                                ),
                                info=NodeInfo(context=generate_context(4, 0, 4, 9)),
                            ),
                            SourceLineNode(
                                line_number="3",
                                line_content="import enum",
                                marker=SourceMarkerNode(
                                    "mark2",
                                    info=NodeInfo(
                                        context=generate_context(5, 11, 5, 18)
                                    ),
                                ),
                                info=NodeInfo(context=generate_context(5, 0, 5, 11)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 5, 18)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 6, 4)),
            ),
        ],
    )


def test_source_engine_callouts_potential_clash():
    source = """
    [engine=source]
    ----
    import: os:mark1:
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="import: os",
                                marker=SourceMarkerNode(
                                    "mark1",
                                    info=NodeInfo(
                                        context=generate_context(3, 10, 3, 17)
                                    ),
                                ),
                                info=NodeInfo(context=generate_context(3, 0, 3, 10)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 17)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 4, 4)),
            ),
        ],
    )


def test_source_engine_callouts_one_single_marker_is_skipped():
    source = """
    [engine=source]
    ----
    import:
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="import:",
                                info=NodeInfo(context=generate_context(3, 0, 3, 7)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 7)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 4, 4)),
            ),
        ],
    )


def test_source_engine_marker_custom_delimiter():
    source = """
    [engine=source, marker_delimiter="|"]
    ----
    import sys
    import os:mark1:
    import enum|mark2|
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="import sys",
                                info=NodeInfo(context=generate_context(3, 0, 3, 10)),
                            ),
                            SourceLineNode(
                                line_number="2",
                                line_content="import os:mark1:",
                                info=NodeInfo(context=generate_context(4, 0, 4, 16)),
                            ),
                            SourceLineNode(
                                line_number="3",
                                line_content="import enum",
                                marker=SourceMarkerNode(
                                    "mark2",
                                    info=NodeInfo(
                                        context=generate_context(5, 11, 5, 18)
                                    ),
                                ),
                                info=NodeInfo(context=generate_context(5, 0, 5, 11)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 5, 18)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 6, 4)),
            ),
        ],
    )


def test_source_engine_highlight_marker_with_default_style():
    source = """
    [engine=source]
    ----
    import sys
    import os:@:
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="import sys",
                                info=NodeInfo(context=generate_context(3, 0, 3, 10)),
                            ),
                            SourceLineNode(
                                line_number="2",
                                line_content="import os",
                                highlight_style="default",
                                info=NodeInfo(context=generate_context(4, 0, 4, 12)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 4, 12)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 5, 4)),
            ),
        ],
    )


def test_source_engine_highlight_custom_marker():
    source = """
    [engine=source, highlight_marker="#"]
    ----
    import sys
    import os:#:
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="import sys",
                                info=NodeInfo(context=generate_context(3, 0, 3, 10)),
                            ),
                            SourceLineNode(
                                line_number="2",
                                line_content="import os",
                                highlight_style="default",
                                info=NodeInfo(context=generate_context(4, 0, 4, 12)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 4, 12)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 5, 4)),
            ),
        ],
    )


def test_source_engine_highlight_marker_change_default_highlight_style():
    source = """
    [engine=source, highlight_default_style="another"]
    ----
    import sys
    import os:@:
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="import sys",
                                info=NodeInfo(context=generate_context(3, 0, 3, 10)),
                            ),
                            SourceLineNode(
                                line_number="2",
                                line_content="import os",
                                highlight_style="another",
                                info=NodeInfo(context=generate_context(4, 0, 4, 12)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 4, 12)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 5, 4)),
            ),
        ],
    )


def test_source_engine_highlight_marker_custom_highlight_style():
    source = """
    [engine=source]
    ----
    import sys
    import os:@green:
    import enum:@+:
    ----
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="source",
                content=[
                    SourceNode(
                        "text",
                        content=[
                            SourceLineNode(
                                line_number="1",
                                line_content="import sys",
                                info=NodeInfo(context=generate_context(3, 0, 3, 10)),
                            ),
                            SourceLineNode(
                                line_number="2",
                                line_content="import os",
                                highlight_style="green",
                                info=NodeInfo(context=generate_context(4, 0, 4, 17)),
                            ),
                            SourceLineNode(
                                line_number="3",
                                line_content="import enum",
                                highlight_style="+",
                                info=NodeInfo(context=generate_context(5, 0, 5, 15)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 5, 15)),
                    )
                ],
                info=NodeInfo(context=generate_context(2, 0, 6, 4)),
            ),
        ],
    )
