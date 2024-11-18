import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QTextEdit, QVBoxLayout,
                             QPushButton, QWidget, QHBoxLayout, QGridLayout, QLabel)
from PyQt5.QtCore import Qt


class CNCInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CNC Interface')
        self.setGeometry(100, 100, 400,300)

        # TextEdit for displaying G-code
        self.textEdit = QTextEdit(self)

        # Load G-code button
        loadButton = QPushButton('Load G-code', self)
        loadButton.clicked.connect(self.loadGcode)

        # Control buttons
        homeButton = QPushButton('Home', self)
        homeButton.clicked.connect(self.homePosition)

        setButton = QPushButton('Set', self)
        setButton.clicked.connect(self.setPosition)

        # Directional buttons
        upButton = QPushButton('↑', self)
        upButton.clicked.connect(self.moveUp)

        downButton = QPushButton('↓', self)
        downButton.clicked.connect(self.moveDown)

        leftButton = QPushButton('←', self)
        leftButton.clicked.connect(self.moveLeft)

        rightButton = QPushButton('→', self)
        rightButton.clicked.connect(self.moveRight)

        # Layout for directional buttons
        grid = QGridLayout()
        grid.addWidget(upButton, 0, 1)
        grid.addWidget(leftButton, 1, 0)
        grid.addWidget(rightButton, 1, 2)
        grid.addWidget(downButton, 2, 1)

        # Layout for control buttons
        hbox = QHBoxLayout()
        hbox.addWidget(homeButton)
        hbox.addWidget(setButton)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(loadButton)
        layout.addWidget(self.textEdit)
        layout.addLayout(grid)
        layout.addLayout(hbox)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def loadGcode(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open G-code File", "", "G-code Files (*.gcode);;All Files (*)",
                                                  options=options)
        if fileName:
            with open(fileName, 'r') as file:
                self.textEdit.setText(file.read())

    def homePosition(self):
        # Logic to move the CNC to the home position
        print("Moving to home position")

    def setPosition(self):
        # Logic to set the current position
        print("Setting current position")

    def moveUp(self):
        # Logic to move the CNC up
        print("Moving up")

    def moveDown(self):
        # Logic to move the CNC down
        print("Moving down")

    def moveLeft(self):
        # Logic to move the CNC left
        print("Moving left")

    def moveRight(self):
        # Logic to move the CNC right
        print("Moving right")


def main():
    app = QApplication(sys.argv)
    mainWin = CNCInterface()
    mainWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
