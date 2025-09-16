import pytest

from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.block import BlockNodeContent
from mau.nodes.inline import SentenceNodeContent, TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_parse_block_title_and_arguments():
    source = """
    .Just a title
    [arg1, *subtype1, #tag1, key1=value1]
    ----
    ----
    """

    parser: DocumentParser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine=None,
                    preprocessor=None,
                ),
                info=NodeInfo(
                    context=generate_context(3, 0),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "content": [],
                    "title": [
                        Node(
                            content=SentenceNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Just a title"),
                                        info=NodeInfo(context=generate_context(1, 0)),
                                    )
                                ]
                            },
                        )
                    ],
                },
            ),
        ],
    )


def test_block_classes_single_class():
    source = """
    [*subtype1,classes=cls1]
    ----
    ----
    """

    parser: DocumentParser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=["cls1"],
                    engine=None,
                    preprocessor=None,
                ),
                info=NodeInfo(
                    context=generate_context(2, 0),
                    subtype="subtype1",
                ),
                children={
                    "content": [],
                },
            )
        ],
    )


def test_block_classes_multiple_classes():
    source = """
    [*subtype1,classes="cls1,cls2"]
    ----
    ----
    """

    parser: DocumentParser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=["cls1", "cls2"],
                    engine=None,
                    preprocessor=None,
                ),
                info=NodeInfo(
                    context=generate_context(2, 0),
                    subtype="subtype1",
                ),
                children={
                    "content": [],
                },
            )
        ],
    )


def test_block_engine():
    source = """
    [*subtype,engine=someengine]
    ----
    ----
    """

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(2, 0)


# def test_command_defblock():
#     source = """
#     ::defblock:alias, *myblock, language=python, engine=source
#     """

#     par = runner(source)

#     assert par.block_aliases["alias"] == {
#         "subtype": "myblock",
#         "mandatory_args": [],
#         "defaults": {"language": "python", "engine": "source"},
#     }


# def test_define_block_in_environment():
#     source = """
#     """

#     environment = Environment()
#     environment.setvar(
#         "mau.parser.block_definitions",
#         {
#             "alias": {
#                 "subtype": "type",
#                 "mandatory_args": ["arg1", "arg2"],
#                 "defaults": {"key1": "value1"},
#             },
#         },
#     )

#     par = runner(source, environment=environment)

#     assert par.block_aliases["alias"] == {
#         "subtype": "type",
#         "mandatory_args": ["arg1", "arg2"],
#         "defaults": {"key1": "value1"},
#     }


# def test_command_defblock_no_subtype():
#     source = """
#     ::defblock:alias, language=python, engine=source
#     """

#     par = runner(source)

#     assert par.block_aliases["alias"] == {
#         "subtype": None,
#         "mandatory_args": [],
#         "defaults": {"language": "python", "engine": "source"},
#     }


# def test_command_defblock_source():
#     source = """
#     """

#     par = runner(source)

#     assert par.block_aliases["source"] == {
#         "subtype": None,
#         "mandatory_args": ["language"],
#         "defaults": {"language": "text", "engine": "source"},
#     }


# def test_command_defblock_source_can_be_overridden():
#     source = """
#     ::defblock:source, *source, language=python, engine=source
#     """

#     par = runner(source)

#     assert par.block_aliases["source"] == {
#         "subtype": "source",
#         "mandatory_args": [],
#         "defaults": {"language": "python", "engine": "source"},
#     }


# def test_command_defblock_no_args():
#     source = """
#     ::defblock:
#     """

#     with pytest.raises(MauErrorException):
#         runner(source)


# def test_block_definitions_are_used():
#     source = """
#     ::defblock:alias, *subtype, name1=value1, name2=value2

#     [*alias]
#     ----
#     ----
#     """

#     assert runner(source).nodes == [
#         BlockNode(
#             subtype="subtype",
#             children=[],
#             secondary_children=[],
#             classes=[],
#             title=None,
#             engine=None,
#             preprocessor="none",
#             args=[],
#             kwargs={"name1": "value1", "name2": "value2"},
#         ),
#     ]


# def test_block_definitions_local_kwargs_overwrite_defined_ones():
#     source = """
#     ::defblock:alias, *subtype, name1=value1, name2=value2

#     [*alias, name1=value99]
#     ----
#     ----
#     """

#     assert runner(source).nodes == [
#         BlockNode(
#             subtype="subtype",
#             children=[],
#             secondary_children=[],
#             classes=[],
#             title=None,
#             engine=None,
#             preprocessor="none",
#             args=[],
#             kwargs={"name1": "value99", "name2": "value2"},
#         ),
#     ]


# def test_block_definitions_local_args_are_used():
#     # This is testing that local args are used even when
#     # an alias is used. However, the test should fail as
#     # blocks cannot have unnamed arguments.

#     source = """
#     ::defblock:alias, *subtype, name1=value1, name2=value2

#     [*alias, attr1, name1=value99]
#     ----
#     ----
#     """

#     assert runner(source).nodes == [
#         BlockNode(
#             subtype="subtype",
#             children=[],
#             secondary_children=[],
#             classes=[],
#             title=None,
#             engine=None,
#             preprocessor="none",
#             args=["attr1"],
#             kwargs={"name1": "value99", "name2": "value2"},
#         ),
#     ]


# def test_block_definitions_unnamed_args_are_used_as_names():
#     # This is testing that the unnamed args specified
#     # in the block definition are used as names for the
#     # unnamed arguments passed to the block.

#     source = """
#     ::defblock:alias, *subtype, attr1, attr2

#     [*alias, value1, value2]
#     ----
#     ----
#     """

#     assert runner(source).nodes == [
#         BlockNode(
#             subtype="subtype",
#             children=[],
#             secondary_children=[],
#             classes=[],
#             title=None,
#             engine=None,
#             preprocessor="none",
#             args=[],
#             kwargs={"attr1": "value1", "attr2": "value2"},
#         ),
#     ]


# def test_block_definitions_unnamed_and_named_args():
#     # This is testing that any named are specifid in
#     # the block definition is included in the block
#     # kwargs if not redefined.

#     source = """
#     ::defblock:alias, *subtype, attr1, attr2, attr3=value3

#     [*alias, value1, value2]
#     ----
#     ----
#     """

#     assert runner(source).nodes == [
#         BlockNode(
#             subtype="subtype",
#             children=[],
#             secondary_children=[],
#             classes=[],
#             title=None,
#             engine=None,
#             preprocessor="none",
#             args=[],
#             kwargs={"attr1": "value1", "attr2": "value2", "attr3": "value3"},
#         ),
#     ]


# def test_block_definitions_no_values_for_unnamed_args():
#     # This is testing that is there are unnamed args in
#     # the block definiton they should be given values
#     # when the block is created.

#     source = """
#     ::defblock:alias, *subtype, attr1, attr2, attr3=value3

#     [*alias]
#     ----
#     ----
#     """

#     with pytest.raises(ValueError):
#         runner(source)


# def test_block_definitions_values_without_unnamed_args():
#     # This is testing that values passed to the
#     # block at creation time should match the parameters
#     # specified in the block definition.

#     source = """
#     ::defblock:alias, *subtype, attr3=value3

#     [*alias, value1, value2]
#     ----
#     ----
#     """

#     assert runner(source).nodes == [
#         BlockNode(
#             subtype="subtype",
#             children=[],
#             secondary_children=[],
#             classes=[],
#             title=None,
#             engine=None,
#             preprocessor="none",
#             args=["value1", "value2"],
#             kwargs={"attr3": "value3"},
#         ),
#     ]


# def test_block_definitions_named_override_unnamed():
#     # This is testing that values passed to the
#     # block at creation time should match the parameters
#     # specified in the block definition.

#     source = """
#     ::defblock:alias, *subtype, arg1, key1=value1

#     [*alias, value2, arg1=value1]
#     ----
#     ----
#     """

#     assert runner(source).nodes == [
#         BlockNode(
#             subtype="subtype",
#             children=[],
#             secondary_children=[],
#             classes=[],
#             title=None,
#             engine=None,
#             preprocessor="none",
#             args=["value2"],
#             kwargs={"arg1": "value1", "key1": "value1"},
#         ),
#     ]
