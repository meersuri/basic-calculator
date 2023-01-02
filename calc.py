import sys

class BasicCalculator:

    _numbers = [str(i) for i in range(10)]
    _ops = ['+', '-']
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
                raise TypeError(f"Invalid character: {input_str[right]}")
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
        raise TypeError(f"Invalid op: {op}")

    def run(self, input_str):
        self._input_str = input_str
        self._tokens = self._tokenize(input_str)
        sub_exprs = self._form_sub_exprs(self._tokens)
        return self._calculate(self._tokens, sub_exprs, 0, len(self._tokens))

if __name__ == '__main__':
    calc = BasicCalculator()
    inp = " -2  +(14 - 330)- 3"
    print(inp)
    out = calc.run(inp)
    print(out)
        
