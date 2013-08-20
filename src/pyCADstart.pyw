#######################################################
#
# preparations
#
#######################################################
import pyCADutils
import conf

import sys
import os

import suboptions
from pyCADidentifier    import CADidentifier
from PySide             import QtGui
from pyCADuiHandler     import StartDialog
from optparse           import OptionParser

import rememberme


#######################################################
#
# main
#
#######################################################
sys.stdout = open(os.getenv('TEMP')+'\pyCADstartSTDOUT.txt', 'w')
sys.stderr = open(os.getenv('TEMP')+'\pyCADstartSTDERR.txt', 'w')

# Directroy
conf.temp       = os.getenv("TEMP")
conf.applicationdir = os.getcwd()
conf.workdir    = conf.temp
  

parser = OptionParser(usage="%prog [-p] [-z] [-c] [-i] [-a]", version="%prog IPEKumgebung "+conf.version)
parser.add_option("-p", "", dest="profiles", help="full path to IPEKUmgebung", metavar="<path>")

# TODO: delete
parser.add_option("-z", "", dest="propath", help="full path to Pro/E install dir", metavar="<path>")

parser.add_option("-c", "", action="store_true", dest="cleancache", default=False, help="cleans the cache")
parser.add_option("-i", "", action="store_true", dest="ipekpool", default=False, help="indicates the IPEK computer pool environment")
parser.add_option("-a", "", action="store_true", dest="aero", default=False, help="stop aero service at startup")

(options, args) = parser.parse_args()

print(options.propath)



if options.profiles:
    os.environ["PRO_FILES"]     = options.profiles
else:
    # get current directory, walk two up and set as pro/files
    profiles                    = os.getcwd()
    profiles, foo               = os.path.split(profiles)
    #profiles, foo               = os.path.split(profiles)
    os.environ["PRO_FILES"]     = profiles

if options.cleancache:
    pyCADutils.cleanCache()

# identify installed Pro/E from registry
CADversions = CADidentifier(options).list

# PDM-Serverlist
CoreOptList = suboptions.coreoptions()

lastsettings = rememberme.lastsettings(CADversions, CoreOptList)



# dialog instance
app     = QtGui.QApplication(sys.argv)
dialog  = StartDialog(CADversions, CoreOptList, options, lastsettings)

# dialog show
dialog.show() 
sys.exit(app.exec_())