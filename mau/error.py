from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from logging import Logger

from mau.text_buffer import adjust_context, adjust_position


class MauErrorType(Enum):
    LEXER = "lexer"
    PARSER = "parser"
    VISITOR = "visitor"


@dataclass
class MauError:
    type: MauErrorType
    content: dict


class MauException(ValueError):
    def __init__(self, message: str, error: MauError | None):
        self.message = message
        self.error = error


class BaseErrorFormatter(ABC):
    type = "base"

    @abstractmethod
    def process_lexer_exception(self, exc: MauException): ...

    @abstractmethod
    def process_parser_exception(self, exc: MauException): ...

    @abstractmethod
    def process_visitor_exception(self, exc: MauException): ...

    def process_mau_exception(self, exc: MauException):
        match exc.error.type:
            case MauErrorType.LEXER:
                return self.process_lexer_exception(exc)

            case MauErrorType.PARSER:
                return self.process_parser_exception(exc)

            case MauErrorType.VISITOR:
                return self.process_visitor_exception(exc)


class RawErrorFormatter(BaseErrorFormatter):
    type = "raw"

    def __init__(self):
        super().__init__()

    def process_lexer_exception(self, exc: MauException):
        message = exc.message
        error = exc.error

        position = error.content["position"]

        print(f"ERROR: {message}")
        if position:
            print(f"POSITION: {adjust_position(position)}")
        print()

    def process_parser_exception(self, exc: MauException):
        message = exc.message
        error = exc.error

        context = error.content["context"]

        print(f"ERROR: {message}")
        if context:
            print(f"CONTEXT: {adjust_context(context)}")
        print()

    def process_visitor_exception(self, exc: MauException):
        message = exc.message
        error = exc.error

        message = exc.message
        error = exc.error

        print("(Mau) # MAU ERROR")
        print(f"(Mau) Message: {message}")
        for k, v in error.content.items():
            print(f"(Mau) {k}: {v}")


class LogErrorFormatter(BaseErrorFormatter):
    type = "log"

    def __init__(self, logger: Logger):
        self.logger = logger

    def process_lexer_exception(self, exc: MauException):
        message = exc.message
        error = exc.error

        position = error.content["position"]

        self.logger.error(f"ERROR: {message}")
        if position:
            self.logger.error(f"POSITION: {adjust_position(position)}")

    def process_parser_exception(self, exc: MauException):
        message = exc.message
        error = exc.error

        context = error.content["context"]

        self.logger.error(f"ERROR: {message}")
        if context:
            self.logger.error(f"CONTEXT: {adjust_context(context)}")

    def process_visitor_exception(self, exc: MauException):
        message = exc.message
        error = exc.error

        self.logger.error("(Mau) # MAU ERROR")
        self.logger.error(f"(Mau) Message: {message}")
        for k, v in error.content.items():
            self.logger.error(f"(Mau) {k}: {v}")
