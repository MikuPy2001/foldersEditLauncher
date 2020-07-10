import os
from time import mktime, strptime
from urllib.parse import urlparse

from requests import get, head
from tqdm import tqdm

from printTimer import printTimer


def createHeaders(url):
    res = urlparse(url)
    headers = {
        "authority": res.netloc,
        "scheme": res.scheme,
        "user-agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
        "dnt": "1",
        "accept": "*/*",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": res.scheme+'://'+res.netloc+'/',
        "accept-language": "zh-CN,zh;q:0.9,en;q:0.8"
    }
    return headers


def geturltime(url):
    header = createHeaders(url)
    res = head(url, headers=header, timeout=(5, 5))
    res.raise_for_status()
    headertime = res.headers["Last-Modified"]
    timeformat = ("%a, %d %b %Y %H:%M:%S GMT")
    webtime = mktime(strptime(headertime, timeformat))
    return webtime


def downfile(url, file):
    with open(file, 'wb') as f:
        header = createHeaders(url)
        res = get(url, stream=True, headers=header, timeout=(5, 5))
        res.raise_for_status()
        if "content-length" in res.headers:
            allsize = int(res.headers["content-length"])
            print((allsize, allsize/1024))
        else:
            allsize = 0
        if allsize > 0:
            with tqdm(total=allsize, unit="kb", ascii=True) as t:
                __private_downfile__(res, f, t)
        else:
            with printTimer("已下载:{:.2f}Kb,速度:{avg:.2f}kb/s,均速{realtime:.2f}kb/s", True) as pt:
                __private_downfile__(res, f, pt)


def __private_downfile__(url, file, update):
    for data in url.iter_content(chunk_size=1024):
        file.write(data)
        update.update(len(data))


if __name__ == "__main__":
    url = "http://myres.mikupy2001.cn/beatstar/bssb/v2-all.json"
    # url = "https://cdn.wes.cloud/beatstar/bssb/v2-all.json"
    downfile(url, os.path.join(os.getcwd(), "v2-all.bak1.json"))
