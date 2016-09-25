# Problem Statement

Write a program that will read expressions consisting of strings and operations from a file, and evaluate and show the output of the given expression.

String expressions consist of strings, the operators `+` (concatenate), `-` (remove), `<` (remove end), and `>` (remove start), along with parentheses to specify a desired order of operations:

* the `<` operator indicates you should delete the last character of the string
* the `>` operator indicates you should delete the first character of the string
* the `+` operator indicates you should append the second string to the end of the first string
* the `-` operator indicates that you should remove the first instance of the second string from the first string (the first string is returned unmodified if there is no match).

String expressions are defined formally as follows:

1. Any string of 1 or more letters a-z (lower-case only) is a string expression.
2. If Y1, Y2, ..., Yk are string expressions then the following are string expressions:
    * <Y1
    * \>Y1
    * (Y1-Y2)
    * (Y1+Y2+Y3+...+Yk)

Notice that the format rules out the expression ab+bc, since it is missing the parentheses. It also rules out `(ab+bc-b)` which would have to instead be written `((ab+bc)-b)`, so no rule of precedence needs to be implemented.

Whitespace may occur in arbitrary places in string expressions, but never in the middle of a string of letters. Each expression will be on a single line.

Examples (the first three are valid, the other four are not):

    (<<dagobah -(>>yoda+go ))                // evaluates to b
    <> <<<((eve + boo+buzz)  - ( >< <nemo))  // evaluates to eboo
    <>((<<mario + >>zelda)- ><samus)         // evaluates to arld
    ((<mccoy+sulu)                           // missing parenthesis
    (leonardo-foot+splinter)                 // mixing operators
    (+pikachu+charizard)                     // extra +
    (clARk + bruCE)                          // the strings use capital letters
