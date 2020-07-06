python-3.6.4.exe /passive InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_test=0 TargetDir=c:\Python364
IF %ERRORLEVEL% equ 0 (echo "It is OK. Please Close program") & pause >nul