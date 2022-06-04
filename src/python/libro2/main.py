import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.mainwindow import MainWindow


def main():
    # if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    #     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    #     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())

if (__name__ == '__main__'):
    main()