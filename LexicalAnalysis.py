from typing import Optional, Union

from InputStream import InputStream
from Tokens import *


class Tokenizer:
    """
    Tokenizer provádí transformaci vstupního zdrojového souboru na proud tokenů, ze kterých je v
    další fázi kompilace stavěn syntaktický strom.
    """

    """Pomocná konstanta s klíčovými slovy a jim odpovídajícími druhy tokenů."""
    __keywords = {
        "if": IfKeywordToken,
        "then": ThenKeywordToken,
        "else": ElseKeywordToken,
        "print": PrintKeywordToken,
        "read": ReadKeywordToken,
        "true": BoolConstantToken.true,
        "false": BoolConstantToken.false
    }

    """Pomocná konstanta obsahující dostupné operátory a jim odpovídající druhy tokenů."""
    __operators = {
        '+': SumOperatorToken,
        '-': SubOperatorToken,
        '*': MulOperatorToken,
        '/': DivOperatorToken,
        '=': AssignOperatorToken,
        '?': AndOperatorToken,
        '|': OrOperatorToken,
        '!': NotOperatorToken,
        '<': LesserThanToken,
        '<=': LesserOrEqualToken,
        '>': GreaterThanToken,
        '>=': GreaterOrEqualToken,
        '==': EqualToken,
        '!=': UnequalToken   
    }

    """Pomocná konstanta obsahující všech dostupné oddělovače a jim odpovídající tokeny."""
    __delimiters = {
        '[': LeftTernaryToken,
        ']': RightTernaryToken,
        '(': LeftParToken,
        ')': RightParToken,
        '{': BlockStartToken,
        '}': BlockEndToken,
        ':': TernaryDividerToken,
        ';': ExprEndToken
    }

    def __init__(self, istream: InputStream):
        """
        Konstruktor

        Ze zadaného InputStreamu vytvoří novou instanci tokenizeru.

        :param istream: Stream usnadňující práci se vstupním souborem.
        """
        self.__is = istream
        self.__current = None

    def peek(self) -> Optional[Token]:
        """
        Vrátí aktuální token

        :return: Aktuálně zpracovávaný token.
        """
        if self.__current is None:
            self.__current = self.__get_next_token()
        return self.__current

    def next(self) -> Optional[Token]:
        """
        Vrátí aktuální token a posune se na další v pořadí

        :return: Aktuálně zpracovávaný token.
        """
        token = self.peek()
        self.__current = None
        return token

    def is_eof(self) -> bool:
        """
        Zjistít, zda jsme již přečetli všechny dostupné tokeny

        :return: True v případě, že jsme za posledním tokenem, False jinak.
        """
        return self.peek() is None

    def __get_next_token(self) -> Optional[Token]:
        if self.__is.is_eof():
            return None

        char = self.__is.peek()
        if char == '#':
            self.__skip_comment()
            return self.__get_next_token()
        if char.isdigit():
            return self.__read_number()
        if char == '"':
            return self.__read_string()
        if char.isalpha():
            return self.__read_identifier_or_keyword()
        if self.__is_operator(char):
            return self.__read_operator()
        if self.__is_delimiter(char):
            return self.__read_delimiter()
        if char.isspace():
            self.__is.next()
            return self.__get_next_token()

        self.__is.raise_error("Unexpected character '{:s}' was found.".format(char))

    def __skip_comment(self) -> None:
        while self.__is.is_eof() is False and self.__is.peek() != '\n':
            self.__is.next()

    def __read_number(self) -> Token:
        value = 0
        while self.__is.peek().isdigit():
            value *= 10
            value += int(self.__is.next())
        return NumericConstantToken(value)

    def __read_string(self) -> Token:
        string = "", self.__is.next()
        while self.__is.is_eof() is False and self.__is.peek() != '"':
            string = self.__is.next()

        if self.__is.is_eof():
            self.__is.raise_error("EOF found while reading string constant")

        return StringConstantToken(str(string))

    def __read_identifier_or_keyword(self) -> Token:
        name = ""
        while self.__is.is_eof() is False and self.__is.peek().isalpha():
            name += self.__is.next()

        if self.__is.is_eof():
            self.__is.raise_error("EOF found while reading identifier")

        if Tokenizer.__is_keyword(name):
            return self.__create_keyword(name)
        else:
            return IdentifierToken(name)

    def __read_operator(self) -> OperatorToken:        
        return Tokenizer.__operators.get(self.__is.next())()

    def __read_delimiter(self) -> Token:
        return Tokenizer.__delimiters.get(self.__is.next())()

    @staticmethod
    def __create_keyword(kw: str) -> Union[KeywordToken, BoolConstantToken]:
        return Tokenizer.__keywords.get(kw)()

    @staticmethod
    def __is_keyword(identifier: str) -> bool:
        return identifier in Tokenizer.__keywords.keys()

    @staticmethod
    def __is_operator(op: str) -> bool:
        return op in Tokenizer.__operators.keys()

    @staticmethod
    def __is_delimiter(char: str) -> bool:
        return char in Tokenizer.__delimiters.keys()
