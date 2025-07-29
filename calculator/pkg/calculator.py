# calculator.py


class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_expression(tokens)

    def _evaluate_expression(self, tokens):
        # Multiplication and Division
        i = 1
        while i < len(tokens) - 1:
            if tokens[i] == "*":
                result = float(tokens[i - 1]) * float(tokens[i + 1])
                tokens = tokens[: i - 1] + [str(result)] + tokens[i + 2 :]
                i = 1  # Reset index to re-evaluate from the beginning
            elif tokens[i] == "/":
                result = float(tokens[i - 1]) / float(tokens[i + 1])
                tokens = tokens[: i - 1] + [str(result)] + tokens[i + 2 :]
                i = 1  # Reset index
            else:
                i += 1

        # Addition and Subtraction
        i = 1
        while i < len(tokens) - 1:
            if tokens[i] == "+":
                result = float(tokens[i - 1]) + float(tokens[i + 1])
                tokens = tokens[: i - 1] + [str(result)] + tokens[i + 2 :]
                i = 1  # Reset index
            elif tokens[i] == "-":
                result = float(tokens[i - 1]) - float(tokens[i + 1])
                tokens = tokens[: i - 1] + [str(result)] + tokens[i + 2 :]
                i = 1  # Reset index
            else:
                i += 1

        return float(tokens[0])
