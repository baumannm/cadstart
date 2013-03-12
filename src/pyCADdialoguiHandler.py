#######################################################
#
# Dialog UI
#
#######################################################

from PySide import QtGui, QtCore
from pyCADdialogui import Ui_Dialog as Dlg

class AskDialog(QtGui.QDialog, Dlg): 
    
    status = False
    
    # Constructor
    def __init__(self): 
        
        QtGui.QDialog.__init__(self) 
        self.setupUi(self)
        
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.doAccept)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.doReject)
  

    def setText(self, text):
        
        self.label.setText(text)
        
        return
    
    def setURL(self, URL):
        self.webView.setUrl(URL)
    
    def doAccept(self):
    
        self.status = True
        
        print("OK")
        
        return
    
    def doReject(self):
        
        self.status = False
        
        print("cancel")
        
        return
    
    def getStatus(self):
        
        return self.status
