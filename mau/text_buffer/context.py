from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Context:
    # Context objects represent the place where a token was found
    # in the source code. They contain start and enf line and
    # column of the text block, and the name of the source file
    # (if provided).

    start_line: int
    start_column: int
    end_line: int
    end_column: int
    source: str | None = None

    @classmethod
    def empty(cls) -> Context:
        return Context(0, 0, 0, 0)

    @classmethod
    def merge_contexts(cls, ctx1: Context, ctx2: Context) -> Context:
        """Merge two contexts.
        This function merges two contexts, returning
        a context that contains both.
        """
        context = Context(
            start_line=min(ctx1.start_line, ctx2.start_line),
            start_column=min(ctx1.start_column, ctx2.start_column),
            end_line=max(ctx1.end_line, ctx2.end_line),
            end_column=max(ctx1.end_column, ctx2.end_column),
            source=ctx1.source,
        )

        return context

    def asdict(self):
        return {
            "start_line": self.start_line,
            "start_column": self.start_column,
            "end_line": self.end_line,
            "end_column": self.end_column,
            "source": self.source,
        }

    def clone(self):
        return self.__class__(**self.asdict())

    def __repr__(self):
        source_prefix = ""
        if self.source:
            source_prefix = f"{self.source}:"

        return f"{source_prefix}{self.start_line},{self.start_column}-{self.end_line},{self.end_column}"

    def __str__(self):
        return repr(self)
