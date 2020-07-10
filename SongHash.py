import csv
import json
import os
from codecs import open
from hashlib import sha1
from os import path
from xml.dom.minidom import parse

import urltools

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

    with open(infofile, 'r') as f:
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
        '('+info['_levelAuthorName']+')'
    return {"name": name,  "hash": hashcode.upper(), "info": info
            }


def getDirSongHash(dir):
    # 获取目录下所有歌曲的sha1,不包括子目录歌曲
    list = os.listdir(dir)
    songs = []
    for name in list:
        songdir = path.join(dir, name)
        if path.isdir(songdir):
            res = getSongInfo(songdir)
            if(res != False):
                songs.append(res)
                res['songdirname'] = name
    return songs


def getDirs(dir):
    # 读取当前游戏能加载的所有歌曲
    # 获取Beat Saber目录
    # TODO 检查是否为游戏目录
    foldersfile = path.join(dir, 'UserData', 'SongCore', 'folders.xml')
    res = [{"name": "默认目录",
            "loc": path.join(dir, 'Beat Saber_Data', 'CustomLevels')}]
    if not path.isfile(foldersfile):  # 没有自定义目录
        return res
    folders = parse(foldersfile).documentElement.getElementsByTagName("folder")
    for folder in folders:
        # TODO 跳过样例目录
        Name = folder.getElementsByTagName('Name')[0].firstChild.data
        Path = folder.getElementsByTagName('Path')[0].firstChild.data

        res.append({"name": Name,
                    "loc": Path})
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
    print(f"已加载{len(dirs)}个目录")
    songs = []
    for dir in dirs:
        for song in getDirSongHash(dir['loc']):
            song['foldername'] = dir['name']
            song['folderloc'] = dir['loc']
            songs.append(song)
    print(f"已加载{len(songs)}首歌曲")
    # 获取PP信息
    ppjson=getPPJson(ppurl)
    for song in songs:
        diffs=ppjson[song['hash']]['diffs']  # json里的diff
        for diff in diffs:
            # print(diff,diffs)
            if not diff['type'] == 1:  # 只统计最基础的模式
                continue
            song['pp-'+diff['diff']]=diff['pp']
            song['star-'+diff['diff']]=diff['star']
    # 生成csv
    print("正在生成csv")
    csvobj=csv.obj2csv()
    csvobj.setDisplayTitleMap(songkv)
    for song in songs:
        song.pop("info")
        song.pop("folderloc")
        csvobj.setValuemap(song)
        csvobj.next()
    return csvobj.tostring()


if __name__ == "__main__":
    with open(path.join(os.getcwd(), "目录.txt"), 'r', 'utf-8') as f:
        dir = f.readline().encode('utf-8').decode('utf-8-sig')
        dir = dir.replace("\r", "").replace("\n", "")
        ppurl = f.readline().replace("\r", "").replace("\n", "")
    dir = path.join(os.getcwd(), "Beat Saber")

    csv = main(dir, ppurl)

    with open(path.join(os.getcwd(), "歌曲.csv"), 'w', 'gbk') as f:
        f.write(csv)
        
