import sys
from PyQt5.QtCore import pyqtSignal, QEvent,Qt,QCoreApplication 
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow,QSystemTrayIcon, QMenu, QApplication, QAction, QMessageBox
from form import Ui_Form
from MainThread import *
import time


class Main(QMainWindow, Ui_Form):
    def __init__(self):
        # initialize all essential object in GUI
        super().__init__()
        self.setupUi(self)
        self.started = False
        self.setWindowIcon(QIcon("icon.png") )
        title = 'ASDA Spirt Program'
        self.setWindowTitle(title)
        self.plainTextEdit.setMaximumBlockCount(60*24)
        self.trayicon = QSystemTrayIcon(QIcon('icon.png'),parent=app)
        self.trayicon.setToolTip(title)
        self.trayicon.show()
        menu =  QMenu()
        openaxtion = menu.addAction('Open')
        exitaxtion = menu.addAction('Exit')     
        openaxtion.triggered.connect(lambda x: self.show())
        exitaxtion.triggered.connect(lambda x: QCoreApplication.exit(0))
        self.trayicon.setContextMenu(menu)

        self.display_thread = DisplayThread()
        self.display_thread.data.connect(self.set_data)
        self.display_thread.exceptions.connect(self.set_exception)
        self.display_thread.start()

    def set_data(self, data):
        # self the value of GUI label of Weight
        text = ""
        for i in range(len(data)):
            text += str(data[i])+"\t"
        self.plainTextEdit.appendPlainText(text)
        
    
    def set_exception(self, first,second):
        # self the value of GUI label of Weight
        text = str(first) + str(second)
        self.plainTextEdit.appendPlainText(text)
 

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.ignore()
                self.close()
                return

        super(Main, self).changeEvent(event)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.trayicon.showMessage('Running', 'Running in the background.')


if __name__ == "__main__":
    import os
    # os.system("python -m PyQt5.uic.pyuic -x .\\form.ui -o .\\form.py")
    app = QApplication(sys.argv)
    the_window = Main()
    the_window.show()
    sys.exit(app.exec_())