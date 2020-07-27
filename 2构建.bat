@echo off
set dist=foldersEditLauncher
set dlldir=C:\Users\admin\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\pywin32_system32

set cmd=PyInstaller
set cmd=%cmd% --specpath __pycache__/spec
set cmd=%cmd% --workpath __pycache__/build
REM set cmd=%cmd% -w
set cmd=%cmd% -i "%~dp0Icon.ico"
set cmd=%cmd% --version-file "%~dp0file_version_info.txt"
set cmd=%cmd% %dist%.py

echo %cmd%
%cmd%
copy "%~dp0Icon.png" "%~dp0dist\%dist%\Icon.png"
copy "%dlldir%\*.dll" "%~dp0dist\%dist%\"