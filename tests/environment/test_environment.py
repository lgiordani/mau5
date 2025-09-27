import pytest

from mau.environment.environment import Environment


def test_init():
    environment = Environment()

    assert environment.asdict() == {}


def test_init_with_flat_content():
    environment = Environment.from_dict({"var1": "value1", "var2": "value2"})

    assert environment.asdict() == {"var1": "value1", "var2": "value2"}


def test_init_with_flat_content_and_namespace():
    environment = Environment.from_dict(
        {"var1": "value1", "var2": "value2"}, namespace="parent"
    )

    assert environment.asdict() == {"parent": {"var1": "value1", "var2": "value2"}}


def test_init_with_nested_content():
    environment = Environment.from_dict({"var1": {"var2": "value2"}})

    assert environment.asdict() == {"var1": {"var2": "value2"}}


def test_init_with_flat_hierarchical_content():
    environment = Environment.from_dict({"var1.var3": "value3", "var2": "value2"})

    assert environment.asdict() == {"var1": {"var3": "value3"}, "var2": "value2"}


def test_update():
    environment = Environment()

    environment.update({"var1": "value1", "var2": "value2"})

    assert environment.asdict() == {"var1": "value1", "var2": "value2"}


def test_update_does_not_replace():
    environment = Environment.from_dict({"var1": "value1", "var2": "value2"})

    environment.update({"var3": "value3"})

    assert environment.asdict() == {
        "var1": "value1",
        "var2": "value2",
        "var3": "value3",
    }


def test_update_with_namespace():
    environment = Environment()

    environment.update({"var1": "value1", "var2": "value2"}, namespace="test")

    assert environment.asdict() == {"test": {"var1": "value1", "var2": "value2"}}


def test_update_with_namespace_does_not_replace():
    environment = Environment.from_dict({"test": {"var1": "value1", "var2": "value2"}})

    environment.update({"var3": "value3"}, namespace="test")

    assert environment.asdict() == {
        "test": {"var1": "value1", "var2": "value2", "var3": "value3"}
    }


def test_update_deep():
    environment = Environment.from_dict({"mau": {"visitor": {"class": "someclass"}}})

    environment.update(
        {"visitor": {"custom_templates": {"template1": "value1"}}}, "mau"
    )

    assert environment.asdict() == {
        "mau": {
            "visitor": {
                "class": "someclass",
                "custom_templates": {"template1": "value1"},
            },
        },
    }


def test_set_variable_flat():
    environment = Environment()

    environment.setvar("var1", "value1")

    assert environment.asdict() == {"var1": "value1"}


def test_set_variable_hierarchical():
    environment = Environment()

    environment.setvar("var1.var2", "value2")

    assert environment.asdict() == {"var1": {"var2": "value2"}}


def test_set_variable_nested():
    environment = Environment()

    environment.setvar("var1", {"var2": "value2"})

    assert environment.asdict() == {"var1": {"var2": "value2"}}


def test_set_variable_empty_dict():
    environment = Environment()

    environment.setvar("var1.var2", {})

    assert environment.asdict() == {"var1": {"var2": {}}}


def test_get_variable_flat():
    environment = Environment.from_dict({"var1": "value1"})

    assert environment.getvar("var1") == "value1"


def test_get_variable_nested():
    environment = Environment.from_dict({"var1": {"var2": "value2"}})

    assert environment.getvar("var1.var2") == "value2"


def test_get_variable_nested_empty():
    environment = Environment.from_dict({"var1": {"var2": {}}})

    assert environment.getvar("var1.var2") == {}


def test_get_variable_flat_default():
    environment = Environment.from_dict({"var1": "value1"})

    assert environment.getvar("var2", "def") == "def"


def test_get_variable_nested_default():
    environment = Environment.from_dict({"var1": {"var2": "value2"}})

    assert environment.getvar("var1.var3", "def") == "def"


def test_get_variable_flat_no_default():
    environment = Environment()

    with pytest.raises(KeyError):
        environment.getvar_nodefault("var1")


def test_get_variable_nested_no_default():
    environment = Environment()

    with pytest.raises(KeyError):
        environment.getvar_nodefault("var1.var2")


def test_get_variable_is_a_namespace():
    environment = Environment.from_dict(
        {
            "top": {
                "middle": {
                    "var1": "value1",
                    "var2": "value2",
                    "var3": {},
                }
            },
        }
    )

    assert environment.getvar("top").asdict() == {
        "middle": {
            "var1": "value1",
            "var2": "value2",
            "var3": {},
        }
    }

    assert environment.getvar("top.middle").asdict() == {
        "var1": "value1",
        "var2": "value2",
        "var3": {},
    }

    assert environment.getvar("notthere") is None

    assert environment.getvar("top.mid") is None
