import random
from threading import Timer
import time


class printTimer():
    def __init__(self, format=None, intMode=False):
        self.format = format
        self.intMode = intMode
        self.bar = 0
        self.isupdate = False

    def __enter__(self):
        self.close = False
        self.time = self.lasttime = time.time()
        self.lastunit = 0
        Timer(1, self.__print__).start()
        return self

    def __exit__(self, type, value, trace):
        self.__print__()
        print()
        self.close = True

    def __print__(self):
        if self.close:
            return
        Timer(1, self.__print__).start()
        if not self.isupdate:
            return
        self.isupdate = False

        print("\r", end="")
        if self.format is None:
            print(self.printobj, end="")
        elif self.intMode:
            rtime = time.time()
            at = rtime-self.time
            rt = rtime-self.lasttime
            ru = self.bar-self.lastunit
            self.lasttime = rtime
            self.lastunit = self.bar
            avg = self.bar/at
            realtime = ru/rt
            s = self.format.format(self.bar, realtime=realtime, avg=avg)
            print(s, end="")
        else:
            s = self.format.format(self.printobj)
            print(s, end="")

    def update(self, obj):
        self.isupdate = True
        if self.intMode:
            self.bar += obj
        else:
            self.printobj = obj


if __name__ == "__main__":
    print("最简单的遍历")
    with printTimer() as pt:
        for i in range(1000):
            pt.update(i)
            time.sleep(0.001)
    print("格式化遍历")
    with printTimer("当前进度为:{}") as pt:
        for i in range(1000):
            pt.update(i)
            time.sleep(0.001)
    print("格式化遍历,带速度")
    with printTimer("当前进度为:{},平均速度为:{avg:.2f}kb/s,即时速度为:{realtime:.2f}kb/s", True) as pt:
        for i in range(1000):
            pt.update(i)
            f = random.randint(1, 99)/10000.0
            time.sleep(f)
