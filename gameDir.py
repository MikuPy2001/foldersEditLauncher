import os
import winreg
from codecs import open

import win32con
import win32ui

import regRead


def getOculusLibDirs():
    Libraries = r"HKEY_CURRENT_USER\SOFTWARE\Oculus VR, LLC\Oculus\Libraries"
    keys = regRead.regGetSubDirs(Libraries)
    if keys is None:
        return
    libs = []
    for key in keys:
        k = os.path.join(Libraries, key, "OriginalPath")
        res = regRead.regGetValue(k)
        if not res is None:
            if os.path.isdir(res):
                libs.append(res)
    return libs


def findGameInOculus(gameDir):
    res = getOculusLibDirs()
    if res is None :
        return
    for dir in res:
        gamebasedir = os.path.join(dir, "Software", gameDir)
        if os.path.isdir(gamebasedir):
            return gamebasedir


def getSteamDir():
    locs = [
        r'HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Valve\Steam\InstallPath',
        r'HKEY_LOCAL_MACHINE\SOFTWARE\Valve\Steam\InstallPath'
    ]
    for loc in locs:
        res = regRead.regGetValue(loc)
        if not res is None:
            return res


def getSteamLibDirs():
    dir = getSteamDir()
    if dir is None:
        return
    dirs = [os.path.join(dir, 'steamapps', 'common')]
    libraryfolders = os.path.join(dir, 'steamapps', 'libraryfolders.vdf')
    if not os.path.isfile(libraryfolders):
        return dirs

    with open(libraryfolders, 'r', "UTF-8") as f:
        for line in f.read().splitlines():
            words = line.split("\t")
            if len(words) < 4:
                continue
            if words[1].replace('"', "").isdigit():
                app = words[3].replace('"', "").replace("\\\\", "\\")
                gamedir = os.path.join(app, 'steamapps', "common")
                if os.path.isdir(gamedir):
                    dirs.append(gamedir)
    return dirs


def findGameInSteam(gameDirName):
    dirs = getSteamLibDirs()
    if dirs is None:
        return
    for libdir in dirs:
        gamedir = os.path.join(libdir, gameDirName)
        if os.path.isdir(gamedir):
            return gamedir


def getDirByUer():
    openFlags = win32con.OFN_OVERWRITEPROMPT | win32con.OFN_FILEMUSTEXIST
    fspec = 'Beat Saber.exe|Beat Saber.exe||'
    dlg = win32ui.CreateFileDialog(1, None, None, openFlags, fspec)
    dlg.SetOFNInitialDir(os.getcwd())
    dlg.SetOFNTitle("请选择游戏主文件")
    res = dlg.DoModal()
    if res == 1:
        filename = dlg.GetPathName()
        return os.path.dirname(filename)


def loadFile():
    gameFolder = os.path.join(os.getcwd(), "gameFolder")
    if os.path.isfile(gameFolder):
        with open(gameFolder, 'r', "UTF-8") as f:
            gameDir = f.read()
            gameexe = os.path.join(gameDir, "Beat Saber.exe")
            if os.path.isfile(gameexe):
                return gameDir


def saveFile(dir):
    gameFolder = os.path.join(os.getcwd(), "gameFolder")
    with open(gameFolder, 'w', "UTF-8") as f:
        f.write(dir)
    return dir


def isBeatSaberDir(dir):
    if dir is None or dir == "":
        return False
    return os.path.isfile(os.path.join(dir, "Beat Saber.exe"))


def getBeatSaberDir():
    # 从配置文件读
    dir = loadFile()
    if isBeatSaberDir(dir):
        return saveFile(dir)
    # 检测上一层目录是否就是游戏目录
    dir = os.path.dirname(os.getcwd())
    if isBeatSaberDir(dir):
        return saveFile(dir)
    # 从 Steam 检测游戏目录
    dir = findGameInSteam("Beat Saber")
    if isBeatSaberDir(dir):
        return saveFile(dir)
    # 从 Oculus 检测游戏目录
    dir = findGameInOculus("hyperbolic-magnetism-beat-saber")
    if isBeatSaberDir(dir):
        return saveFile(dir)


if __name__ == "__main__":
    getBeatSaberDir()
