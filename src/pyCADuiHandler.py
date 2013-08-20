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
    PDMlist = []
    graphics = ""
    currItem = 0
    CADversions = 0
    mac = ""
    
        
    # Constructor
    def __init__(self, CADversions, CoreOptList, options, lastsettings): 
        
        QtGui.QDialog.__init__(self) 
        self.setupUi(self)

        # Slots
        self.connect(self.buttonStart, QtCore.SIGNAL("clicked()"), self.onStart)
        self.connect(self.proList, QtCore.SIGNAL("currentIndexChanged(int)"), self.onSelectProE)
        self.connect(self.ServerList, QtCore.SIGNAL("currentIndexChanged(int)"), self.onSelectServer)
        self.connect(self.openMailtoCAD, QtCore.SIGNAL("clicked()"), self.onMailto)
        self.connect(self.openRSSFeed, QtCore.SIGNAL("clicked()"), self.onRSS)
        self.connect(self.openHelp, QtCore.SIGNAL("clicked()"), self.onHelp)
        self.connect(self.buttonVPN, QtCore.SIGNAL("clicked()"), self.onVPN)
        self.connect(self.buttonTest, QtCore.SIGNAL("clicked()"), self.onTest)
        self.connect(self.openCachetool, QtCore.SIGNAL("clicked()"), self.onCleanCache)
        self.connect(self.ticker, QtCore.SIGNAL("anchorClicked(QUrl)"), self.onRSSLinkClicked)
        self.connect(self.buttonNext, QtCore.SIGNAL("clicked()"), self.raiseTicker)
        self.connect(self.buttonPrev, QtCore.SIGNAL("clicked()"), self.lowerTicker)

        # set fields
        self.versionslist = CADversions
        self.serverlist = CoreOptList.PDMserverList.optionfilelist
        self.PDMserver = CoreOptList.PDMserverList
        self.showTicker()
        self.versionLabel.setText("cadstart V" + conf.version)
        
        # fill DropDown
        for i in range(len(self.versionslist)):
            self.desclist.append(self.versionslist[i].description)
            
        for displayitem in CoreOptList.PDMdisplaylist:
            self.PDMlist.append(displayitem)

        self.proList.addItems(self.desclist)
        self.ServerList.addItems(self.PDMlist)
        
        # set checkboxes
        self.isGerman.setChecked(1)
        self.isOpengl.setChecked(1)
        
        # perform server test at startup
        self.onTest()
        
        # set last used
        
        self.proList.setCurrentIndex(lastsettings.CADid)
        self.ServerList.setCurrentIndex(lastsettings.ServerID)
        if lastsettings.language == "german":
            self.isGerman.setChecked(1)
        if lastsettings.language == "english":
            self.isEnglish.setChecked(1)
            
        if lastsettings.graphics == "opengl":
            self.isOpengl.setChecked(1)
        if lastsettings.graphics == "win32gdi":
            self.isWin32gdi.setChecked(1)
        
        
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
            self.graphics = "opengl"
            
        if self.isWin32gdi.isChecked():
            self.graphics = "win32gdi"
            
        pyDefStart.defStart(self)
        
        self.close()
    
    # action on select Proe / Creo Version
    def onSelectProE(self, pathNo):
        
        self.selectedProE = self.versionslist[pathNo]
        print(self.selectedProE.release)
        
    # action on select Server
    def onSelectServer(self, pathNo):
        
        self.selectedServer = self.serverlist[pathNo]

        
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
        elif info.error() == 1:
            self.statusLight.setPixmap(QtGui.QPixmap(":/icons/img/icon_red.png"))
        else:
            self.statusLight.setPixmap(QtGui.QPixmap(":/icons/img/icon_grey.png"))
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
        
