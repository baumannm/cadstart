import os
import time

def mergefile(file, targetlist):
    if os.path.isfile(file):
        f1= open(file,'r')
        newlines = f1.readlines()
        targetlist.extend(newlines)

def mergelist(filelist, targetfile):
    temptarget = []
    lt = time.localtime()
    temptarget.append(time.strftime("! Date of merging: %c", lt))
    for file in filelist:
        temptarget.append("\n\n! " + file + "\n")
        mergefile(file, temptarget)
    if os.path.isfile(targetfile):
        os.remove(targetfile)
    target = open(targetfile,'a')
    target.writelines(temptarget)
    target.close
    