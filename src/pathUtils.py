# enclose a given string with quotes
import os
import PySide.QtCore

def spacePath(inp):
    
    output=('"'+inp+'"')
    output=(normPath(output))
    
    return output

# normalize path
def normPath(inp):
    
    output = os.path.normpath(inp)
    
    return output

# return a string out of lst elements separated with spaces
def spacer(lst):
    
    output=''
    
    for i in lst:
        output=output+' '+i
        
    return output

# return a string out of lst elements separated with spaces and enclosed with quotes
def spacerq(lst):
    
    output = ''
    
    for i in lst:
        
        i=spacePath(i)
        
        output=output+' '+i
        
    return output

# return URL to html file specified with "inp". Optional argument "lang" defaults to "de"
def textURL(inp, lang="de"):
    
    output=PySide.QtCore.QUrl(os.getcwd()+"\\doc\\"+lang+"\\"+inp+".html")

    return output