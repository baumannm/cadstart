import winreg
from pyCADutils import iterateKeys
import os
import re
import conf
from xml.dom import minidom


class versionid:
    namemask = ""
    releasemask = ""
    versionid = ""
    startcommand = ""
    configdir = ""
    
    def __init__(self,namemask, releasemask, versid, startcommand, configdir):
        self.namemask = namemask
        self.releasemask = releasemask
        self.versionid = versid
        self.startcommand = startcommand
        self.cofigdir = configdir
        
        
        
        
class versionidlist:
    versidlist = []
    
    def __init__(self):
        self.versidlist = []
        filerel = conf.appconfig + "versionid.xml"
        fileabs = os.path.join(os.getcwd(), filerel)
        if os.path.isfile(fileabs): 
            try: 
                xmldoc = minidom.parse(fileabs)  
                idfile = xmldoc.getElementsByTagName("versionidlist")[0]
                idlist = idfile.getElementsByTagName("version")
                for idelement in idlist:
                    namemask = idelement.getElementsByTagName("name")[0].firstChild.data
                    releasemask = idelement.getElementsByTagName("release")[0].firstChild.data
                    versid = idelement.getElementsByTagName("versionid")[0].firstChild.data
                    startcmd = idelement.getElementsByTagName("startcommand")[0].firstChild.data
                    cfgdir = idelement.getElementsByTagName("configdir")[0].firstChild.data
                    versionidele = versionid(namemask, releasemask, versid, startcmd, cfgdir)
                    self.versidlist.append(versionidele)
            except IOError:
                print("versionid.xml IOError")
                
    def findid(self, name, release):
        for idelement in self.versidlist:
            n = not(re.search(name, idelement.namemask, flags=0)==None)
            r = not(re.search(release, idelement.releasemask, flags=0)==None)
            if (n and r):
                return idelement
                break
        else: 
            print(name + release + " not identified")
            return "other"
            
            
        


class version:
    
    # name e.g. 'Creo Parametric' or 'Pro/Engineer'
    name        =''
    
    # release e.g. 'Wilfire 4' or '2.0' 
    release     =''
    
    # datecode e.g. 'F000' or 'M010'
    datecode    =''
    
    # directory e.g. "C:\Program Files\PTC\Creo 2.0'
    installdir  =''
    
    # version-type e.g ProE Wildfire 4 or Creo Parametric 2 as short identifier e.g. WF4 or CP2
    versionid     = ''
    
    # description shown in the GUI-selector
    description = ''
     
        
    def __init__(self, versionidlist, name, release, datecode, installdir):
        self.name       = name
        self.release    = release
        self.datecode   = datecode
        self.installdir = installdir
        self.description = self.name + " -- " + self.release + " -- " +self.datecode
        self.versionid = versionidlist.findid(name, release)
            
        
        
        

class CADidentifier:
    
    # define rootkey
    key = winreg.HKEY_LOCAL_MACHINE
    
    # concatenate licence version, program and shipcode
    list=[]
    
    
    versidlist = ""
    
    options = 0
    
    # initialize
    def __init__(self, options):
               
        self.list = []
        self.options = options
        
        
        self.versidlist = versionidlist()    
        
        # 1. try to identify and append all local Pro/Es (32bit and 64bit versions)
        self.identify(winreg.KEY_WOW64_64KEY)
        self.identify(winreg.KEY_WOW64_32KEY)
        
        # 2. filter identified Pro/Es
        self.filter()
        
        # 3. always check, if this is started from an IPEK computer
        # if so, and if all paths are available append them aswell
        self.ipek()
        
        # 4. and eventually check if an optional pro/E install path,
        # given as script argument exists. Append. 
        self.own()
        
        # Just stdout ...
        self.printList()
            
        
    # returns listitems,programs,shipcodes,paths,releases,lvs
    def identify(self,platform):
        
        # try to find locally installed pro/Es
        try:
            # open HKLM/Software/PTC
            ptckey = winreg.OpenKey(self.key, "Software\PTC", 0, winreg.KEY_READ | platform)
                 
            # go through all subkeys of HKLM/Software/PTC, e.g.  HKLM/Software/PTC/Student, HKLM/Software/PTC/School
            for i in iterateKeys(ptckey):
                
            # open a license version subkey, e.g. HKLM/Software/PTC/Student Edition
                proekey = winreg.OpenKey(ptckey, i, 0, winreg.KEY_READ | platform)
                
                # go through all Pro/E versions of a license version, e.g. HKLM/Software/PTC/School/WF3, HKLM/Software/PTC/School/WF4
                for j in iterateKeys(proekey):
                # open a version subkey
                
                    versionkey = winreg.OpenKey(proekey, j, 0, winreg.KEY_READ | platform)
                    # go through all datecodes of a version
                    
                    for k in iterateKeys(versionkey):
                    # open a datecodekey
                    
                        datecodekey = winreg.OpenKey(versionkey, k, 0, winreg.KEY_READ | platform)
                        
                        temp1 = winreg.QueryValueEx(datecodekey, 'Shipcode')[0]
                        temp2 = winreg.QueryValueEx(datecodekey, 'InstallDir')[0]
                        temp3 = winreg.QueryValueEx(datecodekey, 'Release')[0]
                        
                       # self.append(i,
                       #             j,
                       #             winreg.QueryValueEx(datecodekey, 'Shipcode')[0],
                       #             winreg.QueryValueEx(datecodekey, 'InstallDir')[0],
                       #             winreg.QueryValueEx(datecodekey, 'Release')[0])

                        self.append(i,j,temp1,temp2)

        # if no local proe can be determined
        except:
            
            print("no properly installed Pro/E Version detected")
            
    def filter(self):
        filerel = conf.appconfig + "filter.xml"
        fileabs = os.path.join(os.getcwd(), filerel)
        if os.path.isfile(fileabs): 
            try: 
                xmldoc = minidom.parse(fileabs)
                filterfile = xmldoc.getElementsByTagName("filterlist")[0]
                filterlist = filterfile.getElementsByTagName("filter")
                for filteri in filterlist:
                    name = filteri.getElementsByTagName("name")[0].firstChild.data
                    release = filteri.getElementsByTagName("release")[0].firstChild.data
                    datecode = filteri.getElementsByTagName("datecode")[0].firstChild.data
                    installdir = filteri.getElementsByTagName("installdir")[0].firstChild.data
                    i = int(0)
                    while i < len(self.list):
                        n = not(re.search(name, self.list[i].name, flags=0)==None)
                        r = not(re.search(release, self.list[i].release, flags=0)==None)
                        d = not(re.search(datecode, self.list[i].datecode, flags=0)==None)
                        inst = not(re.search(installdir, self.list[i].installdir, flags=0)==None)
                        if n and r and d and inst:
                            self.list.pop(i)
                            i = i-1
                        i = i+1
            except IOError:
                print("filter.xml IOError")
        
        
    def ipek(self):
        
        # append central installations at IPEK
        # only show up if z:\cad\ is available   
        if os.path.exists(os.getenv("PRO_FILES")) and self.options.ipekpool:
            
            path, null = os.path.split(os.getenv("PRO_FILES"))
            #
            self.append("Pro/ENGINEER Educational",
                        "Wildfire 4.0",
                        "IPEK fallback",
                        path+"\\proewildfire 4.0",
                        )
            
            self.append("Pro/ENGINEER Educational",
                        "Wildfire 3.0",
                        "IPEK fallback",
                        path+"\\proewildfire 3.0",
                        )
            
    def own(self):
                
        try:
            filerel = conf.appconfig + "versions.xml"
            fileabs = os.path.join(os.getcwd(), filerel)
            if os.path.isfile(fileabs): 
                print("ownversion.xml found")
                xmldoc = minidom.parse(fileabs)
                versionsfile = xmldoc.getElementsByTagName("versionlist")[0]
                versionslist = versionsfile.getElementsByTagName("version")
                for versioni in versionslist:
                    name = versioni.getElementsByTagName("name")[0].firstChild.data
                    rel = versioni.getElementsByTagName("release")[0].firstChild.data
                    datecode = versioni.getElementsByTagName("datecode")[0].firstChild.data
                    installdir = versioni.getElementsByTagName("installdir")[0].firstChild.data
                    if os.path.exists(installdir):
                        self.append(name, rel, datecode, installdir)
        except:
            print("ownversion.xml not found")
            
            
    def append(self,name="",rel="",datecode="",installdir=""):
        
        listitem = version(self.versidlist,name,rel,datecode,installdir)
        self.list.append(listitem)

        
    def printList(self):
        
        print("begin version list")
        
        # list and print results
        for i in range(len(self.list)):
            print(self.list[i].description)
        
        print("end version list")
