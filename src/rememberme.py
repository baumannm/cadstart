from xml.dom import minidom
from xml.dom.minidom import Document
import os
import re


class lastsettings():
    
    CADid = 0
    ServerID = 0
    language = 'german'
    graphics = 'opengl'
    
    
    def __init__(self, versionlist, CoreOptList):
        os.getenv("APPDATA")
        folder = os.path.join(os.getenv("APPDATA"), "cadstart\\")
        print(folder)
        if os.path.exists(folder):
            fileabs = os.path.join(folder, "lastsession.xml")
            print(fileabs)
            if os.path.isfile(fileabs):
                try: 
                    xmldoc          = minidom.parse(fileabs)   
                    lastsettings    = xmldoc.getElementsByTagName("lastsettings")[0]
                    
                    CADVersion      = lastsettings.getElementsByTagName("CADVersion")[0]
                    
                    self.name            = CADVersion.getElementsByTagName("name")[0].firstChild.data
                    self.release         = CADVersion.getElementsByTagName("release")[0].firstChild.data
                    self.datecode        = CADVersion.getElementsByTagName("datecode")[0].firstChild.data
                    self.installdir      = CADVersion.getElementsByTagName("installdir")[0].firstChild.data
                
                    self.Server          = lastsettings.getElementsByTagName("Server")[0].firstChild.data
                    self.language        = lastsettings.getElementsByTagName("language")[0].firstChild.data
                    self.graphics    = lastsettings.getElementsByTagName("graphicmode")[0].firstChild.data
                    
                except IOError:
                    print("lastsession.xml IOError")
                    
                self.CADid = self.getversionid(versionlist)
                self.ServerID = self.getserverid(CoreOptList)            
            
            
            
                    
    def getversionid(self, versionlist):
        for i in range(len(versionlist)):
            n = (self.name == versionlist[i].name)
            r = (self.release == versionlist[i].release)
            d = (self.datecode == versionlist[i].datecode)
            inst = (self.installdir == versionlist[i].installdir)
            if (n and r and d and inst):
                return i
                break
            
    def getserverid(self, CoreOptList):
        for i in range(len(CoreOptList.PDMserverList.optionfilelist)):
            n = (self.Server == CoreOptList.PDMserverList.optionfilelist[i].ID)
            if (n):
                return i
                break
 

def savesettings(name, release, datecode, installdir, ServerID, language, graphicmode):
    os.getenv("APPDATA")
    folder = os.path.join(os.getenv("APPDATA"), "cadstart\\")

    if not (os.path.exists(folder)):
        os.makedirs(folder)
        
        
    fileabs = os.path.join(folder, "lastsession.xml")
    #if not (os.path.isfile(fileabs)):
    #    os.makedirs(folder)
    
    file = open(fileabs, 'w+')   

    #create minidom-document
    doc = Document()

    # create base element
    base = doc.createElement('lastsettings')
    doc.appendChild(base)

    # create an entry element
    CADversion = doc.createElement('CADVersion')

    # ... and append it to the base element
    base.appendChild(CADversion)

    # create another element 
    name_element = doc.createElement('name')
    release_element = doc.createElement('release')
    datecode_element = doc.createElement('datecode')
    installdir_element = doc.createElement('installdir')

    # create content
    name_content = doc.createTextNode(name)
    release_content = doc.createTextNode(release)
    datecode_content = doc.createTextNode(datecode)
    installdir_content = doc.createTextNode(installdir)

    # append content to element
    name_element.appendChild(name_content)
    release_element.appendChild(release_content)
    datecode_element.appendChild(datecode_content)
    installdir_element.appendChild(installdir_content)

    # append the german entry to our entry element
    CADversion.appendChild(name_element)
    CADversion.appendChild(release_element)
    CADversion.appendChild(datecode_element)
    CADversion.appendChild(installdir_element)
     
    
    # create an entry element
    Server_element = doc.createElement('Server')
    Server_content = doc.createTextNode(ServerID)
    Server_element.appendChild(Server_content)
    
    # ... and append it to the base element
    base.appendChild(Server_element)
    
    
    # create an entry element
    language_element = doc.createElement('language')
    language_content = doc.createTextNode(language)
    language_element.appendChild(language_content)
    
    # ... and append it to the base element
    base.appendChild(language_element)    
    
    
    
    # create an entry element
    graphic_element = doc.createElement('graphicmode')
    graphic_content = doc.createTextNode(graphicmode)
    graphic_element.appendChild(graphic_content)
    
    # ... and append it to the base element
    base.appendChild(graphic_element)    
    
    
    doc.writexml(file, "", "\t", "\n") 
    file.close()
    
    
    