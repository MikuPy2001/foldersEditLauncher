import csv
import os
import sys
from codecs import open

import Song2csv

if __name__ == "__main__":
    songscsv = os.path.join(os.getcwd(), "songs.csv")
    if not os.path.isfile(songscsv):
        print("请先用song2csv生成csv文件并编辑后再使用本命令")
        sys.exit(-1)

    with open(songscsv, 'r', 'gb18030') as f:
        obj = csv.csv2obj(f.read(), Song2csv.songkv)

    dir, ppurl = Song2csv.loadConfig()
    res = Song2csv.getDirs(dir)
    for song in obj:
        oldfn = song['foldername']
        newfn = song['newfoldername']
        songd = song['songdirname']
        if oldfn in res and newfn in res:
            oldf = os.path.join(res[oldfn], songd)
            newf = os.path.join(res[newfn], songd)
            os.rename(oldf, newf)
