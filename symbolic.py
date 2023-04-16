from lark import Lark
from sys import argv,exit
import z3
from copy import deepcopy


# Evaluate an expression
def evaluateExpr(expr, sym_state):
    if expr.data == 'mul':
        return evaluateExpr(expr.children[0], sym_state) * evaluateExpr(expr.children[1], sym_state)
    elif expr.data == 'div':
        s = z3.Solver()
        for constrainst in sym_state["pc"]:
            s.add(constrainst)
        s.add(evaluateExpr(expr.children[1], sym_state) == 0)
        if s.check() == z3.sat:
            print('RUNTIME ERROR, DIVISION BY 0')
            m = s.model()
            print(m)
            exit(0)
        else: 
            return z3.Int(str(evaluateExpr(expr.children[0], sym_state)) + "/" + str(evaluateExpr(expr.children[1], sym_state)))

    elif expr.data == 'add':
        return evaluateExpr(expr.children[0], sym_state) + evaluateExpr(expr.children[1], sym_state)
    elif expr.data == 'sub':
        return evaluateExpr(expr.children[0], sym_state) - evaluateExpr(expr.children[1], sym_state)
    elif expr.children[0].data == 'var':
        try:
            return sym_state["valueTable"][expr.children[0].children[0].value]
        except:
            print('RUNTIME ERROR, VARIABLE REFERENCE PRE ASSIGNMENT')
            s = z3.Solver()
            for constrainst in sym_state["pc"]:
                s.add(constrainst)
            if s.check() == z3.sat:
                m = s.model()
                print(m)
            exit(0)
    elif expr.children[0].data == 'int':
        return int(expr.children[0].children[0].value)
    
    return evaluateExpr(expr.children[0], sym_state)


# Create state in if-else
def create_if_state(pred, sym_state):
    # Create a new symbolic state
    new_state = deepcopy(sym_state)
    if pred.children[0].data == 'eq':
        old_pc = z3.And(evaluateExpr(pred.children[0].children[0], sym_state) == evaluateExpr(pred.children[0].children[1], sym_state))
        new_pc = z3.And(evaluateExpr(pred.children[0].children[0], sym_state) != evaluateExpr(pred.children[0].children[1], sym_state))
        if old_pc not in sym_state["pc"]: 
            sym_state["pc"].append(old_pc)
        if new_pc not in new_state["pc"]: 
            new_state["pc"].append(new_pc)
        sym_state["schedule"] = [pred.children[1]] + sym_state["schedule"]
        if len(pred.children) == 3:
            new_state["schedule"] = [pred.children[2]] + sym_state["schedule"]
        else:
            new_state["schedule"] = sym_state["schedule"]
        return new_state
    elif pred.children[0].data == 'lt':
        old_pc = z3.And(evaluateExpr(pred.children[0].children[0], sym_state) < evaluateExpr(pred.children[0].children[1], sym_state))
        new_pc = z3.And(evaluateExpr(pred.children[0].children[0], sym_state) >= evaluateExpr(pred.children[0].children[1], sym_state))
        if old_pc not in sym_state["pc"]: 
            sym_state["pc"].append(old_pc)
        if new_pc not in new_state["pc"]: 
            new_state["pc"].append(new_pc)
        sym_state["schedule"] = [pred.children[1]] + sym_state["schedule"]
        if len(pred.children) == 3:
            new_state["schedule"] = [pred.children[2]] + sym_state["schedule"]
        else:
            new_state["schedule"] = sym_state["schedule"]
        return new_state
    elif pred.children[0].data == 'gt':
        old_pc = z3.And(evaluateExpr(pred.children[0].children[0], sym_state) > evaluateExpr(pred.children[0].children[1], sym_state))
        new_pc = z3.And(evaluateExpr(pred.children[0].children[0], sym_state) <= evaluateExpr(pred.children[0].children[1], sym_state))
        if old_pc not in sym_state["pc"]: 
            sym_state["pc"].append(old_pc)
        if new_pc not in new_state["pc"]: 
            new_state["pc"].append(new_pc)
        sym_state["schedule"] = [pred.children[1]] + sym_state["schedule"]
        if len(pred.children) == 3:
            new_state["schedule"] = [pred.children[2]] + sym_state["schedule"]
        else:
            new_state["schedule"] = sym_state["schedule"]
        return new_state


# Execute a program
def execute(schedule, k_unroll = 3):
    # valueTable = {}
    # define_num = 0
    new_state = {"schedule": schedule, "valueTable": {}, "pc": [], "define_num": 0}
    symbolic_states = [new_state]

    for state in symbolic_states:
        while state["schedule"]:
            first = state["schedule"][0]
            state["schedule"] = state["schedule"][1:]

            # unpack different cases

            if first.data == 'p':
                # unpack p to l p or l
                state["schedule"] = first.children + state["schedule"]

            # if it is not a p rule, it is an l rule

            if first.data == 'define':
                # assigns symbolic values to variables
                varname = first.children[0].children[0].value
                state["valueTable"][varname] = z3.Int("s" + str(state["define_num"]))
                state["define_num"] += 1

            if first.data == 'assign':
                # evaluate the expression and assign it to the variable name in the valueTable
                varname = first.children[0].children[0].value
                value = evaluateExpr(first.children[1], state)
                state["valueTable"][varname] = value

            if first.data == 'print':
                # evaluate the expression and print it
                value = evaluateExpr(first.children[0], state)

            if first.data == 'repeat':
                # add the body of the loop to the schedule int times
                value = int(first.children[0].children[0].value)
                # if k_unroll !=  None and value > int(k_unroll):
                #     value = int(k_unroll)
                body = first.children[1]
                state["schedule"] = [body for _ in range(value)] + state["schedule"]

            if first.data == 'if':
                # evaluate the predicate and add if or else body to the schedule
                new_state = create_if_state(first, state)
                # prune the False branch
                s_new = z3.Solver()
                for constrainst in new_state["pc"]:
                    s_new.add(constrainst)
                if s_new.check() == z3.sat:
                    symbolic_states.append(new_state)

                s_old = z3.Solver()
                for constrainst in state["pc"]:
                    s_old.add(constrainst)
                if s_old.check() != z3.sat:
                    break
            
            if first.data == 'while':
                value = int(k_unroll)
                first.data = "if"
                body = first
                state["schedule"] = [body for _ in range(value)] + state["schedule"]
    
    print("NO ERRORS FOUND")



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

    elif len(argv) == 3:
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
        execute([tree], argv[2])

    else:
        print("INVALID SYS ARGS")
