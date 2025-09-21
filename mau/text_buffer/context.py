from dataclasses import dataclass


@dataclass
class Context:
    # Context objects represent the place where a token was found
    # in the source code. They contain line and column where they
    # begin, the name of the source file (if provided), and the
    # text of the full line.

    line: int = 0
    column: int = 0
    source: str | None = None

    def asdict(self):
        return {
            "line": self.line,
            "column": self.column,
            "source": self.source,
        }

    def clone(self):
        return self.__class__(**self.asdict())

    def __repr__(self):
        return str(self.asdict())
