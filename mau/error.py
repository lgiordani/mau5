from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from logging import Logger

from mau.environment.environment import Environment
from mau.text_buffer import Context, Position, adjust_context, adjust_position


class MauMessageType(Enum):
    ERROR_LEXER = "error-lexer"
    ERROR_PARSER = "error-parser"
    ERROR_VISITOR = "error-visitor"


@dataclass
class MauMessage:
    type: MauMessageType = field(init=False)
    text: str


@dataclass
class MauLexerErrorMessage(MauMessage):
    type: MauMessageType = field(init=False, default=MauMessageType.ERROR_LEXER)
    position: Position | None = None


@dataclass
class MauParserErrorMessage(MauMessage):
    type: MauMessageType = field(init=False, default=MauMessageType.ERROR_PARSER)
    context: Context | None = None


@dataclass
class MauVisitorErrorMessage(MauMessage):
    type: MauMessageType = field(init=False, default=MauMessageType.ERROR_VISITOR)
    context: Context | None
    node_type: str | None
    data: dict | None = None
    environment: Environment | None = None
    additional_info: dict[str, str] | None = None


class MauException(ValueError):
    def __init__(self, message: MauMessage):
        self.message = message


class BaseMessageHandler(ABC):
    type = "base"

    @abstractmethod
    def process_lexer_error(self, message: MauLexerErrorMessage): ...

    @abstractmethod
    def process_parser_error(self, message: MauParserErrorMessage): ...

    @abstractmethod
    def process_visitor_error(self, message: MauVisitorErrorMessage): ...

    def process(self, message: MauMessage):
        match message.type:
            case MauMessageType.ERROR_LEXER:
                return self.process_lexer_error(message)

            case MauMessageType.ERROR_PARSER:
                return self.process_parser_error(message)

            case MauMessageType.ERROR_VISITOR:
                return self.process_visitor_error(message)


class NullMessageHandler(BaseMessageHandler):
    type = "null"

    def process_lexer_error(self, message: MauLexerErrorMessage):
        pass

    def process_parser_error(self, message: MauParserErrorMessage):
        pass

    def process_visitor_error(self, message: MauVisitorErrorMessage):
        pass


# class RawErrorFormatter(BaseErrorFormatter):
#     type = "raw"

#     def __init__(self):
#         super().__init__()

#     def process_lexer_exception(self, exc: MauException):
#         message = exc.message
#         error = exc.error

#         position = error.content["position"]

#         print(f"ERROR: {message}")
#         if position:
#             print(f"POSITION: {adjust_position(position)}")
#         print()

#     def process_parser_exception(self, exc: MauException):
#         message = exc.message
#         error = exc.error

#         context = error.content["context"]

#         print(f"ERROR: {message}")
#         if context:
#             print(f"CONTEXT: {adjust_context(context)}")
#         print()

#     def process_visitor_exception(self, exc: MauException):
#         message = exc.message
#         error = exc.error

#         message = exc.message
#         error = exc.error

#         print("(Mau) # MAU ERROR")
#         print(f"(Mau) Message: {message}")
#         for k, v in error.content.items():
#             print(f"(Mau) {k}: {v}")


class LogMessageHandler(BaseMessageHandler):
    type = "log"

    def __init__(self, logger: Logger):
        self.logger = logger

    def process_lexer_error(self, message: MauLexerErrorMessage):
        self.logger.error(f"Lexer error: {message.text}")
        if message.position:
            self.logger.error(f"Position: {adjust_position(message.position)}")

    def process_parser_error(self, message: MauParserErrorMessage):
        self.logger.error(f"Parser error: {message.text}")
        if message.context:
            self.logger.error(f"Context: {adjust_context(message.context)}")

    def process_visitor_error(self, message: MauVisitorErrorMessage):
        self.logger.error("Visitor error")

        values = {}

        values["Message"] = message.text
        values["Context"] = message.context

        if message.node_type:
            values["Node type"] = message.node_type

        if message.data:
            values["Template data"] = message.data

        if message.additional_info:
            values.update(message.additional_info)

        for k, v in values.items():
            self.logger.error(f"{k}: {v}")
