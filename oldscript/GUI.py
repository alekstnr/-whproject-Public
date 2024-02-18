import sys, gamemain
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont, QIcon

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 820, 600)
        self.setWindowTitle("Warhammer: 40,000 Simulation control Panel")
        self.setWindowIcon(QIcon('icon.png'))

        testbtn = QPushButton("Button", self)
        testbtn.resize(testbtn.sizeHint())
        testbtn.move(100, 100)
        testbtn.clicked.connect(gamemain.deploy(gamemain.playerlist))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
