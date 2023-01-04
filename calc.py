import sys

class BasicCalculator:

    _numbers = [str(i) for i in range(10)]
    _ops = ['+', '-', '*', '/']
    _parens = ['(', ')']
    _valid_tokens =  _numbers + _ops + _parens

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
                token = input_str[left: right]
                tokens.append(token)
            tokens.append(input_str[right])
            left, right = right + 1, right + 1

        if left < len(input_str):
            tokens.append(input_str[left:right])

        if not tokens:
            raise RuntimeError(f"Empty expression")

        return tokens

    def _set_op_precedence(self, tokens):
        '''
        3-5*2
        3-(5*2)
        4+(3-5)*(4+5*3)+(2)
        4+((3-5)*(4+5*3))
        4+((3-5)*(4+(5*3)))
        '''
        sub_exprs = self._form_sub_exprs(tokens)
        i = 1
        while i < len(tokens) - 1:
            if self._is_op(tokens[i]):
                i += 1
                continue
            if i == '(':
                sub_end = sub_exprs[i]
                if sub_end + 1 >= len(tokens):
                    i += 1
                    continue
                right = sub_end + 1
            else:
                right = i + 1
            left = i - 1
            if not (tokens[left] in ['+', '-'] and tokens[right] in ['*', '/']):
                i += 1
                continue
            if right + 1 in sub_exprs:
                next_right = sub_exprs[right + 1]
            else:
                next_right = right + 2
            tokens.insert(next_right, ')')
            tokens.insert(i, '(')
            i = 1
            sub_exprs = self._form_sub_exprs(tokens)

        return tokens
        
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
            if tokens[i] == '(':
                res = self._calculate(tokens, sub_exprs, i + 1, sub_exprs[i])
                i = sub_exprs[i] + 1
                continue
            if self._is_number(tokens[i]):
                res = self._eval_op('+', tokens[i], 0)
                i += 1
                continue
            op = tokens[i]
            if i + 1 == right:
                raise RuntimeError(f"Incomplete expression at idx: {i}, expected operand")
            if tokens[i + 1] == '(':
                b = self._calculate(tokens, sub_exprs, i + 2, sub_exprs[i + 1])
                i = sub_exprs[i + 1] + 1
            else:
                self._ensure_is_number(tokens[i + 1], i + 1)
                b = tokens[i + 1]
                i += 2
            res = self._eval_op(op, res, b)
                
        return res

    def _ensure_is_op(self, token, idx):
        if token not in BasicCalculator._ops:
            raise RuntimeError(f"Invalid token at idx: {idx}, expected operator, but got: {token}")

    def _ensure_is_number(self, token, idx):
        if token in BasicCalculator._parens or token in BasicCalculator._ops:
            raise RuntimeError(f"Invalid token at idx: {idx}, expected number, but got: {token}")

    def _is_number(self, token):
        return all(x in BasicCalculator._numbers for x in token)

    def _is_op(self, token):
        return token in self._ops

    def _form_sub_exprs(self, tokens):
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
        print(''.join(self._tokens))
        self._tokens = self._set_op_precedence(self._tokens)
        print(''.join(self._tokens))
        sub_exprs = self._form_sub_exprs(self._tokens)
        return self._calculate(self._tokens, sub_exprs, 0, len(self._tokens))

if __name__ == '__main__':
    calc = BasicCalculator()
    if len(sys.argv) > 1:
        inp = sys.argv[1]
    else:
        inp = " -2  +(14 - 330)- 3"
    print(f"Input: {inp}")
    print(f"Result: {calc.run(inp)}")
        
