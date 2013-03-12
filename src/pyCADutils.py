import pathUtils as pu
import winreg
import os
import time

def iterateKeys(key):
    
    keylist=[]
    
    for i in range(winreg.QueryInfoKey(key)[0]):
        keylist.append(winreg.EnumKey(key,i))
    
    return keylist

def cleanCache():
    
    wf1 = os.getenv("USERPROFILE") + "\\Anwendungsdaten\\PTC\\ProENGINEER\\Wildfire\\.wf"
    wf2 = os.getenv("USERPROFILE") + "\\Appdata\\Roaming\\PTC\\ProENGINEER\\Wildfire\\.wf"
    
    if (os.path.exists(wf1) or os.path.exists(wf2)):
    
        wf1del = pu.spacePath(os.getenv("USERPROFILE") + "\\Anwendungsdaten\\PTC\\ProENGINEER\\Wildfire\\WS_Backup\\Workspace_" + time.strftime("%Y%m%d_%H%M%S"))
        wf2del = pu.spacePath(os.getenv("USERPROFILE") + "\\Appdata\\Roaming\\PTC\\ProENGINEER\\Wildfire\\WS_Backup\\Workspace_" + time.strftime("%Y%m%d_%H%M%S"))
    
        os.system("mkdir " + wf1del)
        os.system("mkdir " + wf2del)
    
        os.system("move " + wf1 + " " + wf1del)
        os.system("move " + wf2 + " " + wf2del)