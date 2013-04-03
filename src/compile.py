from cx_Freeze import setup, Executable

setup( name = "CADstart" , version = "3.3 beta" , description = "" , executables = [Executable(script = "pyCADstart.pyw", base = "Win32GUI")] , )