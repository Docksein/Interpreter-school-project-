from abc import ABC
from typing import TypeVar, Generic


class ASTNode(ABC):   
    """
    Abstraktní třída představující uzel syntaktického stromu

    Tato třída slouží jako společný předek všech konkrétních
    druhů uzlů.  Díky tomuto společnému předkovi můžeme ke
    všem konkrétním vrcholům přistupovat stejně a máme
    zajištěno, že budou mít požadované metody.
    """

    def __init__(self):
        """
        Konstruktor.
        
        :param self: 
        :return: 
        """
        pass

    def evaluate(self, symbol_table: dict):
        """
        Metoda slouží k vyhodnocení konkrétního uzlu
        syntaktického stromu.

        :param self:
        :param symbol_table: Tabulka symbolů slouží k udržování
        informací o proměnných (jméno, hodnota) a o funkcích.

        :return: Výsledek vyhodnocení vrcholu. Podoba záleží 
        na konkrétním druhu vrcholu. 
        """
        pass


#####################################################
# KEYWORDS & VARIABLES                              #
#####################################################
class ASTNodeIdent(ASTNode):

    def __init__(self, name: str):
        super().__init__()
        self.__name = name

    def get_name(self):
        return self.__name

    def evaluate(self, symbol_table: dict):
        return symbol_table[self.__name]


class ASTNodeReadKeyword(ASTNode):

    def __init__(self, ex: ASTNodeIdent):
        super().__init__()
        self.__expr = ex
        
    def evaluate(self, symbol_table: dict):
        data = input("> ")
        try:
            symbol_table[self.__expr.get_name()] = int(data)
        except ValueError:
            if data == "True":
                symbol_table[self.__expr.get_name()] = True
            elif data == "False":
                symbol_table[self.__expr.get_name()] = False
            else:
                symbol_table[self.__expr.get_name()] = data


class ASTNodePrintKeyword(ASTNode):

    def __init__(self, ex: ASTNode):
        super().__init__()
        self.__expr = ex

    def evaluate(self, symbol_table: dict):
        return print(str(self.__expr.evaluate(symbol_table)))


#####################################################
# CONSTANTS                                         #
#####################################################
CT = TypeVar('CT')


class ASTNodeConstant(ASTNode, Generic[CT]):

    def __init__(self, value: CT):
        super().__init__()
        self.__value__ = value

    def evaluate(self, symbol_table: dict) -> CT:
        return self.__value__


class ASTNodeBoolConst(ASTNodeConstant[bool]):
    pass


class ASTNodeNumConst(ASTNodeConstant[int]):
    pass


class ASTNodeStringConst(ASTNodeConstant[str]):
    pass


#####################################################
# OTHERS                                            #
#####################################################
class ASTNodeProg(ASTNode):

    def __init__(self):
        super().__init__()
        self.__expressions = []

    def add_expression(self, expression: ASTNode):
        self.__expressions.append(expression)

    def evaluate(self, symbol_table: dict):
        for e in self.__expressions:
            e.evaluate(symbol_table)


class ASTNodeCondStatement(ASTNode):

    def __init__(self, condition: ASTNode, then: ASTNode):
        super().__init__()
        self.__condition = condition
        if isinstance(then, ASTNodeProg) is False:
            raise TypeError
        self.__then = then
        self.__else = None

    def set_else(self, expressions: ASTNode):
        if isinstance(expressions, ASTNodeProg) is False:
            raise TypeError
        self.__else = expressions

    def evaluate(self, symbol_table: dict):
        if self.__condition.evaluate(symbol_table) is True:
            self.__then.evaluate(symbol_table)
        else:
            if self.__else is not None:
                self.__else.evaluate(symbol_table)

class ASTNodeTernStatement(ASTNode):
    def __init__(self, condition: ASTNode, true_ternary: ASTNode, false_ternary: ASTNode):
        super().__init__()
        self.__condition = condition
        if isinstance(true_ternary, ASTNodeProg) is False:
            raise TypeError
        self.__true_ternary = true_ternary
        if isinstance(false_ternary, ASTNodeProg) is False:
            raise TypeError
        self.__false_ternary = false_ternary
    
    def evaluate(self, symbol_table: dict):
        if self.__condition.evaluate(symbol_table) is True:
            self.__true_ternary.evaluate(symbol_table)
        else:
            self.__false_ternary.evaluate(symbol_table)


#####################################################
# OPERATORS                                         #
#####################################################

class ASTNodeBinaryOp(ASTNode, ABC):

    def __init__(self, left_child: ASTNode, right_child: ASTNode, op):
        super().__init__()
        self.__left_child = left_child
        self.__right_child = right_child
        self.__op = op

    def change_right_child(self, right_child: ASTNode):
        self.__right_child = right_child

    def evaluate(self, symbol_table: dict):
        return self.__op(self.__left_child.evaluate(symbol_table),
                         self.__right_child.evaluate(symbol_table))


class ASTNodeUnaryOp(ASTNode, ABC):

    def __init__(self, child: ASTNode, op):
        super().__init__()
        self.__child = child
        self.__op = op

    def evaluate(self, symbol_table: dict):
        return self.__op(self.__child)


class ASTNodeOpAssign(ASTNodeBinaryOp):

    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, None)

        if isinstance(left_child, ASTNodeIdent) is False:
            raise TypeError

    def evaluate(self, symbol_table: dict):
        symbol_table[self._ASTNodeBinaryOp__left_child.get_name()] \
            = self._ASTNodeBinaryOp__right_child.evaluate(symbol_table)


class ASTNodeOpSum(ASTNodeBinaryOp):

    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x + y)


class ASTNodeOpSub(ASTNodeBinaryOp):

    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x - y)


class ASTNodeOpMul(ASTNodeBinaryOp):

    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x * y)


class ASTNodeOpDiv(ASTNodeBinaryOp):

    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x / y)


class ASTNodeOpAnd(ASTNodeBinaryOp):

    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x and y)


class ASTNodeOpOr(ASTNodeBinaryOp):

    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x or y)

class ASTNodeOpLess(ASTNodeBinaryOp):
    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x < y)

class ASTNodeOpGreat(ASTNodeBinaryOp):
    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x > y)

class ASTNodeOpLessEq(ASTNodeBinaryOp):
    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x <= y)

class ASTNodeOpGreatEq(ASTNodeBinaryOp):
    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x >= y)

class ASTNodeOpEqual(ASTNodeBinaryOp):
    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x == y)

class ASTNodeOpUnequal(ASTNodeBinaryOp):
    def __init__(self, left_child: ASTNode, right_child: ASTNode):
        super().__init__(left_child, right_child, lambda x, y: x != y)

class ASTNodeOpNot(ASTNodeUnaryOp):
    def __init__(self, child: ASTNode):
        super().__init__(child, lambda x: not x)


