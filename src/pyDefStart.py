import os
import envUtils as eu

def defStart(handler):

    # read some environment variables       
    profiles = eu.get("PRO_FILES") 
    temp     = os.getenv("TEMP")

    # put environment variables
    os.environ["PRO_DIRECTORY"]     = handler.selected.installdir
    os.environ["PRO_CONF_FILES"]    = handler.selected.versionid.versionid
    os.environ["LANG"]              = handler.lang
    
    # prepare copy commands
    target = '"' + temp +'\\"'
    source = '"' + profiles + '\\konfiguration\\' + handler.selected.versionid.configdir + '\\*.*"'
    copycmd = 'copy ' + source + ' ' + target + ' /Y'
    #print(copycmd)
    
    # copy
    try:
        os.system(copycmd)
    except:
        print('Error while copying config-files')

    setGraphics(handler, temp, profiles)
    #setModelTreeLanguage(handler, temp, profiles)
    
    # start proe
    os.chdir(temp)
    startupcommand = '"'+handler.selected.installdir+handler.selected.versionid.startcommand+'"'
    os.system('START "Creo" ' + startupcommand)

def setGraphics(handler, temp, profiles):
    
    # stop aero automatically if application was started with parameter "-a"
    if handler.aero:
        os.system("net stop uxsms")
        
    f = open(temp + '\\config.pro', "a")
    f.write("!graphics mode set by cadstart\n")
    f.write(handler.graphics)
    f.close()
    
def setModelTreeLanguage(handler, temp, profiles):
    
    f1= open(profiles + '\\konfiguration\\_gemeinsam\\tree_cfg\\asm_tree.cfg','r')
    atreetgt= open(temp + '\\asm_tree.cfg','w')    
    atreesrc = f1.readlines()

    
    if handler.lang == "german":
        # modify model tree
        for line in atreesrc:
            atreetgt.write(line.replace('COLUMN','!COLUMN'))
    
    if handler.lang == "english":
        # modify model tree
        for line in atreesrc:
            atreetgt.write(line.replace("SPALTE","!SPALTE"))
        
    f1.close()
    atreetgt.close()
