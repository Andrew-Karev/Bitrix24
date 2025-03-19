import re

# Универсальный класс для всех узлов
class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type  # 'number', 'variable', 'binary', 'unary'
        self.value = value  # для чисел и переменных
        self.left = left  # для бинарных и унарных операций
        self.right = right  # для бинарных операций

# Токенизация выражения
def tokenize(expression):
    token_pattern = r'\d+|[xyz]|\+|\-|\*|\(|\)'
    tokens = re.findall(token_pattern, expression)
    if ''.join(tokens) != expression.replace(' ', ''):
        raise ValueError("Недопустимое выражение")
    return tokens

# Парсер
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        if not self.tokens:
            raise ValueError("Недопустимое выражение")
        node = self.parse_expression()
        if self.pos != len(self.tokens):
            raise ValueError("Недопустимое выражение")
        return node

    def parse_expression(self):
        node = self.parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ('+', '-'):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_term()
            node = Node('binary', op, node, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == '*':
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_factor()
            node = Node('binary', op, node, right)
        return node

    def parse_factor(self):
        if self.pos >= len(self.tokens):
            raise ValueError("Недопустимое выражение")
        token = self.tokens[self.pos]
        if token.isdigit():
            self.pos += 1
            return Node('number', int(token))
        elif token in ('x', 'y', 'z'):
            self.pos += 1
            return Node('variable', token)
        elif token == '(':
            self.pos += 1
            node = self.parse_expression()
            if self.pos >= len(self.tokens) or self.tokens[self.pos] != ')':
                raise ValueError("Недопустимое выражение")
            self.pos += 1
            return node
        elif token == '-':
            self.pos += 1
            child = self.parse_factor()
            return Node('unary', '-', child)
        else:
            raise ValueError("Недопустимое выражение")

# Комбинирование словарей
def combine_dicts(d1, d2, op):
    result = d1.copy()
    for key, coeff in d2.items():
        result[key] = op(result.get(key, 0), coeff)
    return {k: v for k, v in result.items() if v != 0}

# Умножение словарей
def multiply_dicts(d1, d2):
    result = {}
    for key1, coeff1 in d1.items():
        for key2, coeff2 in d2.items():
            new_key = tuple(sorted(key1 + key2))
            result[new_key] = result.get(new_key, 0) + coeff1 * coeff2
    return {k: v for k, v in result.items() if v != 0}

# Упрощение выражения
def simplify(node):
    if node.type == 'number':
        return {(): node.value}
    elif node.type == 'variable':
        return {(node.value,): 1}
    elif node.type == 'binary':
        left = simplify(node.left)
        right = simplify(node.right)
        if node.value == '+':
            return combine_dicts(left, right, lambda a, b: a + b)
        elif node.value == '-':
            return combine_dicts(left, right, lambda a, b: a - b)
        elif node.value == '*':
            return multiply_dicts(left, right)
    elif node.type == 'unary':
        child = simplify(node.left)
        return multiply_dicts({(): -1}, child)

# Форматирование результата
def dict_to_string(d):
    if not d:
        return '0'
    terms = []
    for key in sorted(d, key=lambda k: (-len(k), k)):
        coeff = d[key]
        if key:
            mon_str = '*'.join(key)
            term = mon_str if abs(coeff) == 1 else f"{abs(coeff)}*{mon_str}"
        else:
            term = str(abs(coeff))
        terms.append((term, coeff > 0))
    result = terms[0][0] if terms[0][1] else '-' + terms[0][0]
    for term, positive in terms[1:]:
        result += ' + ' + term if positive else ' - ' + term
    return result

# Основная функция
def simplify_expression(expression):
    try:
        tokens = tokenize(expression)
        parser = Parser(tokens)
        node = parser.parse()
        simplified_dict = simplify(node)
        return dict_to_string(simplified_dict)
    except ValueError:
        return "Недопустимое выражение"

# Тесты
test_cases = [
    "2 * (3 * x + 4 * y) - 7 * y + 9",
    "z + z + 2 + 3 - 2 * z",
    "3 * ((",
    "x * y + 2 * x * y",
    "x * 5 - 5 * x",
    "5 * (x + 1)"
]
for test in test_cases:
    print(f"Вход: {test}")
    print(f"Выход: {simplify_expression(test)}\n")