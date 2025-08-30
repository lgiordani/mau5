import pytest

from mau.parsers.arguments_parser import set_names_and_defaults


def test_set_names_and_defaults_use_positional_names():
    args, kwargs = set_names_and_defaults(
        args=["value1", "value2"],
        kwargs={},
        positional_names=["attr1", "attr2"],
        default_values={"attr3": "value3"},
    )

    assert args == []
    assert kwargs == {"attr1": "value1", "attr2": "value2", "attr3": "value3"}


def test_set_names_and_defaults_named_wins_over_positional():
    args, kwargs = set_names_and_defaults(
        args=["value1", "value2"],
        kwargs={"attr1": "value4"},
        positional_names=["attr1", "attr2"],
        default_values={},
    )

    # Named and unnamed arguments clash.
    # Here, attr1 is given as a named argument,
    # which wins over the positional arguments. So,
    # the only remaining positional name is attr2
    # which receives the first positional value (value1),
    # leaving value2 as a flag.
    assert args == ["value2"]
    assert kwargs == {"attr1": "value4", "attr2": "value1"}


def test_set_names_and_defaults_positional_wins_over_default():
    args, kwargs = set_names_and_defaults(
        args=["value1", "value2"],
        kwargs={},
        positional_names=["attr1", "attr2"],
        default_values={"attr1": "value3"},
    )

    # Unnamed and default arguments clash.
    # Here, attr1 has a default, but the assignment
    # of an unnamed value wins over it.
    assert args == []
    assert kwargs == {"attr1": "value1", "attr2": "value2"}


def test_set_names_and_defaults_named_wins_over_default():
    args, kwargs = set_names_and_defaults(
        args=[],
        kwargs={"attr1": "value1"},
        positional_names=[],
        default_values={"attr1": "value2"},
    )

    # Named and default arguments clash.
    # Here, attr1 is given both as a named argument and
    # as a defaults value, but the named one wins.
    assert args == []
    assert kwargs == {"attr1": "value1"}


def test_set_names_and_defaults_not_enough_positional_values():
    # Here, we give two positional names,
    # but there is only one value, so the
    # second name cannot be assigned any value.
    with pytest.raises(ValueError):
        set_names_and_defaults(
            args=["value1"],
            kwargs={},
            positional_names=["attr1", "attr2"],
            default_values={},
        )
