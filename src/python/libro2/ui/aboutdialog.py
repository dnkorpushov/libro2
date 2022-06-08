import webbrowser
from PyQt5.QtWidgets import QDialog
from .aboutdialog_ui import Ui_AboutDialog


class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)

    def openLink(self, link):
        browser = webbrowser.get()
        browser.open_new_tab(link)