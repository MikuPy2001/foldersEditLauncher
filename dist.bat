@echo off
set dist=foldersEditLauncher
del /q %dist%.exe
PyInstaller %dist%.py -w --specpath spec -i "%~dp0Icon.ico"
REM move dist\%dist%.exe %dist%.exe

REM RD /q /s __pycache__
REM RD /q /s build
REM RD /q /s spec
REM RD /q /s dist