from xml.dom import minidom
import conf
import os

class Toptionfile:
    
    ID = ""
    
    displayname_de = ""
    
    displayname_en = ""
    
    filename = ""
    
    def __init__(self, ID, displayname_de, displayname_en, filename):
        self.ID = ID
        self.displayname_de = displayname_de
        self.displayname_en = displayname_en
        self.filename = filename
    

class TconfigOption:
    
    ID = ""
    
    displayname_de = ""
    
    displayname_en = ""
    
    subfolder = ""
    
    optionfilelist = []    
    
    def __init__(self, ID, displayname_de, displayname_en, subfolder):
        self.ID = ID
        self.displayname_de = displayname_de
        self.displayname_en = displayname_en
        self.subfolder = subfolder
        self.optionfilelist = []
    
    def appendfile(self, optionfile):
        self.optionfilelist.append(optionfile)
              



class coreoptions():
    
    coreoptionlist = []
    PDMserverList = []
    PDMdisplaylist = []


    def __init__(self):
        self.getcoreopt()
        self.getPDMserverList()

    def getcoreopt(self):
        filerel = conf.appconfig + "configoptions_core.xml"
        print(filerel)
        fileabs = os.path.join(conf.applicationdir, filerel)
        print(fileabs)
        if os.path.isfile(fileabs): 
            try: 
                xmldoc = minidom.parse(fileabs)  
                configoptionfile = xmldoc.getElementsByTagName("configoptionlist")[0]
                configoptionlist = configoptionfile.getElementsByTagName("configoption")
                for configoption in configoptionlist:
                    id_option               = configoption.getElementsByTagName("id")[0].firstChild.data
                    displayname_de_opt      = configoption.getElementsByTagName("displayname_de")[0].firstChild.data
                    displayname_en_opt      = configoption.getElementsByTagName("displayname_en")[0].firstChild.data
                    subfolder               = configoption.getElementsByTagName("subfolder")[0].firstChild.data
                    #common = configoption.getElementsByTagName("common")[0].firstChild.data
                    #priority = configoption.getElementsByTagName("priority")[0].firstChild.data
                    tempcoreopt = TconfigOption(id_option, displayname_de_opt, displayname_en_opt, subfolder)
                    configoptionfilelist = configoption.getElementsByTagName("optionfile")
                    for optionfile in configoptionfilelist:
                        id_file             = optionfile.getElementsByTagName("id")[0].firstChild.data
                        displayname_de_file = optionfile.getElementsByTagName("displayname_de")[0].firstChild.data
                        displayname_en_file = optionfile.getElementsByTagName("displayname_en")[0].firstChild.data
                        filename            = optionfile.getElementsByTagName("filename")[0].firstChild.data
                        tempcoreoptfile = Toptionfile(id_file, displayname_de_file, displayname_en_file, filename)
                        tempcoreopt.appendfile(tempcoreoptfile)
                
                    self.coreoptionlist.append(tempcoreopt)
                
            except IOError:
                print("configoptions_core.xml IOError")
    
    
    def getPDMserverList(self):
        for configoptionitem in self.coreoptionlist:
            if configoptionitem.ID == "PDM": 
                self.PDMserverList = configoptionitem
                self.PDMdisplaylist = []
                for Server in self.PDMserverList.optionfilelist:
                    self.PDMdisplaylist.append(Server.displayname_de)
                    
