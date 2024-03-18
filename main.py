from logic import *


def main():
    """"Logic expression calculator with operators: And, Or, Not, Implies"""
    tuesday = Symbol('p')
    raining = Symbol('q')
    running = Symbol('r')

    exp = And(
        And(Implies(And(tuesday, Not(raining)), running),
            tuesday),
        Not(raining))
    # The expression is: if it is tuesday and not raining, i will be running. it is tuesday, it is not raining

    print('Expression: ' + print_expression(exp))
    print(exp.evaluate())
    print()
    check_true(exp)  # Checks when expression is true


if __name__ == '__main__':
    main()
