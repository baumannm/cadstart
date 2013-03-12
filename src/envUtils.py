import os

def set(var, input):
        
    os.putenv(var, input)
    
def get(var):  

    r=os.path.normpath(os.getenv(var))
    
    return r
        
def append(var, input):
        
    os.putenv(var, os.getenv(var) + ";" + input)
    
    return