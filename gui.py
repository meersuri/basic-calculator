import sys
from calc import BasicCalculator
from PySide2 import QtCore, QtWidgets, QtGui

class BasicCalc(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.bc = BasicCalculator()
        self.height, self.width = 600, 800

        self.text_input = TextInput()
        self.button_input = ButtonInput()

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.text_input)
        self.layout.addWidget(self.button_input)

        self.button_input.oppad.ops['equals'].clicked.connect(self.equals_clicked)
        self.text_input.input.returnPressed.connect(self.equals_clicked)
        for i, number in enumerate(self.button_input.numpad.numbers):
            number.clicked.connect(self.number_clicked)
        for name, op in self.button_input.oppad.ops.items():
            if name == 'equals':
                continue
            op.clicked.connect(self.op_clicked)
        self.setWindowTitle("BasicCalculator")

        self.resize(self.width, self.height)

    def equals_clicked(self):
        try:
            out = self.bc.run(self.text_input.input.text())
        except Exception as e:
            self.text_input.input.setText(str(e))
        else:
            self.text_input.input.setText(str(out))

    def number_clicked(self):
        num = self.sender().text()
        inp = self.text_input.input.text()
        self.text_input.input.setText(inp + num)

    def op_clicked(self):
        op = self.sender().text()
        inp = self.text_input.input.text()
        self.text_input.input.setText(inp + op)

class TextInput(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.input = QtWidgets.QLineEdit()
        self.input.setClearButtonEnabled(True)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.input)

class ButtonInput(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.numpad = NumberInput()
        self.oppad = OperatorInput()

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.numpad)
        self.layout.addWidget(self.oppad)

class OperatorInput(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ops = {}
        ops = [('plus','+'), ('minus','-'), ('equals', '=')]
        for name, symbol in ops:
            self.ops[name] = QtWidgets.QPushButton(symbol)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        for op in self.ops.values():
            self.layout.addWidget(op)

class NumberInput(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.numbers = [QtWidgets.QPushButton(str(i)) for i in range(10)]

        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        i = 1
        while i < 10:
            number = self.numbers[i]
            idx = i - 1
            self.layout.addWidget(number, 2 - idx//3, idx - (idx//3)*3)
            i += 1
        self.layout.addWidget(self.numbers[0], 3, 0, columnSpan=3)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    calc = BasicCalc()
    calc.show()
    sys.exit(app.exec_())
