# -*- coding: utf-8 -*-

from parser import Parser


INPUTS = [
    "(<<dagobah -(>>yoda+go ))",  # evaluates to b
    "(((<<dagobah -(>>yoda+go ))))",  # evaluates to b
    "<> <<<((eve + boo+buzz)  - ( >< <nemo))",  # evaluates to eboo
    "<>((<<mario + >>zelda)- ><samus)",  # evaluates to arld
    "((<mccoy+sulu)",  # missing parenthesis
    "(leonardo-foot+splinter)",  # mixing operators
    "(+pikachu+charizard)",  # extra +
    "(clARk + bruCE)",  # the strings use capital letters
]


def main():
    for i in INPUTS:
        p = Parser(i)
        try:
            print p.parse()
        except Exception as e:
            print e


if __name__ == '__main__':
    main()
