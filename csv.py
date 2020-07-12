def typeis(obj, type1, s):
    if isinstance(obj, type1):
        return
    s = "{} not is {} , found {}".format(s, type(type1), type(obj))
    raise Exception(s)


class obj2csv:
    def __init__(self):
        self.mapTitleDisplay = {}
        self.item = {}
        self.items = []
        self.listTitle = []  # 决定顺序

    def setDisplayTitleMap(self, TitleDisplayMap):
        for key, value in TitleDisplayMap.items():
            self.setDisplayTitle(key, value)

    def setDisplayTitle(self, title, DisplayTitle):
        typeis(title, str, "title")
        typeis(DisplayTitle, str, "DisplayTitle")
        if title == "" or DisplayTitle == "":
            return
        self.mapTitleDisplay[title] = DisplayTitle
        if title not in self.listTitle:
            self.addTitle(title)

    def addTitle(self, title, DisplayTitle=""):
        '''
        添加一个标题,并为这个标题添加一个可选的显示名称
        '''
        typeis(title, str, "title")
        typeis(DisplayTitle, str, "DisplayTitle")

        if title not in self.listTitle:
            self.listTitle.append(title)

        if DisplayTitle != "":
            self.setDisplayTitle(title, DisplayTitle)

    def __Title(self, title):
        '''
        title 可能不存在,要添加
        title 可能是显示名称,要还原为标准名称
        '''
        typeis(title, str, "title")
        if title in self.listTitle:
            # 已存在
            return title
        for key, value in self.mapTitleDisplay.items():
            # 这是一个显示名称
            if value == title:
                return key
        # 新标题
        self.addTitle(title)
        return title

    def setValuemap(self, mapTitleValue):
        typeis(mapTitleValue, dict, "mapTitleValue")
        for key, value in mapTitleValue.items():
            self.setValue(key, value)

    def setValue(self, title, value):
        # 为当前记录设置一个值
        typeis(title, str, "title")
        typeis(value, str, "value")
        title1 = self.__Title(title)
        typeis(title1, str, "title1")

        self.item[title1] = value

    def next(self):
        # 完成当前记录并跳到下一个记录
        if len(self.item.keys()) > 0:
            self.items.append(self.item)
        self.item = {}

    def zuanyi(self, list):
        teplist = []
        for l in list:
            l = l.replace('"', '""')
            if ',' in l or '"' in l:
                l = '"' + l + '"'
            teplist.append(l)
        return tuple(teplist)

    def tostring(self):
        templistTitle = []
        for i in range(len(self.listTitle)):
            t = self.listTitle[i]
            tt = self.mapTitleDisplay.get(t, t)
            templistTitle.append(tt)
        csv = ",".join(self.zuanyi(templistTitle))
        csv += "\r\n"
        for item in self.items:
            linearr = []
            for t in self.listTitle:
                if t in item:
                    linearr.append(item[t])
                else:
                    linearr.append("")
            csv += ",".join(self.zuanyi(linearr))
            csv += "\r\n"
        return csv


def __split(line):
    start = True
    inside = False
    nextisquotes = False
    list = []
    teps = ""
    yh = '"'
    dh = ','
    llll = len(line)
    for i in range(llll):
        c = line[i]
        c1 = line[i+1] if i+1 < llll else ""
        if start and c == yh and c1 != yh:  # 引号开头,说明有特殊字符
            inside = True
        elif inside and c == yh and c1 == dh:  # 引号结尾
            inside = False
        elif inside and c == dh:  # 特殊字符中的逗号
            teps += dh
        elif nextisquotes:  # 特殊字符里的引号
            teps += yh
            nextisquotes = False
        elif c == yh and c1 == yh:  # 转义引号,下一轮循环由上一个判断块处理
            nextisquotes = True
        elif c == dh and not inside:  # 逗号结束
            list.append(teps)
            teps = ""
            start = True
            continue
        else:  # 无特殊情况就直接累加进字符串
            teps += c
        start = False
    list.append(teps)
    return list


def csv2obj(csvString, TitleDisplayMap={}):
    typeis(csvString, str, "csvString")
    typeis(TitleDisplayMap, dict, "TitleDisplayMap")
    # 处理标题显示
    DTmap = {}
    for k, v in TitleDisplayMap.items():
        DTmap[v] = k
    # csv预处理
    lines = csvString.splitlines(False)
    if len(lines) <= 1:
        return []
    # 解析标题
    ts = __split(lines.pop(0))
    for i in range(len(ts)):
        ts[i] = DTmap.get(ts[i], ts[i])
    # 处理每一行
    res = []
    for line in lines:
        item = {}
        iis = __split(line)
        for i in range(len(ts)):
            if i >= len(iis):
                break
            if iis[i] == "":
                continue
            item[ts[i]] = iis[i]
        if len(item.items()) > 0:
            res.append(item)
    return res


if __name__ == "__main__":
    c = obj2csv()
    c.setDisplayTitleMap({
        "t1": "标题1",
        "t2": "标题2",
        "t3": "标题3",
        "t4": "标题4",
    })
    for i in range(4):
        c.setValuemap({
            "t1": f"第{i}行的,栏目1",
            "t2": f'第{i}行的"栏目2',
            "t3": f"第{i}行的栏目3",
            "t4": f"第{i}行的栏目4",
        })
        c.next()
    csv = c.tostring()
    print("obj2csv")
    print(csv)
    print("csv2obj")
    obj = csv2obj(csv)
    import json
    jsont = json.dumps(obj, indent=4, ensure_ascii=False)
    print(jsont)
