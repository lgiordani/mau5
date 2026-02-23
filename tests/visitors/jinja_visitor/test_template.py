import pytest

from mau.visitors.jinja_visitor import Template


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
