import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QScreen
from PyQt5.QtCore import Qt, QLocale, QTranslator
from ui.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)

    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    else:
        app_path = os.path.dirname(__file__)
    
    locale = QLocale.system().name()
    app_locale = os.path.join(app_path, 'locale/libro2_' + locale + '.qm')
    qt_locale = os.path.join(app_path, 'locale/qtbase_' + locale + '.qm')
    
    if sys.platform == 'win32':
        app_font = QFont('Segoe UI', 9)
        QApplication.setFont(app_font)

    app_translator = QTranslator()
    qt_translator = QTranslator()
    app_translator.load(app_locale)
    qt_translator.load(qt_locale)
    app.installTranslator(app_translator)
    app.installTranslator(qt_translator)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())

if (__name__ == '__main__'):
    main()