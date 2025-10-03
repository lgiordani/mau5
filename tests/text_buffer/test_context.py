from mau.text_buffer.context import Context, reshape_context


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


def test_reshape_context():
    context_list = [Context(0, 0, 0, 4), Context(0, 4, 0, 8), Context(0, 8, 0, 13)]
    line_lengths = [6, 7]

    # The linear context shape is
    # 1111222233333

    # The lines are
    # 111111
    # 2222222

    # I expect the final context shape to be
    # 111122
    # 2233333

    reshape_context(context_list, line_lengths, initial_context=Context(0, 0, 0, 0))

    assert context_list == [
        Context(0, 0, 0, 4),
        Context(0, 4, 1, 2),
        Context(1, 2, 1, 7),
    ]


def test_reshape_context_exact_space():
    context_list = [Context(0, 0, 0, 4), Context(0, 4, 0, 8), Context(0, 8, 0, 12)]
    line_lengths = [4, 4, 4]

    # The linear context shape is
    # 111122223333

    # The lines are
    # 1111
    # 2222
    # 3333

    # I expect the final context shape to be
    # 1111
    # 2222
    # 3333

    reshape_context(context_list, line_lengths, initial_context=Context(0, 0, 0, 0))

    assert context_list == [
        Context(0, 0, 0, 4),
        Context(1, 0, 1, 4),
        Context(2, 0, 2, 4),
    ]


def test_reshape_context_initial_context():
    context_list = [Context(0, 0, 0, 4), Context(0, 4, 0, 8), Context(0, 8, 0, 13)]
    line_lengths = [6, 7]

    # The linear context shape is
    # 1111222233333

    # The lines are
    # 111111
    # 2222222

    # I expect the final context shape to be
    # 111122
    # 2233333

    reshape_context(context_list, line_lengths, initial_context=Context(3, 5, 7, 10))

    assert context_list == [
        Context(3, 0, 3, 4),
        Context(3, 4, 4, 2),
        Context(4, 2, 4, 7),
    ]
