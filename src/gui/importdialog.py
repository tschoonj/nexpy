"""
Base class for import dialogs
"""
import os
from IPython.external.qt import QtCore, QtGui

from nexpy.api.nexus import *

filetype = "Text File" #Defines the Import Menu label

class BaseImportDialog(QtGui.QDialog):
    """Base dialog class for NeXpy import dialogs"""
 
    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent)
        self.accepted = False 

    def filebox(self):
        """
        Creates a text box and button for selecting a file.
        """
        self.filebutton =  QtGui.QPushButton("Choose File")
        self.filebutton.clicked.connect(self.choose_file)
        self.filename = QtGui.QLineEdit(self)
        self.filename.setMinimumWidth(300)
        filebox = QtGui.QHBoxLayout()
        filebox.addWidget(self.filebutton)
        filebox.addWidget(self.filename)
        return filebox
 
    def directorybox(self):
        """
        Creates a text box and button for selecting a directory.
        """
        self.directorybutton =  QtGui.QPushButton("Choose Directory")
        self.directorybutton.clicked.connect(self.choose_directory)
        self.directoryname = QtGui.QLineEdit(self)
        self.directoryname.setMinimumWidth(300)
        directorybox = QtGui.QHBoxLayout()
        directorybox.addWidget(self.directorybutton)
        directorybox.addWidget(self.directoryname)
        return directorybox

    def buttonbox(self):
        """
        Creates a box containing the standard Cancel and OK buttons.
        """
        buttonbox = QtGui.QDialogButtonBox(self)
        buttonbox.setOrientation(QtCore.Qt.Horizontal)
        buttonbox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|
                                          QtGui.QDialogButtonBox.Ok)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        return buttonbox

    def choose_file(self):
        """
        Opens a file dialog and sets the file text box to the chosen path.
        """
        filename, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open File',
            os.path.expanduser('~'))
        self.filename.setText(str(filename))

    def get_filename(self):
        """
        Returns the selected file.
        """
        return self.filename.text()

    def choose_directory(self):
        """
        Opens a file dialog and sets the directory text box to the chosen path.
        """
        dir = QtGui.QFileDialog.getExistingDirectory(self, 'Choose Directory',
            dir=os.path.expanduser('~'))
        self.directoryname.setText(str(dir))

    def get_directory(self):
        """
        Returns the selected directory
        """
        return self.directoryname.text()

    def get_filesindirectory(self):
        """
        Returns a list of files in the selected directory.
        
        The files are sorted using a natural sort algorithm that preserves the
        numeric order when a file name consists of text and index so that, e.g., 
        'data2.tif' comes before 'data10.tif'.
        """
        os.chdir(self.get_directory())
        filenames = os.listdir(os.getcwd())
        return sorted(filenames,key=natural_sort)

    def accept(self):
        """
        Completes the data import.
        """
        self.accepted = True
        from nexpy.gui.consoleapp import _mainwindow
        _mainwindow.import_data()
        QtGui.QDialog.accept(self)
        
    def reject(self):
        """
        Cancels the data import.
        """
        self.accepted = False
        QtGui.QDialog.reject(self)

def natural_sort(key):
    import re
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', key)]    
