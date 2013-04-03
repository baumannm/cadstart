#######################################################
#
# UI
#
#######################################################

import conf
import pyDefStart
import pyCADhelpuiHandler
import pyCADdialoguiHandler
import webbrowser
import PySide.QtNetwork
import pyCADticker
import pyCADfeedbackFormuiHandler
import pyCADutils
import os
import re
import envUtils as eu
import urllib

import pathUtils as pu

from PySide              import QtGui, QtCore

from pyCADui            import Ui_Dialog as Dlg

class StartDialog(QtGui.QDialog, Dlg): 
    
    desclist = []
    aero = True
    graphics = ""
    currItem = 0
    CADversions = 0
    mac = ""
    
        
    # Constructor
    def __init__(self, CADversions, options): 
        
        QtGui.QDialog.__init__(self) 
        self.setupUi(self)

        # Slots
        self.connect(self.buttonStart, QtCore.SIGNAL("clicked()"), self.onStart)
        self.connect(self.proList, QtCore.SIGNAL("currentIndexChanged(int)"), self.onSelect)
        self.connect(self.openMailtoCAD, QtCore.SIGNAL("clicked()"), self.onMailto)
        self.connect(self.openRSSFeed, QtCore.SIGNAL("clicked()"), self.onRSS)
        self.connect(self.openHelp, QtCore.SIGNAL("clicked()"), self.onHelp)
        self.connect(self.buttonVPN, QtCore.SIGNAL("clicked()"), self.onVPN)
        self.connect(self.buttonTest, QtCore.SIGNAL("clicked()"), self.onTest)
        self.connect(self.openCachetool, QtCore.SIGNAL("clicked()"), self.onCleanCache)
        self.connect(self.ticker, QtCore.SIGNAL("anchorClicked(QUrl)"), self.onRSSLinkClicked)
        self.connect(self.buttonNext, QtCore.SIGNAL("clicked()"), self.raiseTicker)
        self.connect(self.buttonPrev, QtCore.SIGNAL("clicked()"), self.lowerTicker)
        self.connect(self.buttonBrowse, QtCore.SIGNAL("clicked()"), self.onBrowse)
        self.connect(self.buttonAero, QtCore.SIGNAL("clicked()"), self.onAeroSwitch)

        # set fields
        self.versionslist = CADversions
        self.aero = options.aero
        self.showTicker()
        self.versionLabel.setText("cadstart V" + conf.version)
        
        # fill DropDown
        for i in range(len(self.versionslist)):
            self.desclist.append(self.versionslist[i].description)

        self.proList.addItems(self.desclist)
        
        # set checkboxes
        self.isPDM.setChecked(1)
        self.isGerman.setChecked(1)
        self.isOpengl.setChecked(1)
        
        # perform server test at startup
        self.onTest()
        
        # check if aero is running
        self.checkAero()
        
    # action at click on start
    def onStart(self): 
        
        # TODO: PDM via Combobox not checkboxes        
        #if self.isPDM.isChecked():
        #    self.release = self.release + ' ' + "PDM"
            
        #if self.isStandalone.isChecked():
        #    self.release = self.release

        if self.isGerman.isChecked():
            self.lang = "german"
        
        if self.isEnglish.isChecked():
            self.lang = "english"
            
        if self.isOpengl.isChecked():
            self.graphics = "graphics opengl"
            
        if self.isWin32gdi.isChecked():
            self.graphics = "graphics win32_gdi"
            
        pyDefStart.defStart(self)
        
        self.close()
    
    # action on select
    def onSelect(self, pathNo):
        
        self.selected = self.versionslist[pathNo]
        print(self.selected.path)
        print(self.selected.release)
        
    # action on links
    def onMailto(self):
        
        dialog = pyCADfeedbackFormuiHandler.FeedbackDialog(self.desclist) 
        
        # dialog show
        dialog.show()
        dialog.exec_()
        
        return
        
    def onHelp(self):
        
        # dialog instance
        dialog = pyCADhelpuiHandler.HelpDialog(self.CADversions) 
        
        # dialog show
        dialog.show()
        dialog.exec_()
        
        return
    
    def onRSS(self):
        
        webbrowser.open(conf.rssURL)
        
        return
    
    def onVPN(self):
        
        webbrowser.open(conf.vpnURL)
        
        return
    
    def onTest(self):
        
        info = PySide.QtNetwork.QHostInfo.fromName(conf.pdmHostName)
        
        if info.error() == 0:
            self.statusLight.setPixmap(QtGui.QPixmap(":/icons/img/icon_green.png"))
            self.isPDM.setEnabled(1)
            self.isPDM.setChecked(1)
            self.isStandalone.setChecked(0)
        elif info.error() == 1:
            self.statusLight.setPixmap(QtGui.QPixmap(":/icons/img/icon_red.png"))
            self.isStandalone.setChecked(1)
            self.isPDM.setEnabled(0)
        else:
            self.statusLight.setPixmap(QtGui.QPixmap(":/icons/img/icon_grey.png"))
            self.isStandalone.setChecked(1)
            self.isPDM.setEnabled(1)
            self.isPDM.setChecked(0)
        return
    
    def onCleanCache(self):
        
        # dialog instance
        dialog = pyCADdialoguiHandler.AskDialog()
                
        dialog.setText("Vorsicht:")
        dialog.setURL(pu.textURL("delcache"))
        
        # dialog modal show
        dialog.exec_()
        
        if dialog.getStatus():
            
            pyCADutils.cleanCache()
            
            print("cache geloescht")
            
            return
        
        else:
            
            print("abgebrochen")
            
            return
        
    def showTicker(self):
        
        item = self.currItem
        
        pyCADticker.setMessage(self, item)
        
        return
    
    def raiseTicker(self):
        
        self.currItem += 1
        
        pyCADticker.setMessage(self, self.currItem)
        
        return
    
    def lowerTicker(self):
        
        self.currItem -= 1
        
        pyCADticker.setMessage(self, self.currItem)
        
        return
        
    def onRSSLinkClicked(self, rssLinkURL):
        
        #PyQt4.Qt.QUrl.
        webbrowser.open(rssLinkURL.toString())
        
        return
    
    def onMac(self):
        
        params = urllib.parse({'program':'ptcschools4','hostid':self.mac})
        url = "http://www.ptc.com/appserver/lm/programs/index.jsp?" + params
            
        webbrowser.open(url)
        
    def onBrowse(self):
        
        return
    
    def onAeroSwitch(self):
        
        # if aero is running switch it off and vice versa
        if self.checkAero() == 1:
            os.system("net stop uxsms")    
        elif self.checkAero() == 0:
            os.system("net start uxsms")
            
        # refresh button color in GUI
        self.checkAero()
                
        return
    
    def checkAero(self):
        
        # preset button color to green
        self.buttonAero.setIcon(QtGui.QIcon(":/icons/img/icon_green.png"))
            
        # query uxsms (aero) status
        status = os.popen(os.getenv("systemroot")+"\system32\sc.exe query uxsms")
        
        # prepare regex pattern to fin status code (1 = stopped, 4 = running)
        pattern = re.compile('STATE.*?(\d).*')
        
        # iterate through status message
        for ln in status:
            
            # search for status code in each line
            match = re.findall(pattern, ln)
            
            # try to match status code, if "1" set button to "red"
            try:
                if match[0]=='4':
                    self.buttonAero.setIcon(QtGui.QIcon(":/icons/img/icon_red.png"))
                    # exit function and return "4" = "aero is running"
                    return 1    
            except:
                foo = 1
                
        # exit function and return "1" = "aero is stopped"
        return 0