
import winreg


def locSplit(loc, dir=False):
    locs = loc.split("\\")
    k = locs[0].upper()
    if k == "HKEY_CURRENT_USER":
        HKEY = winreg.HKEY_CURRENT_USER
    elif k == "HKEY_USERS":
        HKEY = winreg.HKEY_USERS
    elif k == "HKEY_LOCAL_MACHINE":
        HKEY = winreg.HKEY_LOCAL_MACHINE
    elif k == "HKEY_CLASSES_ROOT":
        HKEY = winreg.HKEY_CLASSES_ROOT
    elif k == "HKEY_CURRENT_CONFIG":
        HKEY = winreg.HKEY_CURRENT_CONFIG
    else:
        return
    l = len(locs)
    if dir:
        if l == 2:
            subloc = locs[1]
        elif l > 2:
            subloc = "\\".join(locs[1:])
        else:
            return
        return HKEY, subloc
    else:
        if l == 3:
            subloc = locs[1]
        elif l > 3:
            subloc = "\\".join(locs[1:-1])
        else:
            return
        return HKEY, subloc, locs[-1]


def regGetValue(loc):
    HKEY, subLoc, key = locSplit(loc)
    try:
        with winreg.OpenKey(HKEY, subLoc, 0, winreg.KEY_WOW64_64KEY | winreg.KEY_READ) as h:
            _data, _type = winreg.QueryValueEx(h, key)
            return _data
    except:
        print("regRead.py regGetValue OpenKey 异常")

def regGetSubDirs(loc):
    HKEY, subLoc = locSplit(loc, dir=True)
    try:
        with winreg.OpenKey(HKEY, subLoc, 0, winreg.KEY_WOW64_64KEY | winreg.KEY_READ) as h:
            subDirs = []
            try:
                i = 0
                while 1:
                    res = winreg.EnumValue(h, i)
                    subDirs.append(res)
                    i += 1
            except OSError:
                pass
            return subDirs
    except:
        print("regRead.py regGetSubDirs OpenKey 异常")
