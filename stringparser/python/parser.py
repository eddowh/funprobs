# -*- coding: utf-8 -*-

from constants import (
    LOWERCASE_LETTERS,
    UNARY_OPERATORS, BINARY_OPERATORS,
    VALID_CHARS
)


class ReverseUnaryParser(object):
    _value = None
    _operator = None

    def __init__(self, value=None, operator=None):
        self.set_value(value)
        self.set_operator(operator)

    @property
    def value(self):
        return self._value

    @property
    def operator(self):
        return self._operator

    def __str__(self):
        return "{}{}".format(self.value, self.operator)

    def set_value(self, value):
        self._value = value

    def set_operator(self, operator):
        self._operator = operator

    def is_valid(self):
        if not self.value.isalpha() and not self.value.islower():
            return False
        if self.operator not in UNARY_OPERATORS:
            return False
        return True

    def parse(self):
        if not self.is_valid():
            raise ValueError("Cannot parse invalid expression.")
        if self.operator == '<':
            return self.value[1:]
        elif self.operator == '>':
            return self.value[:-1]


class ReverseBinaryParser(object):
    _lhs = None
    _rhs = None
    _operator = None

    def __init__(self, lhs=None, rhs=None, operator=None):
        self.set_lhs(lhs)
        self.set_rhs(rhs)
        self.set_operator(operator)

    @property
    def lhs(self):
        return self._lhs

    @property
    def rhs(self):
        return self._rhs

    @property
    def operator(self):
        return self._operator

    def __str__(self):
        return "{} {} {}".format(self.lhs, self.operator, self.rhs)

    def set_lhs(self, lhs):
        self._lhs = lhs

    def set_rhs(self, rhs):
        self._rhs = rhs

    def set_operator(self, operator):
        self._operator = operator

    def is_valid(self):
        if not self.lhs.isalpha() and not self.lhs.islower():
            return False
        if not self.rhs.isalpha() and not self.rhs.islower():
            return False
        if self.operator not in BINARY_OPERATORS:
            return False
        return True

    def parse(self):
        if not self.is_valid():
            raise ValueError("Cannot parse invalid expression.")
        if self.operator == '+':
            return self.lhs + self.rhs
        elif self.operator == '-':
            lhs = self.rhs[::-1]
            rhs = self.lhs[::-1]
            start_idx = lhs.find(rhs)
            if start_idx < 0:
                res = lhs
            else:
                res = lhs[lhs.find(rhs) + len(rhs):]
            return res[::-1]


class Parser(object):
    _valid_chars = VALID_CHARS

    def __init__(self, string):
        self._string = string

    def __str__(self):
        return self.string

    @property
    def string(self):
        return self._string

    def parse(self):
        stack = ['(', ]
        for char in self.string:
            if char == ' ':  # omit whitespace
                continue
            if char not in self._valid_chars:
                raise ValueError("{} is not a valid character.".format(char))
            if char != ')':  # check for invalid expressions here
                if len(stack) <= 1:  # nothing has been pushed onto the stack
                    if (char in BINARY_OPERATORS or char == ')'):
                        raise SyntaxError(
                            "Expression cannot start with "
                            "binary operators (+,-) or right parentheses."
                        )
                else:
                    prev = stack[-1]
                    if (char in UNARY_OPERATORS and
                            (prev == ')' or prev in LOWERCASE_LETTERS)):
                        raise SyntaxError(
                            "Unary operators (<, >) can't appear after "
                            "right parentheses or letters."
                        )
                    if (char in BINARY_OPERATORS and
                            (prev == '(' or prev in UNARY_OPERATORS)):
                        raise SyntaxError(
                            "Binary operators (+, -) can't appear after "
                            "left parentheses or unary operators."
                        )
                    if (char == '(' and
                            (prev == ')' or prev in LOWERCASE_LETTERS)):
                        raise SyntaxError(
                            "Left parentheses can't appear after "
                            "right parentheses or letters"
                        )
                stack.append(char)
            else:  # start computing inside the paranthesis
                self._parse_within_parenthesis(stack)
        # rest of the stack
        self._parse_within_parenthesis(stack)
        assert len(stack) == 1, "Stack has to be left with one element."
        return stack.pop()[::-1]

    def _parse_within_parenthesis(self, expr_stack):
        # the expression stack has to have a matching left parentheses
        if len(expr_stack) <= 1:
            raise SyntaxError(
                "There are no matching left parentheses."
            )
        # start a binary parser
        rbp = ReverseBinaryParser()
        res = ''
        val = expr_stack[-1]
        top = expr_stack.pop()
        assert top == val
        while top != '(':
            if top in UNARY_OPERATORS:  # parse unary operators
                rup = ReverseUnaryParser(value=res, operator=top)
                res = rup.parse()
            elif top in BINARY_OPERATORS:  # parse binary operators
                if rbp.operator is not None:  # operator has already been set
                    # in which case the operators can't be different
                    # because we're not implementing any rules of precedence
                    if top != rbp.operator:
                        raise SyntaxError(
                            "Different binary operators cannot be chained."
                        )
                    else:
                        # only pluses can be chained
                        if top == '-':
                            raise SyntaxError(
                                "Binary top '-' cannot be chained."
                            )
                        else:
                            assert top == '+'
                            rbp.set_lhs(rbp.lhs + res)
                            rbp.set_operator(top)
                            res = ''
                else:
                    # no operators yet, so set the left hand side and operator
                    rbp.set_lhs(res)
                    rbp.set_operator(top)
                    res = ''  # reset for a potential right hand side
            else:  # just a letter
                res += top
            top = expr_stack.pop()  # this would pop the open paren. eventually
        # if there is a binary expression waiting to be parsed,
        # set the rhs and compute, otherwise keep the last result
        if rbp.lhs is not None and rbp.rhs is None:
            rbp.set_rhs(res)
            res = rbp.parse()
        # expr_stack.pop()  # pop the open paranthesis
        expr_stack.append(res)
