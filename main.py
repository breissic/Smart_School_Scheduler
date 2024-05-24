import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMenu
from Menu import Menu


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())
