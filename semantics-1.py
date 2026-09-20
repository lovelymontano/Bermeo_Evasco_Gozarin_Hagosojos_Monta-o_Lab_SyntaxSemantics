# Laboratory Activity No. 2 - Syntax and Semantics
# Task A: Syntax Recognizer   -- only checks if input is valid
# Task B: Semantic Evaluator  -- only computes the value (assumes valid)


text = ""     # the input string
pos = 0       # index of the character we are currently reading


def peek():
    if pos < len(text):
        return text[pos]
    return None


def advance():
    global pos
    ch = peek()
    pos += 1
    return ch



# TASK A -- SYNTAX RECOGNIZER
#VALID OR INVALID(ACCEPTED/REJECTED)


error = ""  # holds the error message if the input is invalid


def recognize_factor():
    """<factor> -> ( <expr> ) | <digit>   -- recursion happens here"""
    global error
    ch = peek()

    if ch == '(':
        advance()                    # consume '('
        recognize_expr()             # <-- recursive call
        if error:
            return
        if peek() == ')':
            advance()                # consume ')'
        else:
            error = f"Invalid syntax: expected ')' at position {pos}"

    elif ch is not None and ch.isdigit():
        advance()                    # consume the digit

    else:
        error = f"Invalid syntax: expected a digit or '(' at position {pos}"


def recognize_term():
    """<term> -> <factor> { (* | /) <factor> }"""
    global error
    recognize_factor()
    if error:
        return
    while peek() in ('*', '/'):
        advance()
        recognize_factor()
        if error:
            return


def recognize_expr():
    """<expr> -> <term> { (+ | -) <term> }
    Calling recognize_term() first is what gives * and / priority."""
    global error
    recognize_term()
    if error:
        return
    while peek() in ('+', '-'):
        advance()
        recognize_term()
        if error:
            return


def is_valid_syntax(input_string):
  
    global text, pos, error
    text = input_string
    pos = 0
    error = ""

    if text == "":
        return False, "Invalid syntax: empty input at position 0"

    recognize_expr()

    if error:
        return False, error
    if pos != len(text):
        return False, f"Invalid syntax: unexpected '{text[pos]}' at position {pos}"

    return True, None


# TASK B -- SEMANTIC EVALUATOR


def eval_factor():
    """<factor> -> ( <expr> ) | <digit>"""
    if peek() == '(':
        advance()                    # consume '('
        value = eval_expr()          # <-- recursive call
        advance()                    # consume ')'
        return value
    else:
        return int(advance())        # consume and convert the digit


def eval_term():
    """<term> -> <factor> { (* | /) <factor> }"""
    value = eval_factor()
    while peek() in ('*', '/'):
        op = advance()
        right = eval_factor()
        value = value * right if op == '*' else value / right
    return value


def eval_expr():
    """<expr> -> <term> { (+ | -) <term> }"""
    value = eval_term()
    while peek() in ('+', '-'):
        op = advance()
        right = eval_term()
        value = value + right if op == '+' else value - right
    return value


def evaluate(input_string):
  
    global text, pos
    text = input_string
    pos = 0
    return eval_expr()


def format_value(value):
   
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    return str(value)


def check_and_evaluate(input_string):
   
    valid, message = is_valid_syntax(input_string)
    if not valid:
        return False, message
    try:
        value = evaluate(input_string)
        return True, value
    except ZeroDivisionError:
        return False, "Invalid: division by zero"


# ---------------------------------------------------------------------
# STRETCH REQUIREMENT: naive left-to-right evaluator using the
# ambiguous grammar  <expr> -> <expr>+<expr> | <expr>*<expr> | <digit>
# ---------------------------------------------------------------------
def naive_left_to_right_eval(s):
    chars = list(s)
    result = int(chars[0])
    i = 1
    while i < len(chars):
        op = chars[i]
        num = int(chars[i + 1])
        if op == '+':
            result += num
        elif op == '-':
            result -= num
        elif op == '*':
            result *= num
        elif op == '/':
            result /= num
        i += 2
    return result


if __name__ == "__main__":
    # Keep reading expressions until the user quits.
    while True:
        user_input = input("Enter an arithmetic expression (or q to quit): ").strip()
        if user_input.lower() in ("q", "quit"):
            print("Goodbye!")
            break

        # Check the syntax before trying to calculate the result.
        valid_a, msg_a = is_valid_syntax(user_input)         # Task A
        if valid_a:
            try:
                value = evaluate(user_input)                  # Task B
                print("Task A: Valid syntax.")
                print(f"Task B: Value = {format_value(value)}")
            except ZeroDivisionError:
                print("Task A: Valid syntax.")
                print("Task B: Invalid -- division by zero")
        else:
            print(f"Task A: {msg_a}")