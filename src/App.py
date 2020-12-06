import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton , QLabel, QWidget, QLineEdit, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import numpy as np
import random
import copy

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'Jacobson'
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.createGridLayout()
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.show()
    
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()

        self.values = np.arange(7*7, dtype=QLineEdit).reshape(7,7)
        self.b = np.arange(7,dtype=QLineEdit)

        viewColIndex = 0
        for row in range(7):
            for col in range(7):
                text = QLineEdit(str(random.randint(1, 9)))
                if row == col:
                    text.setText(str(random.randint(40, 90)))
                text.setFixedWidth(40)
                label = QLabel("x" + str(col+1))
                label.setFixedWidth(20)
                layout.addWidget(text, row, viewColIndex)
                viewColIndex += 1
                layout.addWidget(label, row, viewColIndex)
                viewColIndex += 1
                self.values[row][col] = text
            b = QLineEdit(str(random.randint(1, 100)))
            b.setFixedWidth(40)
            layout.addWidget(b, row, viewColIndex+1)
            layout.addWidget(QLabel("="), row, viewColIndex)
            self.b[row] = b
            viewColIndex = 0
        self.precision = QLineEdit("0.0000000001")
        precisionLabel = QLabel("Precision")
        
        runButton = QPushButton("Run")
        runButton.setFixedWidth(40)
        runButton.clicked.connect(self.run)
        layout.addWidget(runButton, 7, 15)
        layout.addWidget(self.precision, 7, 10, 1, 3)
        layout.addWidget(precisionLabel, 7, 8, 1, 2)

        self.horizontalGroupBox.setLayout(layout)
        
    def run(self):
        matrix = np.arange(7*7, dtype=float).reshape(7,7)
        b = np.arange(7, dtype=float)
        for row in range(7):
            b[row] = int(self.b[row].text())
            for col in range(7):
                matrix[row][col] = float(self.values[row][col].text())
        msgBox = QMessageBox()
        msgBox.setText(str(self.solve(matrix, b, np.zeros(len(b)), float(self.precision.text()))))
        msgBox.setWindowTitle("Result")
        msgBox.setFixedWidth(1000)
        msgBox.exec()

    def solve(self, matrix, results, guess, epsilon):
        diagonal = np.diag(np.diag(matrix))
        lowerAndUpper =  matrix - diagonal
        diagonalInverse = np.diag(1/np.diag(diagonal))
        x = copy.deepcopy(guess)
        for _ in range(500):
            current = np.dot(diagonalInverse, results - np.dot(lowerAndUpper, x))
            if np.linalg.norm(current - x) < epsilon:
                return current
            x = copy.deepcopy(current)
        return x

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())