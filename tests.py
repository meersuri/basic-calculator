import unittest

from calc import BasicCalculator as BC

class TestCalculator(unittest.TestCase):

    def test_no_op(self):
        self.assertTrue(1, BC().run("1"))
    
    def test_negation(self):
        self.assertTrue(-1, BC().run("-1"))

    def test_positive(self):
        self.assertTrue(7, BC().run("+7"))

    def test_simple_addition(self):
        self.assertTrue(5, BC().run(" 2 +3"))

    def test_simple_subtraction(self):
        self.assertTrue(-1, BC().run("2- 3"))

    def test_addition_sequential(self):
        self.assertTrue(12, BC().run("2 + 3 + 7"))

    def test_subtraction_sequential(self):
        self.assertTrue(-12, BC().run("-2 - 3 - 7"))

    def test_add_subtract(self):
        exp = "-2+ 3 -7 + 15 -10"
        self.assertTrue(eval(exp), BC().run(exp))

    def test_single_group(self):
        self.assertTrue(3, BC().run("(3)"))

    def test_single_group_negation(self):
        self.assertTrue(-3, BC().run("-(3)"))

    def test_single_group_double_negation(self):
        self.assertTrue(3, BC().run("-(-3)"))

    def test_double_group_nested(self):
        self.assertTrue(3, BC().run("-(-(+3))"))

    def test_grouped_add_subtract(self):
        exp = "-(2+ 3) -(7 + 15) +(-10)"
        self.assertTrue(eval(exp), BC().run(exp))

    def test_grouped_add_subtract_1(self):
        exp = "(-(-(+3-2)+3)-3+1)+3"
        self.assertTrue(eval(exp), BC().run(exp))

    def test_grouped_add_subtract_2(self):
        exp = "(-(3) - (-4) + (-(3-4)+7))"
        self.assertTrue(eval(exp), BC().run(exp))
