import winreg
from pyCADutils import iterateKeys
import os


class CADidentifier:
    
    # define rootkey
    key = winreg.HKEY_LOCAL_MACHINE
    # list to store all paths
    paths = []
    # list to store all program versions
    programs = []
    # licenseversions
    licenses = []
    # list all shipcodes
    shipcodes = []
    # list all releases
    releases = []
    # concatenate licence version, program and shipcode
    list=[]
    # start arguments
    options = 0
    
    # initialize
    def __init__(self,options):
        
        # set local field options from script call arguments
        self.options = options
        
        # 1. try to identify and append all local pro/Es (32bit and 64bit versions)
        self.identify(winreg.KEY_WOW64_64KEY)
        self.identify(winreg.KEY_WOW64_32KEY)
        
        # 2. always check, if this is started from an IPEK computer
        # if so, and if all paths are available append them aswell
        self.ipek()
        
        # 3. and eventually check if an optional pro/E install path,
        # given as script argument exists. Append. 
        self.own()
        
        # make the nice list
        self.makeList()
            
        
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
                    # open a deatecodekey
                    
                        datecodekey = winreg.OpenKey(versionkey, k, 0, winreg.KEY_READ | platform)
                        
                        self.append(i,
                                    j,
                                    winreg.QueryValueEx(datecodekey, 'Shipcode')[0],
                                    winreg.QueryValueEx(datecodekey, 'InstallDir')[0],
                                    winreg.QueryValueEx(datecodekey, 'Release')[0])
                        
        # if no local proe can be determined
        except:
            
            print("no properly installed Pro/E Version detected")
            
        
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
                        "Wildfire 4.0")
            
            self.append("Pro/ENGINEER Educational",
                        "Wildfire 3.0",
                        "IPEK fallback",
                        path+"\\proewildfire 3.0",
                        "Wildfire 3.0")
            
    def own(self):
                
        try:
            
            print("own version found")
            print(self.options.propath)
            
            if os.path.exists(self.options.propath):

                self.append("other Pro/E version",
                            self.options.propath,
                            "Wildfire 4.0",
                            self.options.propath,
                            "Wildfire 4.0")
                
        except:

            print("own version not found")
            
    def append(self,lic="",pro="",shi="",pat="",rel=""):
        
        self.licenses.append(lic)
        self.programs.append(pro)
        self.shipcodes.append(shi)
        self.paths.append(pat)
        self.releases.append(rel)
        
    def makeList(self):
        
        # reset list
        self.list = []
        
        print("begin version list")
        
        # list and print results
        for i in range(len(self.paths)):
        
            self.list.append(self.licenses[i]+" -- "+self.programs[i]+" -- "+self.shipcodes[i])
            print(self.licenses[i]+" -- "+self.programs[i]+" -- "+self.shipcodes[i])
        
        print("end version list")
