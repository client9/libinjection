#!/usr/bin/python

mysql_ops = (
    'AND',
    '&&',
    '=',
    '&',
    '|',
    '^',
    'DIV',
    '/',
    '<=>',
    '>=',
    '>',
    '<<',
    '<=',
    '<',
    'LIKE',
    '-',
    '%',
    'MOD',
    '!=',
    '<>',
    'NOT LIKE',
    'NOT REGEXP',
    'OR',
    '||',
    '+',
    'REGEXP',
    '>>',
    'RLIKE',
    'SOUNDS LIKE',
    '*',
    'XOR'
)

print '# mysql implicit conversions tests'

for op in mysql_ops:
    print "A' {0} 'B".format(op)
    print "A '{0}' B".format(op)
