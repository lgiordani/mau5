import logging

from mau.helpers import rematch
from mau.lexers.base_lexer import BaseLexer
from mau.text_buffer.context import Context
from mau.tokens.token import TokenType

logger = logging.getLogger(__name__)


class DocumentLexer(BaseLexer):
    def _process_functions(self):
        return [
            self._process_multiline_comment,
            self._process_comment,
            self._process_horizontal_rule,
            self._process_block,
            self._process_command_or_directive,
            self._process_control,
            self._process_include,
            self._process_variable,
            self._process_arguments,
            self._process_title,
            self._process_list,
            self._process_header,
            # This is provided by BaseLexer
            self._process_text_line,
        ]

    def _process_multiline_comment(self):
        # Detect the beginning of a multiline comment
        # represented by four slashes ////.

        if self._current_line != "////":
            return None

        tokens = [
            self._create_token_and_skip(
                TokenType.MULTILINE_COMMENT, self._current_line
            ),
            self._create_token_and_skip(TokenType.EOL),
        ]

        self._nextline()

        logger.debug("Found MULTILINE_COMMENT at %s", self._context)
        logger.debug(tokens)

        return tokens

    def _process_comment(self):
        # Detect a single line comment that
        # starts with two slashes //.

        match = rematch(r"^//.*", self._current_line)

        if not match:
            return None

        tokens = [
            self._create_token_and_skip(TokenType.COMMENT, self._current_line),
            self._create_token_and_skip(TokenType.EOL),
        ]

        self._nextline()

        logger.debug("Found COMMENT at %s", self._context)
        logger.debug(tokens)

        return tokens

    def _process_horizontal_rule(self):
        # Detect a horizontal rule represented by
        # three dashes ---.

        match = rematch(r"---$", self._current_line)

        if match is None:
            return None

        tokens = [
            self._create_token_and_skip(TokenType.HORIZONTAL_RULE, self._current_line)
        ]

        logger.debug("Found HORIZONTAL_RULE at %s", self._context)
        logger.debug(tokens)

        return tokens

    def _process_block(self):
        # Detect the beginning of a block represented
        # by four identical characters, e.g. @@@@

        if len(self._current_line) != 4:
            return None

        # Try to match the block delimiter
        match = rematch(r"^(.)\1{3}$", self._current_line)

        if match is None:
            return None

        tokens = [
            self._create_token_and_skip(TokenType.BLOCK, self._current_line),
            self._create_token_and_skip(TokenType.EOL),
        ]

        self._nextline()

        logger.debug("Found BLOCK at %s", self._context)
        logger.debug(tokens)

        return tokens

    def _run_directive(self, name, value):
        # This executes a lexer directive found in the source text.
        # Currently, Mau supports only one directive,
        # `#include` that includes another source file.

        if name == "include":
            with open(value, encoding="utf-8") as included_file:
                # Read the content of the included file.
                text = included_file.read()

                # Create a text buffer with the correct
                # context. Tokens created by this lexer
                # come from another file.
                text_buffer = self.text_buffer.__class__(text, Context(source=value))

                lexer = DocumentLexer(text_buffer, self.environment)
                lexer.process()

                # Remove the last token as it is an EOF
                self.tokens.extend(lexer.tokens[:-1])

    def _process_command_or_directive(self):
        # Detect a command or directive in the form
        # ::COMMAND:[ARGUMENTS]
        # or
        # :: COMMAND:[ARGUMENTS]

        match = rematch(
            r"^(?P<prefix>::) *(?P<command>[a-z0-9_#]+)(?P<separator>:)(?P<arguments>.*)?",
            self._current_line,
        )

        if not match:
            return None

        prefix = match.groupdict().get("prefix")
        command = match.groupdict().get("command")
        separator = match.groupdict().get("separator")
        arguments = match.groupdict().get("arguments")

        if command.startswith("#"):
            # Lexer directives are disguised as commands, but
            # the name of the command starts with #.
            # In this case we need to execute the directive
            # instead of creating tokens.

            # This is a lexer directive, remove the prefix and
            # execute it.
            self._run_directive(command[1:], arguments)

            self._nextline()

            return []

        # If the command is not a lexer directive we can
        # process it as usual, generating tokens.

        tokens = [
            self._create_token_and_skip(TokenType.COMMAND, prefix),
            self._create_token_and_skip(TokenType.TEXT, command),
            self._create_token_and_skip(TokenType.LITERAL, separator),
        ]

        # A command might or might not have arguments.
        if arguments:
            tokens.append(self._create_token_and_skip(TokenType.TEXT, arguments))

        tokens.append(self._create_token_and_skip(TokenType.EOL))

        self._nextline()

        logger.debug("Found COMMAND at %s", self._context)
        logger.debug(tokens)

        return tokens

    def _process_control(self):
        # Detect control logic in the form
        # @OPERATOR:LOGIC
        # or
        # @ OPERATOR:LOGIC
        #
        # Controls implement advanced logic and the
        # custom syntax depends on the specific control.

        match = rematch(
            r"^(?P<prefix>@) *(?P<operator>[^:]+)(?P<separator>:)(?P<logic>.*)",
            self._current_line,
        )

        if not match:
            return None

        prefix = match.groupdict().get("prefix")
        operator = match.groupdict().get("operator")
        separator = match.groupdict().get("separator")
        logic = match.groupdict().get("logic")

        tokens = [
            self._create_token_and_skip(TokenType.CONTROL, prefix),
            self._create_token_and_skip(TokenType.TEXT, operator),
            self._create_token_and_skip(TokenType.LITERAL, separator),
            self._create_token_and_skip(TokenType.TEXT, logic),
            self._create_token_and_skip(TokenType.EOL),
        ]

        self._nextline()

        logger.debug("Found CONTROL at %s", self._context)
        logger.debug(tokens)

        return tokens

    def _process_include(self):
        # Detect included content in the form
        # <<TYPE:[ARGUMENTS]
        # or
        # << TYPE:[ARGUMENTS]
        #
        # The content TYPE can contain lowercase
        # letters, numbers, and the characters
        # _ # \ .

        match = rematch(
            r"^(?P<prefix><<) *(?P<type>[a-z0-9_#\\\.]+)(?P<separator>:)(?P<arguments>.*)?",
            self._current_line,
        )

        if not match:
            return None

        prefix = match.groupdict().get("prefix")
        content_type = match.groupdict().get("type")
        separator = match.groupdict().get("separator")
        arguments = match.groupdict().get("arguments")

        if not content_type:  # pragma: no cover
            return None

        tokens = []

        tokens = [
            self._create_token_and_skip(TokenType.CONTENT, prefix),
            self._create_token_and_skip(TokenType.TEXT, content_type),
            self._create_token_and_skip(TokenType.LITERAL, separator),
        ]

        if arguments:
            tokens.append(self._create_token_and_skip(TokenType.TEXT, arguments))

        tokens.append(self._create_token_and_skip(TokenType.EOL))

        self._nextline()

        logger.debug("Found INCLUDE at %s", self._context)
        logger.debug(tokens)

        return tokens

    def _process_variable(self):
        # Detect a variable definition in the form
        # :NAME:[VALUE]
        #
        # The variable NAME can contain alphanumeric
        # characters and the characters
        # _ . + -

        match = rematch(
            r"^(?P<prefix>:)(?P<name>[a-zA-Z0-9_\.\+\-]+)(?P<separator>:)(?P<value>.*)?",
            self._current_line,
        )

        if not match:  # pragma: no cover
            return None

        prefix = match.groupdict().get("prefix")
        name = match.groupdict().get("name")
        separator = match.groupdict().get("separator")
        value = match.groupdict().get("value")

        tokens = [
            self._create_token_and_skip(TokenType.VARIABLE, prefix),
            self._create_token_and_skip(TokenType.TEXT, name),
            self._create_token_and_skip(TokenType.LITERAL, separator),
        ]

        if value:
            tokens.append(self._create_token_and_skip(TokenType.TEXT, value))

        tokens.append(self._create_token_and_skip(TokenType.EOL))

        self._nextline()

        logger.debug("Found VARIABLE at %s", self._context)
        logger.debug(tokens)

        return tokens

    def _process_arguments(self):
        # Detect arguments in the form
        # [ARGUMENTS]

        match = rematch(
            r"^(?P<prefix>\[)(?P<arguments>.*)(?P<suffix>\])",
            self._current_line,
        )

        if not match:  # pragma: no cover
            return None

        prefix = match.groupdict().get("prefix")
        arguments = match.groupdict().get("arguments")
        suffix = match.groupdict().get("suffix")

        tokens = [
            self._create_token_and_skip(TokenType.ARGUMENTS, prefix),
            self._create_token_and_skip(TokenType.TEXT, arguments),
            self._create_token_and_skip(TokenType.LITERAL, suffix),
            self._create_token_and_skip(TokenType.EOL),
        ]

        self._nextline()

        logger.debug("Found ARGUMENTS at %s", self._context)
        logger.debug(tokens)

        return tokens

    def _process_title(self):
        # Detect a title in the form
        # .TITLE
        # or
        # . TITLE

        match = rematch(
            r"^(?P<prefix>\.) *(?P<title>.*)",
            self._current_line,
        )

        if not match:
            return None

        prefix = match.groupdict().get("prefix")
        title = match.groupdict().get("title")

        tokens = [
            self._create_token_and_skip(TokenType.TITLE, prefix),
            self._create_token_and_skip(TokenType.TEXT, title),
            self._create_token_and_skip(TokenType.EOL),
        ]

        self._nextline()

        logger.debug("Found TITLE at %s", self._context)
        logger.debug(tokens)

        return tokens

    def _process_list(self):
        # Detect a list item in the form
        # * ITEM
        # or
        # # ITEM
        #
        # Multiple prefix symbols can be specified.
        # Withespace at the beginning of the line is ignored,
        # as Mau considers only the number of prefix symbols
        # to decide the nesting level.
        # Space between the prefix symbol and text is ignored as well.

        match = rematch(r"^ *(?P<prefix>[\*#]+) +(?P<item>.*)", self._current_line)

        if not match:
            return None

        prefix = match.groupdict().get("prefix")
        item = match.groupdict().get("item")

        tokens = [
            self._create_token_and_skip(TokenType.LIST, prefix),
            self._create_token_and_skip(TokenType.TEXT, item),
            self._create_token_and_skip(TokenType.EOL),
        ]

        self._nextline()

        logger.debug("Found LIST at %s", self._context)
        logger.debug(tokens)

        return tokens

    def _process_header(self):
        # Detect a header in the form
        # =HEADER
        # or
        # = HEADER
        #
        # Multiple prefix symbols can be specified.

        match = rematch("^(?P<prefix>=+) *(?P<header>.*)", self._current_line)

        if not match:
            return None

        prefix = match.groupdict().get("prefix")
        header = match.groupdict().get("header")

        if not header:
            return None

        tokens = [
            self._create_token_and_skip(TokenType.HEADER, prefix),
            self._create_token_and_skip(TokenType.TEXT, header),
            self._create_token_and_skip(TokenType.EOL),
        ]

        self._nextline()

        logger.debug("Found HEADER at %s", self._context)
        logger.debug(tokens)

        return tokens
