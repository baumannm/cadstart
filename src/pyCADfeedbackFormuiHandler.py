#######################################################
#
# Help UI
#
#######################################################
import os 
import conf

import http, urllib
import webbrowser

from PySide               import QtGui, QtCore
from pyCADfeedbackFormui import Ui_Dialog as Dlg

class FeedbackDialog(QtGui.QDialog, Dlg): 
    
    oslist          = ["", "Windows 7", "Windows XP", "Windows Vista", "anderes"]
    platformlist    = ["", "Laptop", "PC", "Netbook", "Poolraum Workstation", "andere"]
    graphicslist    = ["", "Intel Onboard", "nVidia Geforce", "ATI Radeon", "nVidia Quadro", "ATI FireGL", "andere"]
    lecturelist     = ["MKL 4", "MKL 3", "MKL 2", "MKL 1", "IP", "Studien-/Diplomarbeit", "anderes"]
    majorlist       = ["Maschinenbau", "CIW", "anderer"]
    architecturelist = ["", "32 Bit", "64 Bit"]
    topiclist       = ["", "1: Modellieren und Zeichnen -> ", "2: Datenverwaltung im PDM -> ", "3: Organisatorisches -> ", "4: PDM Account -> ", "4: Verbindung zum Server -> ", "6: Softwareinstallation -> "]
    
    name        = ""
    name_       = ""
    matrikel    = ""
    semester    = ""
    lecture     = ""
    major       = ""
    email_      = ""
    email       = ""
    os          = ""
    architecture= ""
    platform    = ""
    grafics     = ""
    proever     = ""
    text        = ""
    subject_     = ""
    subject     = ""
    
    # Constructor
    def __init__(self, proelist): 
        
        QtGui.QDialog.__init__(self) 
        self.setupUi(self)
        
        # Slots
        self.connect(self.buttonSend, QtCore.SIGNAL("clicked()"), self.onSend)
        self.connect(self.buttonCancel, QtCore.SIGNAL("clicked()"), self.onCancel)
        self.connect(self.buttonMailClient, QtCore.SIGNAL("clicked()"), self.onMailClient)
        self.connect(self.buttonTextEditor, QtCore.SIGNAL("clicked()"), self.onTextEditor)
        self.connect(self.openFAQ, QtCore.SIGNAL("clicked()"), self.onFAQ)
        
        self.fieldProE.addItems(proelist)
        self.fieldOS.addItems(self.oslist)
        self.fieldPlatform.addItems(self.platformlist)
        self.fieldGraphics.addItems(self.graphicslist)
        self.fieldMajor.addItems(self.majorlist)
        self.fieldLecture.addItems(self.lecturelist)
        self.fieldArchitecture.addItems(self.architecturelist)
        self.fieldTopic.addItems(self.topiclist)
        
        
    def onSend(self):
        
        self.getFields()
        
        message = self.generateMessage().toLatin1()
        subject = self.subject_.toLatin1()
        
        params = urllib.parse({'kontakt':'cad' , 'from_name':self.name_, 'from_mail':self.email_, 'subject':subject, 'kommentar':message})
        
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        
        conn = http.client.HTTPConnection("www.ipek.uni-karlsruhe.de:80")
        
        conn.request("POST", "/cms/de/kontakt/kontakt.php", params, headers)
        
        response = conn.getresponse()
        
        print(response.status, response.reason)
        
        data = response.read()
        
        conn.close()
        
        self.close()
        
        return
        
    def onCancel(self):
        
        self.close()
        
        return
    
    def onFAQ(self):
        
        webbrowser.open(conf.faqURL)
        
        return    
        
    def onMailClient(self):
        
        self.getFields()
        
        mailto = "mailto:cad@ipek.uka.de?" + urllib.parse({'subject':self.subject_.toUtf8(), 'body':self.generateMessage().toUtf8()})
        
        webbrowser.open(mailto.replace("+", " "))
        
        self.close()
        
        return
        
    def onTextEditor(self):
        
        self.getFields()
        
        fpath = os.getenv("TEMP") + "\\mail.txt"
        
        f = open(fpath, "w")
        f.write(self.generateMessage())
        f.close()
        
        os.system(fpath)
        
        self.close()
        
        return
    
    def getFields(self):
        
        if self.isPersonal.isChecked():
            self.name_          = self.fieldName.text()
            self.name           = "Name: "              + self.fieldName.text()
            self.matrikel       = "Matrikelnummer: "    + self.fieldMNumber.text()
            self.semester       = "Semester: "          + str(self.fieldSemester.value())
            self.lecture        = "Fach: "              + self.fieldLecture.currentText()
            self.major          = "Studiengang: "       + self.fieldMajor.currentText()
            self.email_         = self.fieldMail.text()
            self.email          = "E-Mail Adresse: "    + self.fieldMail.text()
            
        else:
            self.name_          = ""
            self.name           = ""
            self.matrikel       = ""
            self.semester       = ""
            self.lecture        = ""
            self.major          = ""
            self.email_         = ""
            self.email          = ""
            
        if self.isSystem.isChecked():
            self.os             = "OS: "                + self.fieldOS.currentText()
            self.architecture   = "Architektur: "       + self.fieldArchitecture.currentText()
            self.platform       = "Platform: "          + self.fieldPlatform.currentText()
            self.grafics        = "Grafik: "            + self.fieldGraphics.currentText()
            self.proever        = "Pro/E Version: "     + self.fieldProE.currentText()
            
        else:
            self.os             = ""
            self.architecture   = ""
            self.platform       = ""
            self.grafics        = ""
            self.proever        = ""
            
        self.subject_           = self.fieldTopic.currentText()+self.fieldSubject.text()
        self.subject            = "Betreff: \n"  + self.fieldTopic.currentText()+ self.fieldSubject.text()    
        self.text               = "Nachricht: \n"   + self.fieldText.toPlainText()
        
        return        
    
    def generateMessage(self):
        
        self.getFields()
        
        line = "\n--------------------\n"
        
        message =   line + \
                    self.subject + \
                    line + \
                    self.text + \
                    line + \
                    self.name + \
                    line + \
                    self.matrikel + \
                    line + \
                    self.semester + \
                    line + \
                    self.lecture + \
                    line + \
                    self.major + \
                    line + \
                    self.email + \
                    line + \
                    self.os + \
                    line + \
                    self.architecture + \
                    line + \
                    self.platform + \
                    line + \
                    self.grafics + \
                    line + \
                    self.proever + \
                    line
                    
        return message
