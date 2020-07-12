import csv
import json
import os
from codecs import open
from hashlib import sha1
from os import path
from xml.dom.minidom import parse

import urltools
from printTimer import printTimer

songkv = {
    "foldername": "目录名称",
    "newfoldername": "新目录",
    # "folderloc": "",
    "songdirname": "歌曲目录名称",
    "name": "歌曲名称",
    "hash": "",
    "pp-Easy": "PP值-容易",
    "pp-Normal": "PP值-通常",
    "pp-Hard": "PP值-困难",
    "pp-Expert": "PP值-专家",
    "pp-Expert+": "PP值-噩梦",
    "star-Easy": "难度-容易",
    "star-Normal": "难度-通常",
    "star-Hard": "难度-困难",
    "star-Expert": "难度-专家",
    "star-Expert+": "难度-噩梦",
}


def getSongInfo(loc):
    # 获取单个歌曲目录的sha1
    infofile = path.join(loc, 'info.dat')
    if not path.exists(infofile):
        return False

    with open(infofile, 'r', 'utf-8') as f:
        info = json.load(f)
    diffiles = []
    mapsset = info['_difficultyBeatmapSets']
    for map in mapsset:
        difs = map['_difficultyBeatmaps']
        for dif in difs:
            diffiles.append(dif['_beatmapFilename'])

    hash = sha1()
    with open(infofile, 'rb') as f:
        hash.update(f.read())
    for name in diffiles:
        file = path.join(loc, name)
        with open(file, 'rb') as f:
            hash.update(f.read())
    hashcode = hash.hexdigest()

    # print(path.basename(loc), hashcode, diffiles)
    name = info['_songName']+' - '+info['_songAuthorName'] + \
        '['+info['_levelAuthorName']+']'
    return {"name": name,  "hash": hashcode.upper(), "info": info
            }


def getDirSongHash(dir, pt):
    # 获取目录下所有歌曲的sha1,不包括子目录歌曲
    list = os.listdir(dir)
    songs = []
    for name in list:
        songdir = path.join(dir, name)
        if path.isdir(songdir):
            res = getSongInfo(songdir)
            if(res != False):
                pt.update(1)
                songs.append(res)
                res['songdirname'] = name
    return songs


def getDirs(dir):
    # 读取当前游戏能加载的所有歌曲
    # 获取Beat Saber目录
    # TODO 检查是否为游戏目录
    foldersfile = path.join(dir, 'UserData', 'SongCore', 'folders.xml')
    res = {'默认目录': path.join(dir, 'Beat Saber_Data', 'CustomLevels')}
    if not path.isfile(foldersfile):  # 没有自定义目录
        return res
    folders = parse(foldersfile).documentElement.getElementsByTagName("folder")
    for folder in folders:
        # TODO 跳过样例目录
        Name = folder.getElementsByTagName('Name')[0].firstChild.data
        Path = folder.getElementsByTagName('Path')[0].firstChild.data
        res[Name] = Path
    return res


def getPPJson(url):
    # 获取PP值的文件,带缓存
    file = path.join(os.getcwd(), "v2-all.json")
    if path.isfile(file):
        filetime = os.stat(file).st_mtime
        print("正在检查PP值文件更新")
        webtime = urltools.geturltime(url)
    else:
        filetime = -1
        webtime = 0
    if filetime < webtime:  # 文件不是最新的
        print("正在下载PP值文件")
        urltools.downfile(url, file)
    with open(file, 'r', "UTF-8") as f:
        return json.load(f)


def main(gamedir, ppurl):
    # 加载本地歌曲信息
    dirs = getDirs(gamedir)
    print(f"已加载{len(dirs.keys())}个目录")
    songs = []
    with printTimer("已加载 {} 首歌曲,平均速度为: {avg:.2f} 首每秒", True) as pt:
        for name, loc in dirs.items():
            for song in getDirSongHash(loc, pt):
                song['foldername'] = name
                song['folderloc'] = loc
                songs.append(song)
    print(f"已加载{len(songs)}首歌曲")
    # 获取PP信息
    ppjson = getPPJson(ppurl)
    for song in songs:
        hash = song['hash']
        if hash not in ppjson:
            continue
        diffs = ppjson[hash]['diffs']  # json里的diff
        for diff in diffs:
            # print(diff,diffs)
            if diff['type'] != 1:  # 只统计最基础的模式
                continue
            song['pp-'+diff['diff']] = diff['pp']
            song['star-'+diff['diff']] = diff['star']
    # 生成csv
    print("正在生成csv")
    csvobj = csv.obj2csv()
    csvobj.setDisplayTitleMap(songkv)
    for song in songs:
        song.pop("info")
        song.pop("folderloc")
        csvobj.setValuemap(song)
        csvobj.next()
    return csvobj.tostring()


def loadConfig():
    with open(path.join(os.getcwd(), "config.txt"), 'r', 'utf-8') as f:
        dir = f.readline().encode('utf-8').decode('utf-8-sig')
        dir = dir.replace("\r", "").replace("\n", "")
        ppurl = f.readline().replace("\r", "").replace("\n", "")
    # dir = path.join(os.getcwd(), "Beat Saber")
    return dir, ppurl


if __name__ == "__main__":
    dir, ppurl = loadConfig()

    csv = main(dir, ppurl)

    with open(path.join(os.getcwd(), "songs.csv"), 'w', 'gb18030') as f:
        f.write(csv)
