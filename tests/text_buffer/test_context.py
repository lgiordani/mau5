from mau.text_buffer.context import Context


def test_context():
    ctx = Context(start_line=1, start_column=7, source="main")

    assert ctx.asdict() == {
        "start_line": 1,
        "start_column": 7,
        "end_line": 0,
        "end_column": 0,
        "source": "main",
    }

    assert str(ctx) == "main:1,7-0,0"


def test_context_with_end():
    ctx = Context(
        start_line=1, start_column=7, end_line=5, end_column=10, source="main"
    )

    assert ctx.asdict() == {
        "start_line": 1,
        "start_column": 7,
        "end_line": 5,
        "end_column": 10,
        "source": "main",
    }

    assert str(ctx) == "main:1,7-5,10"
