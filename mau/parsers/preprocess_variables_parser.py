from mau.lexers.preprocess_variables_lexer import PreprocessVariablesLexer
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import BaseParser
from mau.tokens.token import Token, TokenType


# The PreprocessVariablesParser processes tokens,
# scans for variables in the form `{name}`,
# replaces them, and finally outputs a single
# node that contains the whole text.
class PreprocessVariablesParser(BaseParser):
    lexer_class = PreprocessVariablesLexer

    def _process_escaped_char(self):
        # Process escaped characters.
        # This checks if the escaped character
        # is the opening or closing curly brace, in
        # which case it stores it as it is
        # preventing the variable replacement
        # process to take place.

        # Check is the token is an escape backslash.
        self._get_token(TokenType.LITERAL, "\\")

        # Get the following character.
        char = self._get_token()

        # If the character is not a curly brace
        # restore the escape backslash.
        if char.value not in "{}":
            char.value = f"\\{char.value}"

        self._save(
            Node(
                content=TextNodeContent(char.value),
                info=NodeInfo(context=char.context),
            )
        )

        return True

    def _process_verbatim(self):
        # Process text surrounded by backticks.
        # Such text should be left untouched.
        # Verbatim is often used for code and
        # chances are that the syntax `{name}`
        # might be used as curly braces are
        # widespread in coding.

        # Check if the token is the opening backtick.
        opening_tick = self._get_token(TokenType.LITERAL, "`")

        # Get everything before the closing backtick.
        text = self._collect_join(
            [Token(TokenType.LITERAL, "`")],
            preserve_escaped_stop_tokens=True,
        )

        # Check if the token is the closing backtick.
        self._get_token(TokenType.LITERAL, "`")

        # Restore the original form of the text
        # with the surrounding backticks.
        text = f"`{text}`"

        self._save(
            Node(
                content=TextNodeContent(text),
                info=NodeInfo(context=opening_tick.context),
            )
        )

        return True

    def _process_curly(self):
        # This is the core of the replacement process.
        # If the function detects text between curly
        # braces it uses it as the name of a variable
        # and replaces it.

        # Check if the token is the opening curly brace.
        opening_bracket = self._get_token(TokenType.LITERAL, "{")

        # Get everything beforethe closing brace.
        variable_name = self._collect_join(stop_tokens=[Token(TokenType.LITERAL, "}")])

        # Check if the token is the closing curly brace.
        self._get_token(TokenType.LITERAL, "}")

        try:
            # Extract from the environment the variable
            # mentioned between curly braces.
            variable_value = self.environment.getvar_nodefault(variable_name)
        except KeyError as exp:
            raise self._error(
                f'Variable "{variable_name}" has not been defined.',
                context=opening_bracket.context,
            ) from exp

        # Boolean variables shouldn't be printed.
        # Replace them with an empty string.
        if variable_value in [True, False]:
            variable_value = ""

        self._save(
            Node(
                content=TextNodeContent(variable_value),
                info=NodeInfo(context=opening_bracket.context),
            )
        )

        return True

    def _process_pass(self):
        # None of the previous functions succeeded,
        # so we are in front of a pure text token.
        # Just store it and move on.
        text_token = self._get_token()

        self._save(
            Node(
                content=TextNodeContent(text_token.value),
                info=NodeInfo(context=text_token.context),
            )
        )

        return True

    def _process_functions(self):
        return [
            self._process_escaped_char,
            self._process_verbatim,
            self._process_curly,
            self._process_pass,
        ]

    def parse(self):
        super().parse()

        if not self.nodes:
            return

        # After having parsed the text and replaced the
        # variables, this should return a piece of text again.
        context = self.nodes[0].info.context
        text = "".join([str(i.content.value) for i in self.nodes])  # type: ignore[attr-defined]

        self.nodes = [
            Node(content=TextNodeContent(text), info=NodeInfo(context=context))
        ]
