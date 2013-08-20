import os
import conf
import envUtils as eu
import configmerge
import glob
import rememberme

def defStart(handler):

    # read some environment variables       
    profiles = eu.get("PRO_FILES") 

    # put environment variables
    os.environ["PRO_DIRECTORY"]     = handler.selectedProE.installdir
    os.environ["PRO_CONF_FILES"]    = handler.selectedProE.versionid.versionid
    os.environ["LANG"]              = handler.lang
    
    a = handler.selectedProE.name
    b = handler.selectedProE.release
    c = handler.selectedProE.datecode
    d = handler.selectedProE.installdir
    e = handler.selectedServer.ID
    f = handler.lang
    g = handler.graphics
    
    
    rememberme.savesettings(a, b, c, d, e, f, g)
    
    
    # merge configs
    basedir = profiles + '\\' + conf.configdir + '\\' + handler.selectedProE.versionid.configdir + '\\configpro'
    if not os.path.exists(conf.temp + '\\' + conf.tempmergedir):
        os.makedirs(conf.temp + '\\' + conf.tempmergedir)
    targetfile = conf.temp + '\\' + conf.tempmergedir + '\\config.pro'
    filelist = glob.glob(basedir + '\\*.pro')
    filelist.append(basedir + '\\' + handler.PDMserver.subfolder + '\\' +  handler.selectedServer.filename)
    filelist.append(basedir + '\\' + 'treecfg' + '\\' +  handler.lang + '.pro')
    filelist.append(basedir + '\\' + 'graphics' + '\\' +  handler.graphics + '.pro')
    configmerge.mergelist(filelist, targetfile)
    
    
    
    # prepare copy commands
    
    target = '"' + conf.workdir +'\\"'
    source1 = '"' + profiles + '\\' + conf.configdir + '\\' + handler.selectedProE.versionid.configdir + '\\*.*"'
    source2 = '"' + conf.temp + '\\' + conf.tempmergedir + '\\*.*"'

    
    copycmd1 = 'copy ' + source1 + ' ' + target + ' /Y'
    copycmd2 = 'copy ' + source2 + ' ' + target + ' /Y'
    
    # copy
    try:
        os.system(copycmd1)
        os.system(copycmd2)
    except:
        print('Error while copying config-files')

    # todo: stop Aero
    #setModelTreeLanguage(handler, temp, profiles)
    
    # start proe
    os.chdir(conf.workdir)
    startupcommand = '"' + handler.selectedProE.installdir + '\\' + handler.selectedProE.versionid.startcommand + '"'
    os.system('START "Creo" ' + startupcommand)


