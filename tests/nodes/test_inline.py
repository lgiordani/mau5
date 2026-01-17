# from mau.nodes.inline import (
#     RawNode,
#     StyleNode,
#     TextNode,
#     VerbatimNode,
#     WordNode,
# )
# from mau.test_helpers import check_node_with_content
# from mau.text_buffer import Context


# def test_word_node():
#     node = WordNode("somevalue")

#     assert node.type == "word"
#     assert node.value == "somevalue"


# def test_text_node():
#     node = TextNode("somevalue")

#     assert node.type == "text"
#     assert node.value == "somevalue"


# def test_raw_node():
#     node = RawNode("somevalue")

#     assert node.type == "raw"
#     assert node.value == "somevalue"


# def test_verbatim_node():
#     node = VerbatimNode("somevalue")

#     assert node.type == "verbatim"
#     assert node.value == "somevalue"


# def test_style_node_without_content():
#     node = StyleNode("mystyle")

#     assert node.type == "style"
#     assert node.style == "mystyle"


# def test_style_node_with_content():
#     node = StyleNode("mystyle")
#     check_node_with_content(node)
