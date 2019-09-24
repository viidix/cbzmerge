#Copyright (C) 2019 Luca Dessì
#
#Author: Luca Dessì
#
#This file is part of cbzmerge.
#
#cbzmerge is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#cbzmerge is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Nome-Programma.  If not, see http://www.gnu.org/licenses/

from cbzmerge_core import *
from cbzmerge_MainWindow import Ui_MainWindow
from PySide2 import QtCore, QtGui, QtWidgets
import sys, os, traceback

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

    def btnAdd_clicked(self):
        fname, f = QtWidgets.QFileDialog.getOpenFileNames(None, '', '', "cbz (*.cbz);;All files (*.*)")
        if fname != '' and f != '':
            self.ui.listAdded.addItems(fname)
            self.ui.btnMerge.setEnabled(True)
            self.ui.btnRemoveAll.setEnabled(True)
               
    def btnRemove_clicked(self):
        selected = [item.text() for item in self.ui.listAdded.selectedItems()]
        for item in self.ui.listAdded.selectedItems():
            self.ui.listAdded.takeItem(self.ui.listAdded.row(item))
        if self.ui.listAdded.count() == 0:
            self.ui.btnMerge.setEnabled(False)
            self.ui.btnRemoveAll.setEnabled(False)
                       
    def btnRemoveAll_clicked(self):
        self.ui.listAdded.clear()
        self.ui.btnMerge.setEnabled(False)
        self.ui.btnRemoveAll.setEnabled(False)
        
    def btnMerge_clicked(self):
        fname, f = QtWidgets.QFileDialog.getSaveFileName(None, '', '', "cbz (*.cbz);;All files (*.*)")
        if fname != '' and f != '':
            if f == "cbz (*.cbz)" and fname[-4:] != ".cbz":
                fname = fname + ".cbz"
            filelist = []
            for i in range(self.ui.listAdded.count()):
                filelist.append(self.ui.listAdded.item(i).text())
            
            self.statusBar().showMessage('Merging')
            newcbz = cbzunite(filelist)
            try:
                newcbz.MergeCBZ(fname, self.ui.progressBar.setValue)
                self.statusBar().showMessage('Finished')
            except:
                tb = traceback.format_exc()
                error_msg = QtWidgets.QMessageBox(self)
                error_msg.setIcon(QtWidgets.QMessageBox.Critical)
                error_msg.setWindowTitle("Error")
                error_msg.setText("Something went wrong")
                error_msg.setDetailedText(tb)
                error_msg.exec_()

                self.statusBar().showMessage('Error')
            
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            for url in event.mimeData().urls():
                if os.path.isdir(str(url.toLocalFile())):
                    event.ignore()
                else:
                    event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        fname = [str(u.toLocalFile()) for u in event.mimeData().urls()]
        self.ui.listAdded.addItems(fname)
        self.ui.btnMerge.setEnabled(True)
        self.ui.btnRemoveAll.setEnabled(True)
        
    def selectionChanged(self):
        if len(self.ui.listAdded.selectedItems()) != 0:
            self.ui.btnRemove.setEnabled(True)
        else:
            self.ui.btnRemove.setEnabled(False)
            
    def showAbout(self):
        about = QtWidgets.QMessageBox(self)
        about.setIconPixmap(QtGui.QPixmap("icon64.png"))
        about.setWindowTitle("cbzmerge")
        about.setText('<h3>cbzmerge</h3> <p>Simple GUI program to merge multiple *.cbz file into a single file</p> <p>Version: 0.1.5<p> <p>Author: Luca Dessì <a href="mailto:luca.dessi.92@gmail.com">luca.dessi.92@gmail.com</a></p> <p>Website: <a href="https://github.com/viidix/cbzmerge">https://github.com/viidix/cbzmerge</a></p> <h4>Copyright &copy; 2019 Luca Dessì</h4> <p>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p> <p>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p> <p>You should have received a copy of the GNU General Public License along with this program.  If not, see <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a>.</p>')
        about.exec_()

    def showAboutQt(self):
        QtWidgets.QMessageBox.aboutQt(self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
