from LexicalAnalysis import Tokenizer
from Tokens import *
from AST import *


class Parser:
    __precedence = {
        AssignOperatorToken: 1,
        OrOperatorToken: 2,
        AndOperatorToken: 3,
        SumOperatorToken: 10, SubOperatorToken: 10, IncrementOpToken: 10, DecrementOpToken: 10,
        MulOperatorToken: 20, DivOperatorToken: 20
    }

    def __init__(self, tokenizer: Tokenizer):
        self.__tokenizer = tokenizer

    def parse(self):
        root = ASTNodeProg()

        while self.__tokenizer.is_eof() is False:
            expr = self.parse_expression()
            if self.__tokenizer.is_eof() is False:
                if isinstance(self.__tokenizer.peek(), BinaryOperatorToken):
                    root.add_expression(self.parse_binary_operator(expr))
                    self.skip(ExprEndToken)               
                else:
                    root.add_expression(expr)
                    self.skip(ExprEndToken)
            else:
                root.add_expression(expr)

        return root

    def parse_expression(self):
        node = None
        if isinstance(self.__tokenizer.peek(), BoolConstantToken):
            node = self.parse_boolean_constant()
        elif isinstance(self.__tokenizer.peek(), NumericConstantToken):
            node = self.parse_numeric_constant()
        if isinstance(self.__tokenizer.peek(), StringConstantToken):
            node = self.parse_string_constant()
        if isinstance(self.__tokenizer.peek(), IfKeywordToken):
            node = self.parse_if_statement()
        if isinstance(self.__tokenizer.peek(), BlockStartToken):
            node = self.parse_block()
        if isinstance(self.__tokenizer.peek(), UnaryOperatorToken):
            node = self.parse_unary_operator()
        if isinstance(self.__tokenizer.peek(), IdentifierToken):
            node = self.parse_identifier()
        if isinstance(self.__tokenizer.peek(), ReadKeywordToken):
            node = self.parse_read_keyword()
        if isinstance(self.__tokenizer.peek(), PrintKeywordToken):
            node = self.parse_print_keyword()
        if isinstance(self.__tokenizer.peek(), TernaryLeft):
            node = self.parse_ternary()
        if isinstance(self.__tokenizer.peek(), WhileKeywordToken):
            node = self.parse_while()
        if isinstance(self.__tokenizer.peek(), BinaryOperatorToken):
            return self.parse_binary_operator(node)
        if isinstance(self.__tokenizer.peek(), IncrementOperatorToken):
            return self.parse_increment_operator(node)
        else:
            return node

    def parse_boolean_constant(self):
        return ASTNodeBoolConst(self.__tokenizer.next().get_value())

    def parse_numeric_constant(self):
        return ASTNodeNumConst(self.__tokenizer.next().get_value())

    def parse_string_constant(self):
        return ASTNodeStringConst(self.__tokenizer.next().get_value())

    def parse_if_statement(self):
        self.__tokenizer.next()  # Skip if kw

        condition = self.parse_condition()
        self.skip(ThenKeywordToken)
        then_block = self.parse_block()

        root = ASTNodeCondStatement(condition, then_block)

        if isinstance(self.__tokenizer.peek(), ElseKeywordToken):
            self.__tokenizer.next()  # Skip else kw
            root.set_else(self.parse_block())

        return root

    def skip(self, token_type):
        if isinstance(self.__tokenizer.peek(), token_type):           
            self.__tokenizer.next()
        else:
            raise TypeError

    def parse_condition(self):
        self.skip(LeftParToken)
        expr = self.parse_expression()
        self.skip(RightParToken)
        return expr

    def parse_block(self):
        self.skip(BlockStartToken)

        root = ASTNodeProg()
        while self.__tokenizer.is_eof() is False \
                and isinstance(self.__tokenizer.peek(), BlockEndToken) is False:
            root.add_expression(self.parse_expression())
            self.skip(ExprEndToken)

        if self.__tokenizer.is_eof():
            raise EOFError

        self.skip(BlockEndToken)
        return root

    def parse_ternary_condition(self):
        self.skip(TernaryLeft)
        expr = self.parse_expression()
        self.skip(TernaryRight)
        return expr

    def parse_ternary_true(self):
        self.skip(AndOperatorToken)

        root = ASTNodeProg()
        while self.__tokenizer.is_eof() is False and isinstance(self.__tokenizer.peek(), TernaryDivider) is False:
            root.add_expression(self.parse_expression())

        if self.__tokenizer.is_eof():
            raise EOFError

        return root

    def parse_ternary_false(self):
        self.skip(TernaryDivider)
        root = ASTNodeProg()
        while self.__tokenizer.is_eof() is False and isinstance(self.__tokenizer.peek(), ExprEndToken) is False:
            root.add_expression(self.parse_expression())
            self.skip(ExprEndToken)
            

        return root

    def parse_ternary(self):
        condition = self.parse_ternary_condition()
        true_ternary = self.parse_ternary_true()
        false_ternary = self.parse_ternary_false()

        root = ASTNodeTernStatement(condition, true_ternary, false_ternary)       
        return root
    
    def parse_while(self):
        self.__tokenizer.next()
        condition = self.parse_condition()
        while_block = self.parse_block();

        root = ASTNodeWhileLoop(condition, while_block)

        return root

    def parse_increment_operator(self, left_operand: ASTNode):
        operator = self.__tokenizer.next()

        if isinstance(operator, IncrementOpToken):
            node = ASTNodeOpIncr(left_operand)
        elif isinstance(operator, DecrementOpToken):
            node = ASTNodeOpDecr(left_operand)        
        else:
            raise TypeError
        return node


    def parse_binary_operator(self, left_operand: ASTNode):
        operator = self.__tokenizer.next()
        right_operand = self.parse_expression()

        node = None
        if isinstance(operator, SumOperatorToken):
            node = ASTNodeOpSum(left_operand, right_operand)
        elif isinstance(operator, AssignOperatorToken):
            node = ASTNodeOpAssign(left_operand, right_operand)
        elif isinstance(operator, SubOperatorToken):
            node = ASTNodeOpSub(left_operand, right_operand)
        elif isinstance(operator, MulOperatorToken):
            node = ASTNodeOpMul(left_operand, right_operand)
        elif isinstance(operator, DivOperatorToken):
            node = ASTNodeOpDiv(left_operand, right_operand)
        elif isinstance(operator, AndOperatorToken):
            node = ASTNodeOpAnd(left_operand, right_operand)
        elif isinstance(operator, OrOperatorToken):
            node = ASTNodeOpOr(left_operand, right_operand)
        elif isinstance(operator, GreaterThanToken):
            node = ASTNodeOpGrThan(left_operand, right_operand)
        elif isinstance(operator, GreaterOrEqualToken):
            node = ASTNodeOpGrOrEqual(left_operand, right_operand)
        elif isinstance(operator, EqualToken):
            node = ASTNodeOpEqual(left_operand, right_operand)
        elif isinstance(operator, NotEqualToken):
            node = ASTNodeOpNotEq(left_operand, right_operand)
        elif isinstance(operator, LesserThanToken):
            node = ASTNodeOpLess(left_operand, right_operand)
        elif isinstance(operator, LesserOrEqualToken):
            node = ASTNodeOpLesOrEqual(left_operand, right_operand)             

        else:
            raise TypeError

        if isinstance(self.__tokenizer.peek(), BinaryOperatorToken):
            if self.__precedence[type(operator)] > self.__precedence[type(self.__tokenizer.peek())]:
                return self.parse_binary_operator(node)
            else:
                node.change_right_child(self.parse_binary_operator(right_operand))
                return node
        else:
            return node

    def parse_unary_operator(self):            
        if isinstance(self.__tokenizer.peek(), NotOperatorToken):
            return ASTNodeOpNot(self.parse_expression())
        else:
            raise TypeError

    def parse_identifier(self):
        return ASTNodeIdent(self.__tokenizer.next().get_name())

    def parse_read_keyword(self):
        self.skip(ReadKeywordToken)
        return ASTNodeReadKeyword(self.parse_expression())

    def parse_print_keyword(self):
        self.skip(PrintKeywordToken)
        return ASTNodePrintKeyword(self.parse_expression())
