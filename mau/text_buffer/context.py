from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Context:
    # Context objects represent the place where a token was found
    # in the source code. They contain line and column where they
    # begin, the name of the source file (if provided), and the
    # text of the full line.

    start_line: int = 0
    start_column: int = 0
    end_line: int = 0
    end_column: int = 0
    source: str | None = None

    @classmethod
    def merge_contexts(cls, start_context: Context, end_context: Context) -> Context:
        context = start_context.clone()
        context.end_line = end_context.end_line
        context.end_column = end_context.end_column

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
