@echo off
set dist=foldersEditLauncher

set cmd=PyInstaller
set cmd=%cmd% --specpath __pycache__/spec
set cmd=%cmd% --workpath __pycache__/build
set cmd=%cmd% -w
set cmd=%cmd% -i "%~dp0Icon.ico"
set cmd=%cmd% --version-file "%~dp0file_version_info.txt"
set cmd=%cmd% %dist%.py
rem set cmd=%cmd% --key 123456789

echo %cmd%
%cmd%
copy "%~dp0Icon.png" "%~dp0dist\%dist%\Icon.png"