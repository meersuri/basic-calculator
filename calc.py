import sys


class BasicCalculator:

    _numbers = [str(i) for i in range(10)]
    _ops = ['+', '-', '*', '/']
    _parens = ['(', ')']
    _valid_tokens = _numbers + _ops + _parens

    _precedence_rules = {
        ('+', '*'): '*',
        ('-', '*'): '*',
        ('+', '/'): '/',
        ('-', '/'): '/',
    }

    def __init__(self):
        self._input_str = ""

    def _tokenize(self, input_str):
        input_str = input_str.replace(' ', '')
        tokens = []
        left, right = 0, 0
        while right < len(input_str):
            if input_str[right] not in BasicCalculator._valid_tokens:
                raise RuntimeError(f"Invalid character: {input_str[right]}")
            if input_str[right] in BasicCalculator._numbers:
                right += 1
                continue
            if right > left:
                token = input_str[left:right]
                tokens.append(token)
            tokens.append(input_str[right])
            left, right = right + 1, right + 1

        if left < len(input_str):
            tokens.append(input_str[left:right])

        if not tokens:
            raise RuntimeError(f"Empty expression")

        return tokens

    def _set_op_precedence(self, tokens):
        self._set_unary_op_precedence(tokens)
        self._set_binary_op_precedence(tokens)
        return tokens

    def _set_unary_op_precedence(self, tokens):
        if len(tokens) <= 1:
            return tokens

        tokens = self._handle_exp_starts_with_plus_minus(tokens)
        tokens = self._handle_sub_expr_starts_with_plus_minus(tokens)
        tokens = self._handle_mul_div_followed_by_plus_minus(tokens)
        tokens = self._handle_successive_plus_minus(tokens)
        return tokens

    def _handle_exp_starts_with_plus_minus(self, tokens):

        sub_exprs = self._find_sub_exprs(tokens)
        if tokens[0] in ['+', '-']:
            next_idx = self._get_next_idx(tokens, sub_exprs, 1)
            tokens.insert(next_idx, ')')
            tokens.insert(0, '(')

        return tokens

    def _handle_sub_expr_starts_with_plus_minus(self, tokens):
        i = 0
        sub_exprs = self._find_sub_exprs(tokens)
        while i < len(tokens) - 1:
            if tokens[i] != '(':
                i += 1
                continue
            if tokens[i + 1] not in ['+', '-']:
                i += 1
                continue
            self._ensure_is_sub_expr(tokens[i + 2], i + 2)
            next_idx = self._get_next_idx(tokens, sub_exprs, i + 2)
            if tokens[next_idx] == ')':
                i += 1
                continue

            tokens.insert(next_idx, ')')
            tokens.insert(i, '(')

            sub_exprs = self._find_sub_exprs(tokens)
            i = 0

        return tokens

    def _handle_mul_div_followed_by_plus_minus(self, tokens):
        i = 0
        sub_exprs = self._find_sub_exprs(tokens)
        while i < len(tokens) - 1:
            if tokens[i] not in ['*', '/']:
                i += 1
                continue
            if tokens[i + 1] not in ['+', '-']:
                i += 1
                continue
            self._ensure_is_sub_expr(tokens[i + 2], i + 2)
            next_idx = self._get_next_idx(tokens, sub_exprs, i + 2)

            tokens.insert(next_idx, ')')
            tokens.insert(i + 1, '(')

            sub_exprs = self._find_sub_exprs(tokens)
            i = 0

        return tokens

    def _handle_successive_plus_minus(self, tokens):
        i = 0
        sub_exprs = self._find_sub_exprs(tokens)
        while i < len(tokens) - 1:
            if tokens[i] not in ['+', '-']:
                i += 1
                continue
            if tokens[i + 1] not in ['+', '-']:
                i += 1
                continue
            self._ensure_is_sub_expr(tokens[i + 2], i + 2)
            next_idx = self._get_next_idx(tokens, sub_exprs, i + 2)

            tokens.insert(next_idx, ')')
            tokens.insert(i + 1, '(')

            sub_exprs = self._find_sub_exprs(tokens)
            i = 0

        return tokens

    def _set_binary_op_precedence(self, tokens):
        '''
        3-5*2
        3-(5*2)
        4+(3-5)*(4+5*3)+(2)
        4+((3-5)*(4+5*3))
        4+((3-5)*(4+(5*3)))

        (.. 3)-5*2
        ((.. 3)-5)*2
        '''
        sub_exprs = self._find_sub_exprs(tokens)
        i = 1
        while i < len(tokens) - 1:
            prev_idx = i - 1
            next_idx = self._get_next_idx(tokens, sub_exprs, i)
            if next_idx >= len(tokens):
                i += 1
                continue
            if not (self._is_sub_expr(tokens[i]) and self._is_op(
                    tokens[prev_idx]), self._is_op(tokens[next_idx])):
                i += 1
                continue

            op_pair = (tokens[prev_idx], tokens[next_idx])
            winner = BasicCalculator._precedence_rules.get(op_pair, op_pair[0])
            if winner == op_pair[0]:
                i += 1  # matches default left->right order
                continue

            # insert explicit parens to change ordering
            next_next_idx = self._get_next_idx(tokens, sub_exprs, next_idx + 1)
            tokens.insert(next_next_idx, ')')
            tokens.insert(i, '(')
            i = 1
            sub_exprs = self._find_sub_exprs(tokens)

        return tokens

    def _get_next_idx(self, tokens, sub_exprs, idx):
        if tokens[idx] == '(':
            return sub_exprs[idx] + 1
        return idx + 1

    def _calculate(self, tokens, sub_exprs, left, right):
        '''
        2+3-1
        -2+(5-(3+4)-1)
        -(3+4)
        (3+4)
        '''
        assert right - left >= 1

        i = left
        res = 0
        while i < right:
            if self._is_sub_expr(tokens[i]):
                res, i = self._calc_sub_expr(tokens, sub_exprs, i)
                continue

            op = tokens[i]
            if i + 1 == right:
                raise RuntimeError(
                    f"Incomplete expression at idx: {i}, expected operand")
            b, i = self._calc_sub_expr(tokens, sub_exprs, i + 1)
            res = self._eval_op(op, res, b)

        return res

    def _calc_sub_expr(self, tokens, sub_exprs, idx):
        if tokens[idx] == '(':
            end_idx = sub_exprs[idx] + 1
            res = self._calculate(tokens, sub_exprs, idx + 1, sub_exprs[idx])
            next_idx = sub_exprs[idx] + 1
        else:
            self._ensure_is_number(tokens[idx], idx)
            res = self._eval_op('+', tokens[idx], 0)
            next_idx = idx + 1

        return res, next_idx

    def _ensure_is_op(self, token, idx):
        if token not in BasicCalculator._ops:
            raise RuntimeError(
                f"Invalid token at idx: {idx}, expected operator, but got: {token}"
            )

    def _ensure_is_sub_expr(self, token, idx):
        if self._is_number(token):
            return
        if token not in ['('] + BasicCalculator._numbers:
            raise RuntimeError(
                f"Invalid token at idx: {idx}, expected `(` or number, but got: {token}"
            )

    def _ensure_is_number(self, token, idx):
        if token in BasicCalculator._parens or token in BasicCalculator._ops:
            raise RuntimeError(
                f"Invalid token at idx: {idx}, expected number, but got: {token}"
            )

    def _is_sub_expr(self, token):
        return token == '(' or self._is_number(token)

    def _is_number(self, token):
        return all(x in BasicCalculator._numbers for x in token)

    def _is_op(self, token):
        return token in self._ops

    def _find_sub_exprs(self, tokens):
        sub_exprs = {}
        starts = []
        for i, x in enumerate(tokens):
            if x == '(':
                starts.append(i)
            elif x == ')':
                if not starts:
                    raise RuntimeError(f"Unmatched ')' at idx: {i}")
                left = starts.pop()
                sub_exprs[left] = i
            else:
                pass

        if starts:
            raise RuntimeError(f"Unmatched '(' at idx: {starts[-1]}")

        return sub_exprs

    def _eval_op(self, op, a, b):
        if op == '+':
            return int(a) + int(b)
        if op == '-':
            return int(a) - int(b)
        if op == '*':
            return int(a) * int(b)
        if op == '/':
            x, y = int(a), int(b)
            if y == 0 and x != 0:
                raise ZeroDivisionError("Divide by zero")
            if y == 0 and x == 0:
                raise RuntimeError(f"Undefined")
            return int(a) // int(b)
        raise RuntimeError(f"Invalid op: {op}")

    def run(self, input_str):
        self._input_str = input_str
        self._tokens = self._tokenize(input_str)
        self._tokens = self._set_op_precedence(self._tokens)
        print(''.join(self._tokens))
        sub_exprs = self._find_sub_exprs(self._tokens)
        return self._calculate(self._tokens, sub_exprs, 0, len(self._tokens))


if __name__ == '__main__':
    calc = BasicCalculator()
    if len(sys.argv) > 1:
        inp = sys.argv[1]
    else:
        inp = " -2  +(14 - 330)- 3"
    print(f"Input: {inp}")
    print(f"Result: {calc.run(inp)}")
