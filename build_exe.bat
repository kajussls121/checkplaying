@echo off
:start
if "%1" == "-d" (
    pyinstaller --onefile ^
    %2 %3 %4 %5 %6 %7 %8 %9 ^
    checkplaying.py
    set err=%ERRORLEVEL%
) else (
    pyinstaller --onefile ^
    %* checkplaying.py
    set err=%ERRORLEVEL%
)

choice /C YN /M "Do you want to launch dist.exe?"
if errorlevel 2 goto end
start dist\checkplaying.exe
echo Started.
:end
pause