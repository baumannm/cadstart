
call setpath

cd src

python %PARSERPATH%\uic.py -o pyCADapp.py pyCADapp.ui
python %PARSERPATH%\uic.py -o pyCADui.py pyCADui.ui
python %PARSERPATH%\uic.py -o pyCADhelpui.py pyCADhelpui.ui
python %PARSERPATH%\uic.py -o pyCADdialogui.py pyCADdialogui.ui
python %PARSERPATH%\uic.py -o pyCADfeedbackFormui.py pyCADfeedbackFormui.ui

pause