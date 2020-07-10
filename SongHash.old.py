import json
import os
import xml.dom.minidom
from codecs import open
from hashlib import sha1
from os import path
from time import mktime, sleep, strptime
from urllib.parse import urlparse
from xml.dom.minidom import parse

import requests
from tqdm import tqdm

dirs = [
    {
        "name": "",
        "loc": "",
        "songs": [
            {
                "name": "",
                "dirname": "",
                "hash": "",
                "info": "json(info.dat)",
                "pp": [
                    {
                        "diff": "",
                        "pp": "",
                        "star": ""
                    }
                ]
            }
        ]
    }
]


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
    return {"name": name,  "hash": hashcode.upper()
            # , "info": info
            }


def getDirSongHash(dir):
    # 获取目录下所有歌曲的sha1,不包括子目录歌曲
    list = os.listdir(dir)
    songs = []
    for name in list:
        songdir = path.join(dir, name)
        # print(name, songdir)
        if path.isdir(songdir):
            res = getSongInfo(songdir)
            # print(res)
            if(res != False):
                songs.append(res)
                res['dirname'] = name
                # dics[name] = res.upper()
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
    print("正在检查PP值文件更新")
    file = path.join(os.getcwd(), "v2-all.json")
    isold = True

    res = urlparse(url)
    header = {
        "authority": res.netloc,
        "scheme": res.scheme,
        "user-agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
        "dnt": "1",
        "accept": "*/*",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": res.scheme+'://'+res.netloc+'/',
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q:0.9,en;q:0.8"
    }
    # print(header)
    s = requests.Session()
    # 文件是否存在
    if path.isfile(file):
        # 文件是否最新
        import time
        time1 = time.time()
        res = s.head(url, headers=header, timeout=(5, 5))
        print(f"耗时{time.time()-time1}秒")
        res.raise_for_status()
        headertime = res.headers["Last-Modified"]
        # headertime: Sun, 21 Jun 2020 14:45:45 GMT
        timeformat = ("%a, %d %b %Y %H:%M:%S GMT")
        webtime = mktime(strptime(headertime, timeformat))
        filetime = os.stat(file).st_mtime
        # print(webtime, filetime)
        if filetime >= webtime:
            print("缓存为最新,无需更新")
            isold = False
    if isold:
        time1 = time.time()
        res = s.get(url, stream=True, headers=header, timeout=(5, 5))
        res.raise_for_status()
        with open(file, 'wb') as f:
            size = 0  # 初始化已下载大小
            for data in res.iter_content(chunk_size=1024):
                f.write(data)
                size += len(data)
                # 开始下载，显示下载文件大小
                print('\r正在下载PP值文件: '+'%.2f' % (size/1024)+' KB', end='')
        print("")
        print(f"耗时{time.time()-time1}秒")
    with open(file, 'r', "UTF-8") as f:
        return json.load(f)


def main(gamedir, ppurl):
    dirs = getDirs(gamedir)
    print(f"已加载{len(dirs)}个目录")
    lens = 0
    for dir in dirs:
        dir['songs'] = getDirSongHash(dir['loc'])
        lens += len(dir['songs'])
    print(f"已加载{lens}首歌曲")

    # 填充PP值
    ppjson = getPPJson(ppurl)
    for dir in dirs:
        for song in dir['songs']:
            diffs = ppjson[song['hash']]['diffs']  # json里的diff
            song['pp'] = []
            for diff in diffs:
                # print(diff,diffs)
                if not diff['type'] == 1:  # 只统计最基础的模式
                    continue
                song['pp'].append({
                    "diff": diff['diff'],
                    "pp": diff['pp'],
                    "star": diff['star']
                })
    return dirs


def toCsv(dirs):
    '''
    dirname newdir songdirname songname diff-pp siff-star ...
    '''
    diffset = set()  # 拿到所有难度
    for dir in dirs:
        for song in dir['songs']:
            for pp in song['pp']:
                diffset.add(pp['diff'])
    # 标题
    csv = "旧目录,新目录,歌曲目录,歌曲名称"
    for diff in diffset:
        csv += f",{diff}-pp,{diff}-star"
    csv += "\r\n"
    # 内容
    for dir in dirs:
        for song in dir['songs']:
            line = "{},,{},{}".format(
                dir['name'], song['dirname'], song['name'])
            for diff_ in diffset:
                has = False
                for pp in song['pp']:
                    if pp['diff'] == diff_:
                        has = True
                        line += ",{},{}".format(pp['pp'], pp['star'])
                if not has:
                    line += ",,"
            csv += line
    return csv


def text():
    with open(path.join(os.getcwd(), "目录.txt"), 'r', 'utf-8') as f:
        dir = f.readline().encode('utf-8').decode('utf-8-sig')
        dir = dir.replace("\r", "").replace("\n", "")
        ppurl = f.readline().replace("\r", "").replace("\n", "")
    dir = path.join(os.getcwd(), "Beat Saber")
    dirs = main(dir, ppurl)
    csv = toCsv(dirs)
    print(csv)


if __name__ == "__main__":
    text()
