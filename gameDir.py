import os
import winreg
from codecs import open

import win32con
import win32ui


def getSteamDir():
    try:
        steamreg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Valve\Steam',
                                  0, (winreg.KEY_WOW64_64KEY + winreg.KEY_READ))
    except:
        try:
            steamreg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Valve\Steam',
                                      0, (winreg.KEY_WOW64_64KEY + winreg.KEY_READ))
        except:
            return

    _data, _type = winreg.QueryValueEx(steamreg, "InstallPath")
    winreg.CloseKey(steamreg)
    return _data


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
            if os.path.isfile(gameDir):
                return gameDir


def saveFile(dir):
    gameFolder = os.path.join(os.getcwd(), "gameFolder")
    with open(gameFolder, 'w', "UTF-8") as f:
        f.write(dir)


def getBeatSaberDir():
    # 从配置文件读
    dir = loadFile()
    if dir is None:
        # 检测上一层目录是否就是游戏目录
        dir = os.path.dirname(os.getcwd())
        game = os.path.join(dir, "Beat Saber.exe")
        if not os.path.isfile(game):
            # 从steam 检测游戏目录
            dir = findGameInSteam("Beat Saber")
            if dir is None:
                # 直接让用户手选
                dir = getDirByUer()
                if dir is None:
                    # 没救了,再见
                    return
    saveFile(dir)
    return dir


# getBeatSaber()
