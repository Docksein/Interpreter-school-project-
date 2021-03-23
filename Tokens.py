from abc import ABC


class Token(ABC):

    def __init__(self):
        pass

    def __str__(self):
        return "<TOKEN type={:s}>".format(str(type(self)))


class ConstantToken(Token):

    def __init__(self, value):
        super().__init__()
        self.__value = value

    def get_value(self):
        return self.__value


class NumericConstantToken(ConstantToken):

    def __init__(self, value: int):
        super().__init__(value)

    def get_value(self) -> int:
        return int(super().get_value())

    def __str__(self):
        return "<CONST_NUM val='{:d}'>".format(super().get_value())


class StringConstantToken(ConstantToken):

    def __init__(self, value: str):
        super().__init__(value)

    def get_value(self) -> str:
        return str(super().get_value())

    def __str__(self):
        return "<CONST_STR val='{:s}'>".format(super().get_value())


class BoolConstantToken(ConstantToken):

    @staticmethod
    def true():
        return BoolConstantToken(True)

    @staticmethod
    def false():
        return BoolConstantToken(False)

    def __init__(self, value: bool):
        super().__init__(value)

    def get_value(self) -> bool:
        return bool(super().get_value())

    def __str__(self):
        return "<CONST_BOOL val='{:s}'>".format(str(super().get_value()))


class KeywordToken(Token):

    def __init__(self):
        super().__init__()


class IfKeywordToken(KeywordToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<KW_IF>"


class ThenKeywordToken(KeywordToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<KW_THEN>"


class ElseKeywordToken(KeywordToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<KW_ELSE>"


class PrintKeywordToken(KeywordToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<KW_PRINT>"


class ReadKeywordToken(KeywordToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<KW_READ>"


class OperatorToken(Token):

    def __init__(self):
        super().__init__()


class UnaryOperatorToken(OperatorToken):

    def __init__(self):
        super().__init__()


class BinaryOperatorToken(OperatorToken):

    def __init__(self):
        super().__init__()


class SumOperatorToken(BinaryOperatorToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<OP_SUM>"


class SubOperatorToken(BinaryOperatorToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<OP_SUB>"


class MulOperatorToken(BinaryOperatorToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<OP_MUL>"


class DivOperatorToken(BinaryOperatorToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<OP_DIV>"


class AndOperatorToken(BinaryOperatorToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<OP_AND>"


class OrOperatorToken(BinaryOperatorToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<OP_OR>"


class AssignOperatorToken(BinaryOperatorToken):  

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<OP_ASSIGN>"


class NotOperatorToken(UnaryOperatorToken):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<OP_NOT>"


class IdentifierToken(Token):

    def __init__(self, name: str):
        super().__init__()
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def __str__(self):
        return "<IDENT name='{:s}'>".format(self.get_name())


class LeftParToken(Token):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<LPAR>"


class RightParToken(Token):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<RPAR>"


class BlockStartToken(Token):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<SBLOCK>"


class BlockEndToken(Token):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<EBLOCK>"


class ExprEndToken(Token):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "<SEMICOLON>"

class LesserThanToken(BinaryOperatorToken):   
    def __init__(self):
        super().__init__()
    
    def __str__(self):      
        return "<OP_LESSER_THAN>"

class LesserOrEqualToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<OP_LESSER_OR_EQUAL_THAN>"

class GreaterThanToken(BinaryOperatorToken): 
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<OP_GREATER_THAN>"

class GreaterOrEqualToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<OP_GREATER_OR_EQUAL_THAN>"


class EqualToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<OP_EQUAL>"


class UnequalToken(BinaryOperatorToken):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<OP_UNEQUAL>"

class LeftTernaryToken:
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<LTERN>"

class RightTernaryToken:
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<RTERN>"

class TernaryDividerToken:
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "<DIVTERN>"
