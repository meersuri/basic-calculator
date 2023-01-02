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

        self.button_input.oppad.equals.clicked.connect(self.equals_clicked)
        self.text_input.input.returnPressed.connect(self.equals_clicked)

        self.setWindowTitle("BasicCalculator")
        self.resize(self.width, self.height)

    def equals_clicked(self):
        try:
            out = self.bc.run(self.text_input.input.text())
        except RuntimeError as e:
            self.text_input.input.setText(str(e))
        else:
            self.text_input.input.setText(str(out))

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
        self.equals = QtWidgets.QPushButton("=")

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.equals)

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
