import pytest

from mau.visitors.jinja_visitor import Template
from mau.nodes.node import Node


def test_specificity():
    template_a = Template(type="atype", content="content_a", name="name_a")

    template_b = Template(
        type="atype",
        content="content_b",
        name="name_b",
        subtype="asubtype",
        prefix="aprefix",
        ptype="aptype",
        tags=["tag1", "tag2"],
    )

    assert template_a.specificity == (0, 0, 0, 0)
    assert template_b.specificity == (1, 1, 1, 2)


def test_from_name_type_only():
    template = Template.from_name("atype", content="somecontent")

    assert template.specificity == (0, 0, 0, 0)


def test_from_name_empty_string():
    with pytest.raises(ValueError):
        Template.from_name("", content="somecontent")


def test_from_name_type_and_subtype():
    template = Template.from_name("atype.asubtype", content="somecontent")

    assert template.specificity == (1, 0, 0, 0)


def test_from_name_type_and_prefix():
    template = Template.from_name("atype.pf_aprefix", content="somecontent")

    assert template.specificity == (0, 1, 0, 0)


def test_from_name_type_and_ptype():
    template = Template.from_name("atype.pt_aptype", content="somecontent")

    assert template.specificity == (0, 0, 1, 0)


def test_from_name_type_and_tags():
    template = Template.from_name("atype.tg_atag1.tg_atag2", content="somecontent")

    assert template.specificity == (0, 0, 0, 2)


def test_from_name_type_and_multiple_out_of_order():
    template = Template.from_name(
        "atype.tg_atag1.pt_aptype.asubtype.pf_aprefix.tg_atag2",
        content="somecontent",
    )

    assert template.specificity == (1, 1, 1, 2)


def test_match_type():
    template = Template(type="type_a", name="name_a", content="content_a")

    node_a = Node()
    node_a.type = "type_a"

    node_b = Node()
    node_b.type = "type_b"

    assert template.match(node_a)
    assert not template.match(node_b)


def test_match_prefix():
    template = Template(
        type="type_a", name="name_a", content="content_a", prefix="prefix_a"
    )

    node_a = Node()
    node_a.type = "type_a"

    assert template.match(node_a, prefix="prefix_a")

    assert not template.match(node_a, prefix="prefix_b")


def test_match_subtype():
    template = Template(
        type="type_a", name="name_a", content="content_a", subtype="subtype_a"
    )

    node_a = Node()
    node_a.type = "type_a"
    node_a.arguments.subtype = "subtype_a"

    node_b = Node()
    node_b.type = "type_a"
    node_b.arguments.subtype = "subtype_b"

    assert template.match(node_a)
    assert not template.match(node_b)


def test_match_ptype():
    template = Template(
        type="type_a", name="name_a", content="content_a", ptype="ptype_a"
    )

    parent_a = Node()
    parent_a.type = "ptype_a"

    parent_b = Node()
    parent_b.type = "ptype_b"

    node_a = Node()
    node_a.type = "type_a"
    node_a.parent = parent_a

    node_b = Node()
    node_b.type = "type_a"
    node_b.parent = parent_b

    assert template.match(node_a)
    assert not template.match(node_b)


def test_match_ptype_no_parent():
    template = Template(
        type="type_a", name="name_a", content="content_a", ptype="ptype_a"
    )

    node_a = Node()
    node_a.type = "type_a"

    assert not template.match(node_a)


def test_match_tags():
    template = Template(
        type="type_a", name="name_a", content="content_a", tags=["tag_a1", "tag_a2"]
    )

    node_a = Node()
    node_a.type = "type_a"
    node_a.arguments.tags = ["tag_a1"]

    node_b = Node()
    node_b.type = "type_a"
    node_b.arguments.tags = ["tag_a1", "tag_a2", "tag_a3"]

    node_c = Node()
    node_c.type = "type_a"
    node_c.arguments.tags = ["tag_c1"]

    assert template.match(node_b)
    assert not template.match(node_a)
    assert not template.match(node_c)
