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


def reshape_context(
    context_list: list[Context], line_lengths: list[int], initial_context: Context
):
    context_index = 0

    current_line = 0
    current_column = 0

    space_left = line_lengths[current_line]

    while context_index < len(context_list):
        # The context we are currently processing.
        current_context = context_list[context_index]

        # The space used by this context.
        current_context_size = current_context.end_column - current_context.start_column

        # There is no space for the beginning of the context.
        if space_left == 0:
            # Update the current line and column.
            current_line += 1
            current_column = 0

            # Update the space left in the current line.
            space_left = line_lengths[current_line]

            # Move on.
            continue

        # There is space for the beginning.

        # The current context can start at the
        # present coordinates, update it.
        current_context.start_line = initial_context.start_line + current_line
        current_context.start_column = current_column

        # There is space for the end of the context.
        if current_context_size <= space_left:
            # Update the end context.
            current_context.end_line = initial_context.start_line + current_line
            current_context.end_column = current_column + current_context_size

            # Update the current column and the space left.
            current_column = current_context.end_column
            space_left -= current_context_size

            # Move to the next context.
            context_index += 1

            # Move on.
            continue

        # There is no space for the end of the context.

        # Block the former space left.
        previous_space_left = space_left

        # Update the current line and column.
        current_line += 1
        current_column = 0

        # Update the space left in the current line.
        space_left = line_lengths[current_line]

        # The end of the current context is on
        # this line, update it.
        current_context.end_line = initial_context.start_line + current_line
        current_context.end_column = current_context_size - previous_space_left

        current_column += current_context.end_column

        # Move to the next context.
        context_index += 1

        # Move on.
        continue
