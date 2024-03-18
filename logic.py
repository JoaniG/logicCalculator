from dataclasses import dataclass
from typing import Set
from typing import Any


def create_symbols(symbols_str):
    symbols = []
    for symbol_str in symbols_str.split():
        name = symbol_str.strip("!")
        value = not bool(symbol_str.startswith("!"))
        symbols.append(Symbol(name, value))
    return symbols


@dataclass()
class Symbol:
    name: str
    value: bool = False

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def set_value(self, value):
        self.value = value

    def print_value(self):
        print(f'{self.name}: {self.value}')


@dataclass(frozen=True)
class And:
    left: Any
    right: Any

    def evaluate(self):
        left_value = evaluate(self.left)
        right_value = evaluate(self.right)
        return left_value and right_value

    def __str__(self):
        return f"({print_expression(self.left)} ^ {print_expression(self.right)})"


@dataclass(frozen=True)
class Or:
    left: Any
    right: Any

    def evaluate(self):
        left_value = evaluate(self.left)
        right_value = evaluate(self.right)
        return left_value or right_value

    def __str__(self):
        return f"({print_expression(self.left)} v {print_expression(self.right)})"


@dataclass(frozen=True)
class Implies:
    left: Any
    right: Any

    def evaluate(self):
        left_value = evaluate(self.left)
        right_value = evaluate(self.right)
        return (not left_value) or right_value

    def __str__(self):
        return f"({print_expression(self.left)} -> {print_expression(self.right)})"


@dataclass(frozen=True)
class Not:
    left: Any

    def evaluate(self):
        return not evaluate(self.left)

    def __str__(self):
        return f"!{print_expression(self.left)}"


def evaluate(expression):
    if isinstance(expression, Symbol):
        if expression.value is None:
            raise ValueError(f"Value of symbol {expression.name} is not defined")
        return expression.value
    elif isinstance(expression, (And, Or, Implies, Not)):
        return expression.evaluate()
    else:
        raise ValueError(f"Invalid expression: {expression}")


def print_expression(expression):
    if isinstance(expression, (And, Or, Implies, Not, Symbol)):
        return str(expression)
    else:
        raise ValueError(f"Invalid expression: {expression}")


def get_symbols(expression) -> Set[Symbol]:
    symbols = set()

    if isinstance(expression, Symbol):
        symbols.add(expression)
    elif isinstance(expression, (And, Or, Implies, Not)):
        symbols.update(get_symbols(expression.left))
        if not isinstance(expression, Not):
            symbols.update(get_symbols(expression.right))

    return symbols


def check_true(expression, query=None):
    symbols = get_symbols(expression)
    symbols_length = len(symbols)
    num_of_combinations = 2 ** symbols_length
    flag = False  # Checks if the expression has ever been true.
    message = ''  # In case the query can be both true and false, we print a message
    value = None
    count = 1
    for i in range(num_of_combinations):
        bin_array = decimal_to_binary(i, symbols_length)
        j = 0
        for symbol in symbols:
            if bin_array[j] == 0:
                symbol.set_value(False)
            else:
                symbol.set_value(True)
            j += 1

        if evaluate(expression):
            if query is None:
                flag = True
                print(f'Case {count}:')
                for symbol in symbols:
                    symbol.print_value()
            else:
                if flag:
                    if value != query.value:
                        message = "We don't know"
                value = query.value
                flag = True

    if not flag:
        print('KB is false')

    if message != '':
        print(message)
    else:
        if flag and query is not None:
            print(value)


def decimal_to_binary(decimal, size=None):
    binary_str = bin(decimal)[2:]  # Convert decimal to binary string
    if size is not None:
        binary_str = binary_str.zfill(size)  # Pad with zeros
    return [int(bit) for bit in binary_str]
