import math

def check_brackets(expr):
    stack = []
    for ch in expr:
        if ch == "(":
            stack.append("(")
        elif ch == ")":
            if stack == []:
                return False
            stack.pop()
    if stack == []:
        return True
    else:
        return False

def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch.isdigit():
            start = i
            while i < len(expr) and expr[i].isdigit():
                i += 1
            tokens.append(expr[start:i])
        elif ch.isalpha():
            start = i
            while i < len(expr) and expr[i].isalpha():
                i += 1
            tokens.append(expr[start:i])
        elif ch == ' ':
            i += 1
        else:
            tokens.append(ch)
            i += 1
    return tokens

priority = {'+': 1, '-': 1, '*': 2, '/': 2, 'u-': 3, '^': 4}
right_assoc = {'^'}
functions = {'floor', 'sqrt'}

def to_rpn(tokens):
    output = []
    stack = []
    for i, t in enumerate(tokens):
        if t.isdigit():
            output.append(t)
        elif t in functions:
            stack.append(t)
        elif t == '(':
            stack.append(t)
        elif t == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
            if stack and stack[-1] in functions:
                output.append(stack.pop())
        elif t in ('+', '-') and is_unary(tokens, i):
            if t == '-':
                stack.append('u-')
        elif t in priority:
            if t in right_assoc:
                while stack and stack[-1] != '(' and priority[t] < priority[stack[-1]]:
                    output.append(stack.pop())
            else:
                while stack and stack[-1] != '(' and priority[t] <= priority[stack[-1]]:
                    output.append(stack.pop())
            stack.append(t)
    while stack:
        output.append(stack.pop())
    return output

def evaluate_rpn(rpn):
    stack = []
    for t in rpn:
        if t.isdigit():
            stack.append(int(t))
        elif t == 'u-':
            a = stack.pop()
            stack.append(-a)
        elif t == 'sqrt':
            a = stack.pop()
            if a < 0:
                raise ValueError("корінь з від'ємного числа")
            stack.append(math.sqrt(a))
        elif t == 'floor':
            a = stack.pop()
            stack.append(math.floor(a))
        elif t in priority:
            b = stack.pop()
            a = stack.pop()
            if t == '+':
                stack.append(a + b)
            elif t == '-':
                stack.append(a - b)
            elif t == '*':
                stack.append(a * b)
            elif t == '/':
                if b == 0:
                    raise ValueError('ділення на нуль')
                stack.append(a / b)
            elif t == '^':
                if a == 0 and b < 0:
                    raise ValueError('ділення на нуль')
                if a < 0 and not float(b).is_integer():
                    raise ValueError("результат не є дійсним числом")
                if abs(a) > 1 and b * math.log10(abs(a)) > 4000:
                    raise ValueError("результат завеликий")
                stack.append(a ** b)
    return stack[-1]

def calculate(expr):
    try:
        if not check_brackets(expr):
            raise ValueError("дужки розставлено неправильно")
        tokens = tokenize(expr)
        validate(tokens)
        rpn = to_rpn(tokens)
        return evaluate_rpn(rpn)
    except ValueError as e:
        return "Помилка: " + str(e)
    except OverflowError:
        return "Помилка: число завелике"

def is_unary(tokens, i):
    previous = tokens[i-1]
    if i == 0 and tokens[i] in ('+', '-'):
        return True
    elif tokens[i] in ('+', '-'):
        if previous in priority or previous == '(':
            return True
    return False

def validate(tokens):
    expect_operand = True
    for i, t in enumerate(tokens):
        if expect_operand:
            if t.isdigit():
                expect_operand = False
            elif t in ('(', '+', '-'):
                expect_operand = True
            elif t in functions:
                if i + 1 < len(tokens) and tokens[i+1] == '(':
                    expect_operand = True
                else:
                    raise ValueError("після функції має бути (")
            elif t in ('*', '/', '^', ')'):
                raise ValueError("оператор або ) без операнда")
            else:
                raise ValueError("невідомий символ")
        else:
            if t in ('+', '-', '*', '/', '^'):
                expect_operand = True
            elif t == ')':
                expect_operand = False  #
            else:
                if t.isdigit() or t == '(' or t in functions:
                    raise ValueError("неправильний порядок")
                else:
                    raise ValueError("невідомий символ")
    if expect_operand:
        raise ValueError("неправильний порядок")

if __name__ == "__main__":
    while True:
        expr = input("Введіть вираз (exit для виходу): ")
        if expr.lower().strip() == "exit":
            print('End')
            break
        if expr.strip() == '':
            print('Порожній рядок')
            continue
        print(calculate(expr))