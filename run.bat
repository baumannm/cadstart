:: set python path

call setpath

:: remove old logfiles
del /q %TEMP%\pyCADstartSTDOUT.txt
del /q %TEMP%\pyCADstartSTERR.txt
del /q %TEMP%\pyCADstartLOG.txt

:: run cadstart
python src\pyCADstart.pyw %1 %2 %3 %4 %5 %6 %7 %8 %9

:: combine STDERR and STDOUT
echo STDOUT: > %TEMP%\pyCADstartLOG.txt
type %TEMP%\pyCADstartSTDOUT.txt >> %TEMP%\pyCADstartLOG.txt
echo STDERR: >> %TEMP%\pyCADstartLOG.txt
type %TEMP%\pyCADstartSTDERR.txt >> %TEMP%\pyCADstartLOG.txt

:: open combined log
start %TEMP%\pyCADstartLOG.txt

pause