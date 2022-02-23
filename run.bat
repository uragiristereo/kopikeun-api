@echo off
cmd /c env\Scripts\activate.bat
flask run -h 0.0.0.0
pause