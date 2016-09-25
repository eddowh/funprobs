# -*- coding: utf-8 -*-

LOWERCASE_LETTERS = set([
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
])

UNARY_OPERATORS = set([
    '<', '>',
])

BINARY_OPERATORS = set([
    '+', '-',
])

OPERATORS = UNARY_OPERATORS.union(BINARY_OPERATORS)
VALID_CHARS = LOWERCASE_LETTERS.union(OPERATORS).union(set(['(', ')']))
