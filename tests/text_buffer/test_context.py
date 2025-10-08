from mau.test_helpers import dedent, generate_context, TEST_CONTEXT_SOURCE
from mau.text_buffer.context import Context


def test_context():
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


def test_context_merge():
    ctx1 = generate_context(1, 7, 5, 10)
    ctx2 = generate_context(100, 107, 105, 110)

    context = Context.merge_contexts(ctx1, ctx2)

    assert context == generate_context(1, 7, 105, 110)


def test_context_merge_overlapping():
    ctx1 = generate_context(1, 7, 5, 10)
    ctx2 = generate_context(4, 9, 105, 110)

    context = Context.merge_contexts(ctx1, ctx2)

    assert context == generate_context(1, 7, 105, 110)


def test_context_merge_included():
    ctx1 = generate_context(1, 2, 3, 4)
    ctx2 = generate_context(0, 0, 5, 6)

    context = Context.merge_contexts(ctx1, ctx2)

    assert context == ctx2


def test_context_clone():
    ctx1 = generate_context(1, 7, 5, 10)
    ctx2 = ctx1.clone()

    assert ctx1 == ctx2


def test_context_clones_are_independent():
    ctx1 = generate_context(1, 7, 5, 10)
    ctx2 = ctx1.clone()

    ctx2.start_line = 200

    assert ctx1.start_line == 1
