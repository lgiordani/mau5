from mau.text_buffer.text_buffer import Context


def test_context():
    ctx = Context(line=1, column=7, source="main")

    assert ctx.asdict() == {
        "line": 1,
        "column": 7,
        "end_line": None,
        "end_column": None,
        "source": "main",
    }

    assert str(ctx) == "main:1,7"


def test_context_with_end():
    ctx = Context(line=1, column=7, end_line=5, end_column=10, source="main")

    assert ctx.asdict() == {
        "line": 1,
        "column": 7,
        "end_line": 5,
        "end_column": 10,
        "source": "main",
    }

    assert str(ctx) == "main:1,7-5,10"
