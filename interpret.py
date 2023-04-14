from lark import Lark
from sys import argv,exit
import z3
from copy import deepcopy


# Evaluate an expression
def evaluateExpr(expr, valueTable):
    if expr.data == 'mul':
        return evaluateExpr(expr.children[0], valueTable) * evaluateExpr(expr.children[1], valueTable)
    if expr.data == 'div':
        try:
            return int(evaluateExpr(expr.children[0], valueTable) / evaluateExpr(expr.children[1], valueTable))
        except:
            print('RUNTIME ERROR, DIVISION BY 0')
            exit(0)
    if expr.data == 'add':
        return evaluateExpr(expr.children[0], valueTable) + evaluateExpr(expr.children[1], valueTable)
    if expr.data == 'sub':
        return evaluateExpr(expr.children[0], valueTable) - evaluateExpr(expr.children[1], valueTable)
    if expr.children[0].data == 'var':
        try:
            return valueTable[expr.children[0].children[0].value]
        except:
            print('RUNTIME ERROR, VARIABLE REFERENCE PRE ASSIGNMENT')
            exit(0)
    if expr.children[0].data == 'int':
        return int(expr.children[0].children[0].value)
    return evaluateExpr(expr.children[0], valueTable)

# Evaluate a predicate
def evaluatePred(pred, valueTable):
    if pred.data == 'eq':
        return evaluateExpr(pred.children[0], valueTable) == evaluateExpr(pred.children[1], valueTable)
    if pred.data == 'lt':
        return evaluateExpr(pred.children[0], valueTable) < evaluateExpr(pred.children[1], valueTable)
    if pred.data == 'gt':
        return evaluateExpr(pred.children[0], valueTable) > evaluateExpr(pred.children[1], valueTable)


# Execute a program
def execute(schedule):
    valueTable = {}
    while schedule:
        first = schedule[0]
        schedule = schedule[1:]

        # unpack different cases

        if first.data == 'p':
            # unpack p to l p or l
            schedule = first.children + schedule

        # if it is not a p rule, it is an l rule

        if first.data == 'define':
            # prompt user to define the variable repeatedly, until they input an int
            varname = first.children[0].children[0].value
            valueTable[varname] = None
            while not valueTable[varname] != None:
                try:
                    valueTable[varname] = int(input("Enter value for %s: " % varname))
                except:
                    pass

        if first.data == 'assign':
            # exaluate the expression and assign it to the variable name in the valueTable
            varname = first.children[0].children[0].value
            value = evaluateExpr(first.children[1], valueTable)
            valueTable[varname] = value

        if first.data == 'print':
            # evaluate the expression and print it
            value = evaluateExpr(first.children[0], valueTable)
            print(value)

        if first.data == 'repeat':
            # add the body of the loop to the schedule int times
            value = int(first.children[0].children[0].value)
            body = first.children[1]
            schedule = [body for _ in range(value)] + schedule

        if first.data == 'if':
            # evaluate the predicate and add if or else body to the schedule
            if evaluatePred(first.children[0], valueTable):
                schedule = [first.children[1]] + schedule
            else:
                schedule = [first.children[2]] + schedule



if __name__ == '__main__':
    if len(argv) == 2:
        parser = Lark(open("grammar").read(), start ="p")
        fname = argv[1]
        try:
            f = open(fname)
        except:
            print("CAN'T OPEN", fname)
            exit(0)
        try:
            tree = parser.parse(f.read())
        except:
            print("PARSER ERROR")
            exit(0)
        execute([tree])

    else:
        print("INVALID SYS ARGS")
