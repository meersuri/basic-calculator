import unittest

from calc import BasicCalculator as BC

class TestCalculator(unittest.TestCase):

    def test_no_op(self):
        self.assertEqual(1, BC().run("1"))
    
    def test_negation(self):
        self.assertEqual(-1, BC().run("-1"))

    def test_positive(self):
        self.assertEqual(7, BC().run("+7"))

    def test_simple_addition(self):
        self.assertEqual(5, BC().run(" 2 +3"))

    def test_simple_subtraction(self):
        self.assertEqual(-1, BC().run("2- 3"))

    def test_addition_sequential(self):
        self.assertEqual(12, BC().run("2 + 3 + 7"))

    def test_subtraction_sequential(self):
        self.assertEqual(-12, BC().run("-2 - 3 - 7"))

    def test_add_subtract(self):
        exp = "-2+ 3 -7 + 15 -10"
        self.assertEqual(eval(exp), BC().run(exp))

    def test_single_group(self):
        self.assertEqual(3, BC().run("(3)"))

    def test_single_group_negation(self):
        self.assertEqual(-3, BC().run("-(3)"))

    def test_single_group_double_negation(self):
        self.assertEqual(3, BC().run("-(-3)"))

    def test_double_group_nested(self):
        self.assertEqual(3, BC().run("-(-(+3))"))

    def test_grouped_add_subtract(self):
        exp = "-(2+ 3) -(7 + 15) +(-10)"
        self.assertEqual(eval(exp), BC().run(exp))

    def test_grouped_add_subtract_1(self):
        exp = "(-(-(+3-2)+3)-3+1)+3"
        self.assertEqual(eval(exp), BC().run(exp))

    def test_grouped_add_subtract_2(self):
        exp = "(-(3) - (-4) + (-(3-4)+7))"
        self.assertEqual(eval(exp), BC().run(exp))

    def test_grouped_add_subtract_3(self):
        exp = "-1-2+3-(-4-(-5+(-7)+1)-(-(4+1))+3)"
        self.assertEqual(eval(exp), BC().run(exp))

    def test_incomplete_expr_only_op(self):
        with self.assertRaises(RuntimeError):
            BC().run("+")

    def test_incomplete_expr_missing_b(self):
        with self.assertRaises(RuntimeError):
            BC().run("1-2+")

    def test_bad_grouping_missing_close(self):
        with self.assertRaises(RuntimeError):
            BC().run("(1-2+3")

    def test_bad_grouping_missing_close_1(self):
        with self.assertRaises(RuntimeError):
            BC().run("(3+(1-2+(3))")

    def test_bad_grouping_missing_open(self):
        with self.assertRaises(RuntimeError):
            BC().run("(-1))+(1-2+3)")

    def test_invalid_token(self):
        with self.assertRaises(RuntimeError):
            BC().run("(-1))&(1-2+3)")

    def test_invalid_token_1(self):
        with self.assertRaises(RuntimeError):
            BC().run("1+(hello world)")

    def test_missing_operand(self):
        with self.assertRaises(RuntimeError):
            BC().run("-(-3)+")

    def test_missing_operand_1(self):
        with self.assertRaises(RuntimeError):
            BC().run("1+3+-4-7")

    def test_simple_multiply(self):
        self.assertEqual(BC().run("*3"), 0)

    def test_simple_multiply_1(self):
        self.assertEqual(BC().run("2*3"), 6)

    def test_multiply_sequential(self):
        self.assertEqual(BC().run(" 2 *2  *3* 5*1"), 60)

    def test_add_multiply(self):
        inp = "-2 *(2+3)  *3*(5*1+3)"
        self.assertEqual(BC().run(inp), eval(inp))

    def test_simple_add_multiply(self):
        inp = "2+5*3"
        self.assertEqual(BC().run(inp), eval(inp))

    def test_simple_add_multiply_1(self):
        inp = "2+5*3-3*(4-1)+1"
        self.assertEqual(BC().run(inp), eval(inp))

    def test_add_sub_multiply(self):
        inp = "-2 *(2-3*(2))  *3*(5*1-3*(-1-(-4*3)))"
        self.assertEqual(BC().run(inp), eval(inp))

    def test_simple_divide(self):
        self.assertEqual(BC().run("/2"), 0)

    def test_simple_divide_1(self):
        self.assertEqual(BC().run("4/2"), 2)

    def test_simple_divide_flooring(self):
        self.assertEqual(BC().run("4/3"), 1)

    def test_simple_divide_flooring_1(self):
        self.assertEqual(BC().run("10/2/3"), 1)

    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            BC().run("4/0")

    def test_zero_by_zero(self):
        with self.assertRaises(RuntimeError):
            BC().run("0/0")

    def test_simple_divide_seq(self):
        self.assertEqual(BC().run("48/2/3/4"), 2)

    def test_simple_add_divide(self):
        self.assertEqual(BC().run("3/2+48+4"), 53)

    def test_simple_add_divide_1(self):
        self.assertEqual(BC().run("48+3/2+4"), 53)

    def test_simple_divide_negative(self):
        inp = "-3/2"
        eval_inp = inp.replace('/', '//')
        self.assertEqual(eval(eval_inp), BC().run(inp))

    def test_simple_divide_negative_1(self):
        inp = "-3/-2"
        eval_inp = inp.replace('/', '//')
        self.assertEqual(eval(eval_inp), BC().run(inp))

    def test_simple_divide_negative_2(self):
        inp = "-3/(-2)"
        eval_inp = inp.replace('/', '//')
        self.assertEqual(eval(eval_inp), BC().run(inp))

    def test_simple_divide_negative_3(self):
        inp = "1-(-3/2)"
        eval_inp = inp.replace('/', '//')
        self.assertEqual(eval(eval_inp), BC().run(inp))

    def test_simple_divide_negative_4(self):
        inp = "1-(-(3+2)/2)"
        eval_inp = inp.replace('/', '//')
        self.assertEqual(eval(eval_inp), BC().run(inp))

    def test_simple_add_divide_2(self):
        inp = "48+3/2+9/(3+4)+1"
        eval_inp = inp.replace('/', '//')
        self.assertEqual(BC().run(inp), eval(eval_inp))

    def test_all_ops(self):
        inp = "-(-(-4+3*2-5/2)+12/3*(-3)*2-4)"
        eval_inp = inp.replace('/', '//')
        self.assertEqual(BC().run(inp), eval(eval_inp))

    def test_all_ops_1(self):
        inp = "3+(4-(3*(12/(-(4+3/7)+2)-3)/1+2)-4)*2"
        eval_inp = inp.replace('/', '//')
        self.assertEqual(BC().run(inp), eval(eval_inp))

    def test_unary_grouping_mul(self):
        inp = "-3*-4"
        self.assertEqual(BC().run(inp), eval(inp))

    def test_unary_grouping_mul_1(self):
        inp = "-3*-4-4*-2"
        self.assertEqual(BC().run(inp), eval(inp))

    def test_unary_grouping_div(self):
        inp = "-3/-4"
        eval_inp = inp.replace('/', '//')
        self.assertEqual(BC().run(inp), eval(eval_inp))

    def test_unary_grouping_div_1(self):
        inp = "-20/-4/-2/(-4/-(-3/2))"
        eval_inp = inp.replace('/', '//')
        self.assertEqual(BC().run(inp), eval(eval_inp))
