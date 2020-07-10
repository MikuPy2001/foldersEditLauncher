xmlhttp = new XMLHttpRequest()
xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == 4) {
        console.log(xmlhttp.status)
        console.log(xmlhttp.getAllResponseHeaders())
    }
}
url="http://myres.mikupy2001.cn/beatstar/bssb/v2-all.json"
xmlhttp.open("HEAD", url, true)
xmlhttp.send(null)