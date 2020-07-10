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
        if not title in self.listTitle:
            self.addTitle(title)

    def addTitle(self, title, DisplayTitle=""):
        '''
        添加一个标题,并为这个标题添加一个可选的显示名称
        '''
        typeis(title, str, "title")
        typeis(DisplayTitle, str, "DisplayTitle")

        if not title in self.listTitle:
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

    def tostring(self):
        templistTitle = []
        for i in range(len(self.listTitle)):
            t = self.listTitle[i]
            tt = self.mapTitleDisplay.get(t, t)
            templistTitle.append(tt)
        csv = ",".join(tuple(templistTitle))
        csv += "\r\n"
        for item in self.items:
            linearr = []
            for t in self.listTitle:
                if t in item:
                    linearr.append(item[t])
                else:
                    linearr.append("")
            csv += ",".join(tuple(linearr))
            csv += "\r\n"
        return csv


def csv2obj(csvString, TitleDisplayMap={}):
    typeis(csvString, str, "csvString")
    typeis(TitleDisplayMap, dict, "TitleDisplayMap")
    # 处理标题显示
    DTmap = {}
    for k, v in TitleDisplayMap.items():
        DTmap[v] = k
    # csv预处理
    lines = csvString.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if len(lines) <= 1:
        return []
    # 解析标题
    ts = lines.pop(0).split(",")
    for i in range(len(ts)):
        ts[i] = DTmap.get(ts[i], ts[i])
    # 处理每一行
    res = []
    for line in lines:
        item = {}
        iis = line.split(",")
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
            "t1": f"第{i}行的栏目1",
            "t2": f"第{i}行的栏目2",
            "t3": f"第{i}行的栏目3",
            "t4": f"第{i}行的栏目4",
        })
        c.next()
    csv = c.tostring()
    print("obj2csv")
    print(csv)
    print("csv2obj")
    print(csv2obj(csv))
