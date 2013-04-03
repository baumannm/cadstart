#######################################################
#
# Help UI
#
#######################################################
import os 
import conf
import webbrowser
import pyCADdialoguiHandler
import pathUtils as pu
from PySide            import QtGui, QtCore
from pyCADhelpui        import Ui_Dialog as Dlg

class HelpDialog(QtGui.QDialog, Dlg): 
    

    
    # Constructor
    def __init__(self, CADversions): 
        
        QtGui.QDialog.__init__(self) 
        self.setupUi(self)

        # Slots
        self.connect(self.helpCADde, QtCore.SIGNAL("clicked()"), self.onCADde)
        self.connect(self.helpFAQ, QtCore.SIGNAL("clicked()"), self.onFAQ)
        self.connect(self.helpCADSkript, QtCore.SIGNAL("clicked()"), self.onCADSkript)
        self.connect(self.helpPDMSkript, QtCore.SIGNAL("clicked()"), self.onPDMSkript)
        self.connect(self.helpCADUebungen, QtCore.SIGNAL("clicked()"), self.onCADUebungen)
        self.connect(self.helpIPEKhp, QtCore.SIGNAL("clicked()"), self.onIPEKhp)
        self.connect(self.helpPDMhelp, QtCore.SIGNAL("clicked()"), self.onPDMhelp)
        self.connect(self.helpProHelp, QtCore.SIGNAL("clicked()"), self.onProHelp)
        self.connect(self.helpScreencasts, QtCore.SIGNAL("clicked()"), self.onScreencasts)
        self.connect(self.helpMovies, QtCore.SIGNAL("clicked()"), self.onMovies)
        self.connect(self.helpOffice, QtCore.SIGNAL("clicked()"), self.onOffice)
        
        self.CADversions = CADversions
        
    def onCADde(self):
        
        webbrowser.open(conf.caddeURL)
        
        return
    
    def onFAQ(self):
        
        webbrowser.open(conf.faqURL)
        
        return

    def onScreencasts(self):
        
        webbrowser.open(conf.screencastURL)
        
        return

    def onCADSkript(self):
        
        webbrowser.open(conf.cadSkriptURL)
        
        return
        
    def onPDMSkript(self):
        
        webbrowser.open(conf.pdmSkriptURL)
        
        return
        
    def onCADUebungen(self):
        
        webbrowser.open(conf.cadUebungenURL)
        
        return        
    
    def onIPEKhp(self):
        
        webbrowser.open(conf.cadURL)
        
        return

    def onMovies(self):
        
        webbrowser.open(conf.movieURL)
        
        return
    
    def onOffice(self):
        
        webbrowser.open(conf.officeURL)
        
        return    
    
    def onPDMhelp(self):
        
        webbrowser.open(conf.pdmHelpURL)
        
        return
    
    def onProHelp(self):
        # TODO: Helpcenter in Creo. Path???
        noHelp = True
        for i in self.CADversions:
            
            pathDE = pu.normPath(i.installdir + "\\html\\german\\proe\\default.htm")
            pathEN = pu.normPath(i.installdir + "\\html\\usascii\\proe\\default.htm")
            
            if os.path.exists(pathDE):
                
                os.system(pu.spacePath(pathDE))
                noHelp = False
                
                return
                
            if os.path.exists(pathEN):
                
                os.system(pu.spacePath(pathEN))
                noHelp = False
                
                return
            
        if noHelp:
            
            # dialog instance
            dialog = pyCADdialoguiHandler.AskDialog()
            
            dialog.setText("Hinweis:")
            dialog.setURL(pu.textURL("noprohelp"))
            
            # dialog modal show
            dialog.exec_()

        return
